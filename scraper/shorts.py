import time

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

        driver.get(url)  # 요청

        # consent
        # consent.consent(driver)

        # wait for YouTube to load the page data
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'yt-shorts-video-title-view-model'))
        )


        # detail click
        driver.find_element(By.CSS_SELECTOR, 'yt-shorts-video-title-view-model').click()

        time.sleep(1)

        title = driver.find_element(By.CSS_SELECTOR, '#anchored-panel').find_element(By.CSS_SELECTOR,
                                                                             '#content #items #title').text

        like_count = driver.find_element(By.CSS_SELECTOR, '#anchored-panel').find_element(By.CSS_SELECTOR,
                                                                             '#content #items #factoids >factoid-renderer:nth-child(1)').text

        view_count = driver.find_element(By.CSS_SELECTOR, '#anchored-panel').find_element(By.CSS_SELECTOR,
                                                                             '#content #items #factoids > view-count-factoid-renderer').text

        regist_date = driver.find_element(By.CSS_SELECTOR, '#anchored-panel').find_element(By.CSS_SELECTOR,
                                                                             '#content #items #factoids > factoid-renderer:nth-child(3)').text

        shorts = {'title': title, 'like_count': like_count, 'view_count': view_count, 'regist_date': regist_date}

        return shorts


    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.quit()  # 드라이버 종료


if __name__ == "__main__":
    print("start")

    req_url = ['https://www.youtube.com/shorts/vidIegij9BY', 'https://www.youtube.com/shorts/2j0taLMF85U']
    data = scrape(req_url[1])

    file_utils.make_result_json(data, output_path = '../output/shorts.json')

    print("finish")
