import re
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.video import scrape as video_scrape
from utils import driver_utils


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
        driver.find_elements(By.CSS_SELECTOR, 'ytd-search #contents ytd-item-section-renderer ytd-video-renderer')


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