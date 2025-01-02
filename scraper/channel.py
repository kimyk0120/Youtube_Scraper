from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import config_utils, driver_utils, file_utils

config = config_utils.init_config()

def scrape(url):

    try:
        driver = driver_utils.create_driver()
        driver.implicitly_wait(10)  # 동기화
        driver.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동

        if 'videos' not in url:
            url += '/videos'

        driver.get(url)  # 요청

        # load page data
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.dynamic-text-view-model-wiz__h1'))
        )

        # consent
        # consent.consent(driver)

        print("test")


    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.quit()  # 드라이버 종료


if __name__ == "__main__":
    print("start channel")

    req_url = 'https://www.youtube.com/@BrightData/videos'
    channel = scrape(req_url)

    # file_utils.make_result_json(video, output_path = '../output/channel.json')

    print("finish channel")
