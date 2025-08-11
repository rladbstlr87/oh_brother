import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class BandScraper:
    def __init__(self):
        self.band_url = os.getenv('BAND_URL')
        self.naver_id = os.getenv('BAND_NAVER_ID')
        self.naver_password = os.getenv('BAND_NAVER_PASSWORD')

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self):
        self.driver.get(self.band_url)
        time.sleep(3)

        # Click login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'a.u_btn.u_btn_primary')
        login_button.click()
        time.sleep(2)

        # Switch to Naver login
        naver_login_button = self.driver.find_element(By.CSS_SELECTOR, 'a[data-type="naver"] > span.u_tx')
        naver_login_button.click()
        time.sleep(2)

        # Input credentials
        self.driver.execute_script(f"document.getElementById('id').value = '{self.naver_id}'")
        self.driver.execute_script(f"document.getElementById('pw').value = '{self.naver_password}'")
        time.sleep(1)

        # Click final login button
        final_login_button = self.driver.find_element(By.ID, 'log.login')
        final_login_button.click()
        time.sleep(5) # Wait for login to complete

    def get_posts(self):
        self.driver.get(self.band_url)
        time.sleep(5) # Wait for page to load

        # Scroll down to load more posts (adjust scroll count as needed)
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find posts (this selector might need adjustment)
        posts = soup.find_all('div', class_='post_item') 
        return posts

    def close(self):
        self.driver.quit()
