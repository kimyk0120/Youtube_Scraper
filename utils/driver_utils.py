from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless=False):
    """드라이버를 안전하게 생성하고 반환"""
    options = Options()
    options.add_argument('--no-sandbox')  # 보안 기능 비활성
    options.add_argument("--disable-extensions")  # 확장 프로그램 비활성
    options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

    if headless:
        options.add_argument('--headless')

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )