import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import config_utils, driver_utils, file_utils
from scraper.video import scrape as video_scrape

config = config_utils.init_config('../config/config.ini')

def scrape(url, get_videos=True):

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

        # channel result data
        channel = {}

        # title
        title = driver.find_element(By.CSS_SELECTOR, 'h1.dynamic-text-view-model-wiz__h1').text

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
        # 0: email (hidden), 1: phone (hidden), 2: page_url, 3: subscriber, 4 : video count, 5: view count, 6: regist date, 7: None
        try:
            tr_els = driver.find_element(By.CSS_SELECTOR, '#additional-info-container').find_elements(By.CSS_SELECTOR,
                                                                                             "tr.description-item")
            page_url = tr_els[2].text
            subscriber = tr_els[3].text
            video_count = tr_els[4].text
            view_count = tr_els[5].text
            regist_date = tr_els[6].text

        except Exception as e:
            page_url = None
            subscriber = None
            video_count = None
            view_count = None
            regist_date = None
            print(e)


        # close popup
        driver.find_element(By.CSS_SELECTOR, '#visibility-button').click()

        if get_videos:
            # page scroll to end
            total_video_count = int(re.sub(r'\D', '', video_count))  # \D는 숫자가 아닌 모든 문자에 해당
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

                    targer_els = driver.find_elements(By.CSS_SELECTOR, '#content ytd-rich-item-renderer #content ytd-thumbnail #thumbnail[href]')
                    print("len(targer_els) : " , len(targer_els))
                    time.sleep(1)

                    for el in targer_els[previous_list_size:]:
                        video_url = el.get_attribute('href')
                        if video_url not in total_listings:
                            start_time = time.time()
                            total_listings.append(video_url)
                            print("appended video url total len : ", len(total_listings))

                    # 가져온 목록 수가 전체 목록수와 동일할 때 break
                    # 전체 목록수는 비공개, 삭제, 플레이리스트에 포함 등의 이유로 같지 않을 수 있음
                    if len(targer_els) == total_video_count:
                        print("len(targer_els) == previous_list_size")
                        break

                    # 가져옥 목록 수가 이전 목록수와 동일하면서 시간이 리미트 시간이 경과했을때 break
                    if len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec:
                        print("len(targer_els) == previous_list_size and time.time() - start_time > timeout_sec")
                        break

                    if len(total_listings) >= limit_count:
                        print("len(total_listings) >= limit_count")
                        total_listings = total_listings[:limit_count]
                        break

                    previous_list_size = len(targer_els)

                except Exception as e:
                    print("error scrolling down: {}".format(e))
                    break

            videos = []
            for listing in total_listings:
                print("go : ", listing)
                video = video_scrape(listing)
                videos.append(video)


        channel['title'] = title
        channel['description'] = channel_description
        channel['links'] = links
        channel['page_url'] = page_url
        channel['subscriber'] = subscriber
        channel['video_count'] = video_count
        channel['view_count'] = view_count
        channel['regist_date'] = regist_date
        if get_videos:
            channel['videos'] = videos

        return channel

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
    channel = scrape(req_url[0])

    file_utils.make_result_json(channel, output_path = '../output/channel.json')

    print("finish channel")
