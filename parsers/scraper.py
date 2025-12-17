import os
import time
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class BandScraper:
    def __init__(self, scroll_count: int = 3, wait_seconds: int = 10):
        # 프로젝트 루트의 .env 로드 (중복 호출 안전)
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")

        self.band_url = os.getenv("BAND_URL")
        self.naver_id = os.getenv("BAND_NAVER_ID")
        self.naver_password = os.getenv("BAND_NAVER_PASSWORD")
        self.cookie_header = os.getenv("BAND_COOKIE_HEADER")
        self.auth_cookie_header = os.getenv("BAND_AUTH_COOKIE_HEADER")
        self.allow_manual_captcha = os.getenv("BAND_ALLOW_MANUAL_CAPTCHA", "false").lower() == "true"
        self.allow_manual_login = os.getenv("BAND_ALLOW_MANUAL_LOGIN", "false").lower() == "true"
        self.scroll_count = scroll_count
        self.wait_seconds = wait_seconds

        if not self.band_url:
            raise ValueError("BAND_URL 환경변수가 필요합니다.")

        # 쿠키가 없으면 계정 로그인 정보가 필요
        if not self.cookie_header and (not self.naver_id or not self.naver_password):
            raise ValueError("BAND_COOKIE_HEADER가 없으면 BAND_NAVER_ID, BAND_NAVER_PASSWORD가 필요합니다.")

        chrome_options = Options()
        if os.getenv("BAND_HEADLESS", "true").lower() != "false":
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

    def login(self):
        # 1) 쿠키가 있으면 로그인 스킵
        used_cookies = False
        if self.cookie_header:
            self._apply_cookie_header(self.cookie_header, "https://www.band.us")
            # auth 도메인에도 같은 쿠키 또는 별도 헤더 적용
            self._apply_cookie_header(
                self.auth_cookie_header or self.cookie_header, "https://auth.band.us"
            )
            self.driver.get(self.band_url)
            used_cookies = True
            # 쿠키 로그인 성공 여부 확인
            if not self._is_login_page():
                return
            # 쿠키만 있고 계정 정보가 없으면 더 진행 불가
            if not self.naver_id or not self.naver_password:
                if self.allow_manual_login:
                    self._wait_for_manual_login("쿠키 로그인에 실패했습니다. 브라우저에서 직접 로그인 후 Enter를 누르세요.")
                    if not self._is_login_page():
                        return
                raise RuntimeError("쿠키 로그인에 실패했고 계정 정보가 없어 진행할 수 없습니다.")

        # 밴드 공식 로그인 페이지에 next_url로 바로 진입
        login_url = "https://auth.band.us/login?next_url=" + quote(self.band_url, safe="")
        self.driver.get(login_url)

        wait = WebDriverWait(self.driver, self.wait_seconds)
        main_window = self.driver.current_window_handle

        # 네이버 로그인 버튼 클릭 (외부 로그인)
        naver_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.-naver.externalLogin"))
        )
        naver_btn.click()

        # 새 창/탭으로 전환
        wait.until(lambda drv: len(drv.window_handles) >= 1)
        if len(self.driver.window_handles) > 1:
            for handle in self.driver.window_handles:
                if handle != main_window:
                    self.driver.switch_to.window(handle)
                    break

        # 네이버 로그인 입력
        wait.until(EC.presence_of_element_located((By.ID, "id"))).send_keys(
            self.naver_id
        )
        wait.until(EC.presence_of_element_located((By.ID, "pw"))).send_keys(
            self.naver_password
        )
        wait.until(EC.element_to_be_clickable((By.ID, "log.login"))).click()

        # 로그인 완료 후 밴드 페이지로 이동/전환
        time.sleep(3)
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if "band.us" in self.driver.current_url:
                break

        # 네이버 측에서 캡차가 노출되면 자동 로그인 불가 상태로 간주
        if self.driver.find_elements(By.ID, "captchaimg") or self.driver.find_elements(
            By.ID, "captchaimg2"
        ):
            if self.allow_manual_captcha:
                print(
                    "캡차가 표시되었습니다. 브라우저(HEADLESS=false)에서 직접 풀이 후 Enter 키를 누르면 계속 진행합니다."
                )
                wait_seconds = int(os.getenv("BAND_MANUAL_CAPTCHA_WAIT", "120"))
                try:
                    input("캡차 풀이가 끝나면 Enter를 누르세요...")
                except EOFError:
                    # 터미널 입력이 막힌 경우 일정 시간 대기 후 진행
                    print(f"입력을 받을 수 없어 {wait_seconds}초 동안 대기합니다...")
                    time.sleep(wait_seconds)
            else:
                raise RuntimeError("네이버 로그인에 캡차가 표시되어 자동 로그인이 차단되었습니다.")

        # 자동 로그인 이후에도 로그인 페이지라면 수동 로그인 기회 제공
        if self._is_login_page() and self.allow_manual_login:
            self._wait_for_manual_login("자동 로그인 실패. 브라우저에서 직접 로그인 후 Enter를 누르세요.")
            if self._is_login_page():
                raise RuntimeError("수동 로그인 후에도 로그인 페이지입니다. 자격 증명 또는 쿠키를 확인하세요.")

    def _apply_cookie_header(self, cookie_header: str, base_url: str):
        # 드라이버에 쿠키를 추가하려면 먼저 해당 도메인으로 진입해야 함
        self.driver.get(base_url)
        cookies = self._parse_cookie_header(cookie_header)
        parsed = urlparse(base_url)
        for name, value in cookies:
            cookie_data = {
                "name": name,
                "value": value,
                "path": "/",
                "secure": base_url.startswith("https"),
            }
            if parsed.hostname:
                parts = parsed.hostname.split(".")
                if len(parts) >= 2:
                    base_domain = ".".join(parts[-2:])
                    cookie_data["domain"] = base_domain
            try:
                self.driver.add_cookie(cookie_data)
            except Exception:
                # 개별 쿠키 실패는 무시
                continue

    @staticmethod
    def _parse_cookie_header(cookie_header: str) -> List[tuple]:
        pairs = []
        for part in cookie_header.split(";"):
            if "=" not in part:
                continue
            name, value = part.split("=", 1)
            name = name.strip()
            value = value.strip().strip('"')
            if name:
                pairs.append((name, value))
        return pairs

    def _is_login_page(self) -> bool:
        url = self.driver.current_url.lower()
        title = (self.driver.title or "").lower()
        return ("auth.band.us/login" in url) or ("로그인" in title) or ("login" in url)

    def _wait_for_manual_login(self, message: str):
        wait_seconds = int(os.getenv("BAND_MANUAL_LOGIN_WAIT", os.getenv("BAND_MANUAL_CAPTCHA_WAIT", "120")))
        print(message)
        try:
            input("로그인이 끝나면 Enter를 누르세요...")
        except EOFError:
            print(f"입력을 받을 수 없어 {wait_seconds}초 동안 대기합니다...")
            time.sleep(wait_seconds)

    def get_posts_with_details(self) -> List[dict]:
        self.driver.get(self.band_url)
        try:
            WebDriverWait(self.driver, self.wait_seconds).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.postWrap"))
            )
        except TimeoutException:
            return []

        for _ in range(self.scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        posts = soup.select("div.postWrap article")

        results = []
        seen_keys = set()
        for post in posts:
            post_text = self._extract_post_text(post)
            attachment_urls = self._extract_attachments(post)
            timestamp = self._extract_timestamp(post)

            if post_text or attachment_urls or timestamp:
                key = (
                    timestamp or "",
                    post_text[:80] if post_text else "",
                    tuple(sorted(attachment_urls)),
                )
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                results.append(
                    {
                        "text": post_text,
                        "attachment_urls": attachment_urls,
                        "timestamp": timestamp,
                    }
                )

        return results

    @staticmethod
    def _extract_post_text(post) -> str:
        # 대표적인 본문 컨테이너 후보를 순서대로 조회
        text_candidates = [
            post.select_one("div.dPostTextView"),
            post.select_one("div.postMain"),
            post.select_one("div.textWrap"),
        ]
        for candidate in text_candidates:
            if candidate:
                text = candidate.get_text(" ", strip=True)
                if text:
                    return text
        return ""

    @staticmethod
    def _extract_attachments(post) -> List[str]:
        urls: List[str] = []
        selectors = [
            "a.collageImage._postMediaItem",
            "a._postPhotoItem",
            "a._postPhoto",
        ]
        for selector in selectors:
            for img in post.select(selector):
                href = img.get("href") or img.get("data-url")
                if href:
                    urls.append(href)
        return urls

    @staticmethod
    def _extract_timestamp(post) -> Optional[str]:
        time_element = post.select_one("time.time") or post.select_one("span.time")
        if time_element:
            value = time_element.get("datetime") or time_element.get_text(strip=True)
            return value or None
        return None

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    """
    디버그 실행용 엔트리포인트.
    - .env를 로드해 BAND_URL 등 설정을 사용
    - 캡차가 뜨면 환경 변수에 따라 수동 입력/대기 처리
    """
    scraper = None
    try:
        scraper = BandScraper()
        print("[scraper] 로그인 시도...")
        scraper.login()
        print("[scraper] 로그인 완료, 게시글 수집 시작...")
        posts = scraper.get_posts_with_details()
        print(f"[scraper] 게시글 {len(posts)}개 수집됨")
        if posts:
            for i, post in enumerate(posts[:3], 1):
                print(f"  #{i} text={post.get('text')[:50]!r} attachments={len(post.get('attachment_urls', []))} timestamp={post.get('timestamp')}")
    except Exception as e:
        print(f"[scraper] 오류: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if scraper:
            scraper.close()
            print("[scraper] 드라이버 종료")
