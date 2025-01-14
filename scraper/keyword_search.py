import re
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.video import scrape as video_scrape
from utils import config_utils, driver_utils, file_utils

config = config_utils.init_config('../config/config.ini')

def scrape(search_keyword,):
    try:
        driver = driver_utils.create_driver(headless=False)
        driver.implicitly_wait(10)  # 동기화
        driver.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동

        driver.get('https://www.youtube.com/')  # 요청

        # consent
        # consent.consent(driver)

        # load page data
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="search_query"]'))
        )

        # input search word
        search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="search_query"]')
        search_input.send_keys(search_keyword)
        search_input.submit()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//yt-chip-cloud-chip-renderer[@chip-shape-data[contains(., "동영상")]]'))
        )

        video_chip = driver.find_element(By.XPATH, '//yt-chip-cloud-chip-renderer[@chip-shape-data[contains(., "동영상")]]')
        ActionChains(driver).move_to_element(video_chip).click().perform()


        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-search #contents ytd-item-section-renderer'))
        )

        # TODO 페이징 및 리미트 필요
        limit_count = int(config['CONFIG']['video_limit_cnt'])
        timeout_sec = int(config['CONFIG']['timeout_sec'])

        start_time = time.time()  # 현재 시간을 기록
        total_listings = []
        previous_list_size = 0

        new_height = driver.execute_script("return document.getElementById('content').scrollHeight")

        while True:
            try:
                driver.execute_script("window.scrollTo(0, {});".format(new_height))
                new_height = driver.execute_script("return document.getElementById('content').scrollHeight")

                targer_els = driver.find_elements(By.CSS_SELECTOR, 'ytd-search #contents ytd-item-section-renderer ytd-video-renderer')
                print("len(targer_els) : " , len(targer_els))
                time.sleep(1)

                for el in targer_els[previous_list_size:]:
                    video_url = el.find_element(By.CSS_SELECTOR, 'ytd-thumbnail #thumbnail').get_attribute('href')
                    channel_url = el.find_element(By.CSS_SELECTOR, '#channel-thumbnail').get_attribute('href')
                    if video_url not in total_listings:
                        start_time = time.time()
                        total_listings.append({'video_url':video_url, 'channel_url':channel_url})
                        print("appended url total len : ", len(total_listings))
                #
                # # 가져온 목록 수가 전체 목록수와 동일할 때 break
                # # 전체 목록수는 비공개, 삭제, 플레이리스트에 포함 등의 이유로 같지 않을 수 있음
                # if len(targer_els) == total_video_count:
                #     print("len(targer_els) == previous_list_size")
                #     break
                #
                # # 가져옥 목록 수가 이전 목록수와 동일하면서 시간이 리미트 시간이 경과했을때 break
                # if len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec:
                #     print("len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec")
                #     break
                #
                # if len(total_listings) >= limit_count:
                #     print("len(total_listings) >= limit_count")
                #     total_listings = total_listings[:limit_count]
                #     break
                #
                # previous_list_size = len(targer_els)

            except Exception as e:
                print("error scrolling down: {}".format(e))
                break


        print("end proc")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.quit()  # 드라이버 종료



if __name__ == "__main__":
    scrape('강아지사료')