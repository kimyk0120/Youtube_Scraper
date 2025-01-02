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

        # consent
        # consent.consent(driver)

        # load page data
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.dynamic-text-view-model-wiz__h1'))
        )

        # ...더보기 버튼
        driver.find_element(By.CSS_SELECTOR, '#page-header button.truncated-text-wiz__absolute-button').click()

        # desc
        try:
            channel_description = driver.find_element(By.CSS_SELECTOR, '#description-container > span').text
        except Exception as e:
            channel_description = None
            print(e)

        # links
        links = []
        try:
            like_els = driver.find_element(By.ID, 'link-list-container').find_elements(By.CSS_SELECTOR,
                                                                        'yt-channel-external-link-view-model')
            for el in like_els:
                el_text = el.text
                txt_splt = el_text.split('\n')
                link_name = txt_splt[0]
                link_url = txt_splt[1]
                links.append({'name': link_name, 'url': link_url})

        except Exception as e:
            links = None
            print(e)

        # channel detail infos



        # close popup
        driver.find_element(By.CSS_SELECTOR, '#visibility-button').click()




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

    req_url = ['https://www.youtube.com/@BrightData/videos', 'https://www.youtube.com/@archive-os5yn']
    scrape(req_url[1])

    # file_utils.make_result_json(video, output_path = '../output/channel.json')

    print("finish channel")
