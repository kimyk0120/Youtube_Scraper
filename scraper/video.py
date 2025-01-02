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
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
        )

        video = {}

        title = driver \
            .find_element(By.CSS_SELECTOR, 'h1.ytd-watch-metadata') \
            .text

        # dictionary where to store the channel info
        channel = {}

        # scrape the channel info attributes
        channel_element = driver \
            .find_element(By.ID, 'owner')

        channel_url = channel_element \
            .find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint') \
            .get_attribute('href')
        channel_name = channel_element \
            .find_element(By.ID, 'channel-name') \
            .text
        channel_image = channel_element \
            .find_element(By.ID, 'img') \
            .get_attribute('src')
        channel_subs = channel_element \
            .find_element(By.ID, 'owner-sub-count') \
            .text \
            .replace(' subscribers', '')

        channel['url'] = channel_url
        channel['name'] = channel_name
        channel['image'] = channel_image
        channel['subs'] = channel_subs

        driver.find_element(By.ID, 'description-inline-expander').click()

        info_container_elements = driver \
            .find_elements(By.CSS_SELECTOR, '#info-container span')

        views = info_container_elements[0] \
            .text \
            .replace(' views', '')
        publication_date = info_container_elements[2] \
            .text

        description = driver \
            .find_element(By.CSS_SELECTOR, '#description-inline-expander .ytd-text-inline-expander span') \
            .text

        likes = driver \
            .find_element(By.CSS_SELECTOR, 'like-button-view-model button .yt-spec-button-shape-next__button-text-content') \
            .text

        # transcript
        try:
            driver.find_element(By.CSS_SELECTOR, '#primary .ytd-structured-description-content-renderer .ytd-video-description-transcript-section-renderer button').click()

            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#segments-container yt-formatted-string'))
            )

            string_els = driver.find_elements(By.CSS_SELECTOR, '#segments-container yt-formatted-string')
            t_scripts = ''
            for el in string_els:
                t_scripts += el.text + '\n'
        except Exception as e:
            print(e)
            t_scripts = None
            print("transcript not found")

        # scroll bottom for 댓글 개수 엘리먼트 로딩
        def scroll_down_page(speed=8):
            current_scroll_position, new_height = 0, driver.execute_script("return document.getElementById('content').scrollHeight")
            while current_scroll_position <= new_height:
                current_scroll_position += speed
                try:
                    driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                except Exception as e:
                    print("error scrolling down: {}".format(e))
                    break

        scroll_down_page(8)

        # wait foor revies
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#leading-section #count span'))
        )

        # reply count
        reply_count = driver.find_elements(By.CSS_SELECTOR, '#leading-section #count span')[1].text


        # video data
        video['url'] = url
        video['title'] = title
        # video['channel'] = channel  # channel 단위 일때는 필요하지 않음
        video['views'] = views
        video['publication_date'] = publication_date
        video['description'] = description
        video['likes'] = int(likes)
        video['transcript'] = t_scripts
        video['reply_count'] = int(reply_count)

        return video


    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 리소스 정리
        if driver:
            print("Driver closed")
            driver.quit()  # 드라이버 종료


if __name__ == "__main__":
    print("start")

    req_url = 'https://www.youtube.com/watch?v=kuDuJWvho7Q'
    video = scrape(req_url)

    file_utils.make_result_json(video, output_path = '../output/video.json')

    print("finish")
