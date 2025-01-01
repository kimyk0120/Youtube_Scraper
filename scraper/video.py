import configparser
import json
import os

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '../config/config.ini')
config.read(config_path, encoding='utf-8')


def create_driver():
    """드라이버를 안전하게 생성하고 반환"""
    options = Options()
    options.add_argument('--no-sandbox')  # 보안 기능 비활성
    options.add_argument("--disable-extensions")  # 확장 프로그램 비활성
    options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

    return webdriver.Chrome(
        # service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

def scrape(url):
    """스크래핑 로직"""
    try:
        driver = create_driver()
        driver.implicitly_wait(10)  # 동기화
        driver.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동

        driver.get(url)  # 요청

        try:
            # wait up to 15 seconds for the consent dialog to show up
            consent_overlay = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'dialog'))
            )

            # select the consent option buttons
            consent_buttons = consent_overlay.find_elements(By.CSS_SELECTOR,
                                                            '.eom-buttons button.yt-spec-button-shape-next')
            if len(consent_buttons) > 1:
                # retrieve and click the 'Accept all' button
                accept_all_button = consent_buttons[1]
                accept_all_button.click()
            else:
                print('No consent buttons found')
        except TimeoutException:
            print('Cookie modal missing')

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

        # TODO scripts
        driver.find_element(By.CSS_SELECTOR, '#primary .ytd-structured-description-content-renderer .ytd-video-description-transcript-section-renderer button').click()



        video['url'] = url
        video['title'] = title
        video['channel'] = channel
        video['views'] = views
        video['publication_date'] = publication_date
        video['description'] = description
        video['likes'] = likes

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

    # 출력 경로 정의
    output_path = 'output/video.json'
    output_dir = os.path.dirname(output_path)

    # 디렉토리 생성 확인
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(video, file, ensure_ascii=False, indent=4)

    print("finish")
