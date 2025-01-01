from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless=new')
options.add_argument('--no-sandbox')  # 보안 기능 비활성
options.add_argument("--disable-extensions")  # 확장 프로그램 비활성
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

def scrape():
    # scraping logic...
    url = 'https://www.youtube.com/watch?v=kuDuJWvho7Q'

    driver.get(url)
    driver.implicitly_wait(10)

    # print(driver.page_source)
    print("test")

    # close the browser and free up the resources
    driver.quit()


if __name__ == "__main__":
    print("start")

    scrape()

    print("finish")
