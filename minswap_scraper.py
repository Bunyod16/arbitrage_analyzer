from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

def init_driver():

    chrome_options = Options()
    chrome_options.add_argument('--log-level=OFF')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu') 
    chrome_options.add_experimental_option("detach", True)
    s=Service(ChromeDriverManager().install())
    # Establish chrome driver and go to report site URL
    url = "https://app.minswap.org/"
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    driver.get(url)
    return (driver)
    
def scroll_to_bottom(driver):
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/main/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/span')))
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def find_prices(driver):
        prices_info = {}
        try:
            WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div.dark\:bg-dark.bg-light.relative.flex.min-h-full.w-full.flex-col.bg-fixed.font-main > main > div > div > div.overflow-hidden.rounded-xl.bg-white.shadow-main.dark\:bg-dark-800 > div > div:nth-child(3) > div:nth-child(2) > div > div > div.divide-y.divide-gray-200.dark\:divide-dark-600 > div:nth-child(1)')))
            i = 1
            while True:
                element = driver.find_element(by=By.CSS_SELECTOR, value=f'#__next > div.dark\:bg-dark.bg-light.relative.flex.min-h-full.w-full.flex-col.bg-fixed.font-main > main > div > div > div.overflow-hidden.rounded-xl.bg-white.shadow-main.dark\:bg-dark-800 > div > div:nth-child(3) > div:nth-child(2) > div > div > div.divide-y.divide-gray-200.dark\:divide-dark-600 > div:nth-child({i})')
                lst = element.text.split("\n")
                pair = lst[0].replace(" - ", "/")
                pair = pair[pair.find("/") + 1 :] + "/" + pair[0:pair.find("/")]
                price = lst[1]
                prices_info[pair] = float(price[0:-2])
                i += 1
                if (element == []):
                    break
        except Exception as err:
                print("finish")
        return (prices_info)

def get_min_swap_prices():
    driver = init_driver()
    scroll_to_bottom(driver)
    old = None
    while True:
        prices = find_prices(driver)
        prices = json.dumps(prices)
        with open("./minswap_prices.txt", 'w') as f:
            f.write(str(prices))
            f.close()
        driver.quit()
        return
        old = prices
        driver.refresh()
        time.sleep(15)