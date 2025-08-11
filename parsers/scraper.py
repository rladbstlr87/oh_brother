import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BandScraper:
    def __init__(self):
        self.band_url = os.getenv('BAND_URL')
        self.naver_id = os.getenv('BAND_NAVER_ID')
        self.naver_password = os.getenv('BAND_NAVER_PASSWORD')

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 헤드리스 모드로 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self):
        self.driver.get(self.band_url)
        time.sleep(3)

        # '로그인' 이라는 텍스트가 포함된 <a> 태그를 찾습니다.
        login_button = self.driver.find_element(By.XPATH, '//a[contains(text(), "로그인")]')
        login_button.click()
        time.sleep(2)

        # 네이버 로그인으로 전환
        naver_login_button = self.driver.find_element(By.CSS_SELECTOR, '#login_list > li:nth-child(3) > a')
        naver_login_button.click()
        time.sleep(2)

        # 로그인 정보 입력
        self.driver.execute_script(f"document.getElementById('id').value = '{self.naver_id}'")
        self.driver.execute_script(f"document.getElementById('pw').value = '{self.naver_password}'")
        time.sleep(1)

        # 최종 로그인 버튼 클릭
        final_login_button = self.driver.find_element(By.ID, 'log.login')
        final_login_button.click()
        time.sleep(5) # 로그인 완료 대기

    def get_posts_with_details(self):
        self.driver.get(self.band_url)
        time.sleep(5) # 페이지 로딩 대기

        # 추가 게시글 로드를 위한 스크롤 다운 (횟수 조정 가능)
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # 중요: 실제 게시글 전체를 감싸는 컨테이너 선택자로 수정 필수
        posts = soup.find_all('div', class_='#content > section > div:nth-child(17) > div:nth-child(2) > div > div.postWrap > div:nth-child(1) > article > div:nth-child(3) > div.postMain > div > div.dPostTextView > div > p') # PLACEHOLDER_SELECTOR

        results = []
        for post in posts:
            # 1. 게시글 텍스트 추출 (클래스: txtBody)
            text_element = post.find('div', class_='#content > section > div:nth-child(17) > div:nth-child(2) > div > div.postWrap > div:nth-child(1) > article > div:nth-child(3) > div.postMain > div > div.dPostTextView > div > p')
            post_text = text_element.get_text(strip=True) if text_element else ""

            # 2. 첨부 이미지 URL 목록 추출 (클래스: collageImage _postMediaItem)
            image_elements = post.select('a.collageImage._postMediaItem') # select 사용
            attachment_urls = [img['href'] for img in image_elements if img.has_attr('href')]

            # 3. 게시 시간 추출 (태그: time, 클래스: time)
            time_element = post.find('time', class_='time')
            timestamp = time_element.get_text(strip=True) if time_element else None

            # 텍스트, 첨부파일, 시간 중 하나라도 있으면 결과에 추가
            if post_text or attachment_urls or timestamp:
                details = {
                    'text': post_text,
                    'attachment_urls': attachment_urls,
                    'timestamp': timestamp
                }
                results.append(details)
        
        return results

    def close(self):
        self.driver.quit()
