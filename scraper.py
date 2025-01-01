from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def create_driver():
    """드라이버를 안전하게 생성하고 반환"""
    options = Options()
    options.add_argument('--no-sandbox')  # 보안 기능 비활성
    options.add_argument("--disable-extensions")  # 확장 프로그램 비활성
    options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

def scrape():
    """스크래핑 로직"""
    try:
        driver = create_driver()
        driver.implicitly_wait(10)  # 동기화
        driver.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
        url = 'https://www.youtube.com/watch?v=kuDuJWvho7Q'

        driver.get(url)  # 요청

        print("pausetime")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.quit()  # 드라이버 종료


if __name__ == "__main__":
    print("start")
    scrape()
    print("finish")
