import os
import sys
import django
from pprint import pprint
from pathlib import Path

from dotenv import load_dotenv

# Django 환경 설정
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from parsers.scraper import BandScraper  # noqa: E402


def run_test():
    """
    BandScraper를 직접 실행하여 결과를 확인하기 위한 테스트 함수
    """
    print("--- 스크래퍼 테스트 시작 ---")
    scraper = None
    try:
        scraper = BandScraper()

        print("1. 로그인 시도...")
        scraper.login()
        print("   로그인 성공!")

        print("2. 게시글 상세 정보 수집 시도...")
        posts_data = scraper.get_posts_with_details()

        print(f"\n--- 수집 결과: 총 {len(posts_data)}개의 게시글 데이터 발견 ---")

        if not posts_data:
            print("수집된 데이터가 없습니다. parsers/scraper.py의 선택자를 확인하세요.")
        else:
            pprint(posts_data)

        print("\n--- 스크래퍼 테스트 종료 ---")

    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if scraper:
            scraper.close()
            print("스크래퍼 리소스 정리 완료.")


if __name__ == "__main__":
    run_test()
