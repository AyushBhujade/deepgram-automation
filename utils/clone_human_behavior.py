import random
import re
import time
from selenium.webdriver.common.action_chains import ActionChains

def human_delay(min_sec=1.5, max_sec=4.5):
    time.sleep(random.uniform(min_sec, max_sec))

def scroll_into_view(element,driver):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(random.uniform(0.8, 1.6))

def human_move_to_element(element,driver):
    try:
        scroll_into_view(element,driver)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.5, 1.2))
        actions.perform()
    except:
        scroll_into_view(element)
        time.sleep(1.5)
        ActionChains(driver).move_to_element(element).perform()

def human_type(element, text):
    element.clear()
    human_delay(0.4, 0.9)
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.06, 0.17))
