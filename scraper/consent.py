from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def consent(driver,):
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
