import re
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.shorts import scrape as shorts_scrape
from scraper.channel import scrape as channel_scrape
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
            EC.presence_of_element_located((By.XPATH, '//yt-chip-cloud-chip-renderer[@chip-shape-data[contains(., "Shorts")]]'))
        )

        video_chip = driver.find_element(By.XPATH, '//yt-chip-cloud-chip-renderer[@chip-shape-data[contains(., "Shorts")]]')
        ActionChains(driver).move_to_element(video_chip).click().perform()


        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-search #contents ytd-item-section-renderer'))
        )

        # 페이징 및 리미트 필요
        limit_count = int(config['CONFIG']['video_limit_cnt'])
        timeout_sec = int(config['CONFIG']['timeout_sec'])

        start_time = time.time()  # 현재 시간을 기록
        total_listings = []
        visited_urls = set()  # 중복 방지를 위한 Set
        previous_list_size = 0

        scroll_position = 500
        scroll_increment = 300

        while True:
            try:
                scroll_position += scroll_increment
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")

                time.sleep(2)

                targer_els = driver.find_elements(By.CSS_SELECTOR, 'ytd-search #primary  #contents ytd-item-section-renderer.ytd-section-list-renderer #contents > ytd-video-renderer')
                print("len(targer_els) : " , len(targer_els))

                for el in targer_els[previous_list_size:]:
                    if el.aria_role == 'generic':
                        video_url = el.find_element(By.CSS_SELECTOR, 'ytd-thumbnail > #thumbnail').get_attribute('href')
                        channel_url = el.find_element(By.CSS_SELECTOR, '#channel-thumbnail').get_attribute('href')
                        if video_url not in visited_urls:
                            start_time = time.time()
                            visited_urls.add(video_url)  # Set에 추가
                            total_listings.append({'video_url':video_url, 'channel_url':channel_url})
                            print("appended url total len : ", len(total_listings))

                # # 가져옥 목록 수가 이전 목록수와 동일하면서 시간이 리미트 시간이 경과했을때 break
                if len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec:
                    print("len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec")
                    break

                # limit count
                if len(total_listings) >= limit_count:
                    print("len(total_listings) >= limit_count")
                    total_listings = total_listings[:limit_count]
                    break

                # 메시지가 HTML에 포함되어 있는지 확인
                page_html = driver.page_source
                if "결과가 더 이상 없습니다" in page_html:
                    print("더 이상 결과가 없습니다. 반복문 종료.")
                    break
                else:
                    print("'결과가 더 이상 없습니다' 메시지가 발견되지 않았습니다. 계속 진행.")

                previous_list_size = len(targer_els)

            except Exception as e:
                print("error scrolling down: {}".format(e))
                break
        result_info = []
        for url_info in total_listings:
            shorts = shorts_scrape(url_info['video_url'])
            channel = channel_scrape(url_info['channel_url'], get_videos=False)
            result_info.append({'shorts':shorts, 'channel':channel})

        results = {'search_keyword':search_keyword, 'data':result_info , 'scrape_date':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}
        file_utils.make_result_json(results, output_path = '../output/output.json')

        print("end proc")
        return results

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.close()
            driver.quit()  # 드라이버 종료



if __name__ == "__main__":
    scrape('강아지사료')