from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json

def init_driver():

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu') 
    chrome_options.add_argument('--log-level=OFF')
    chrome_options.add_experimental_option("detach", True)
    s=Service(ChromeDriverManager().install())
    # Establish chrome driver and go to report site URL
    url = "https://exchange.sundaeswap.finance/#/"
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    driver.get(url)
    return (driver)
    
def scroll_to_bottom(driver):
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]')))
    SCROLL_PAUSE_TIME = 0.5
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
            element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]')))
            i = 1
            while True:
                try:
                    pair = element.find_element(by=By.XPATH, value=f'//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]/div[{i}]/div/div[1]/div/span/span')
                except:
                    break
                price = element.find_element(by=By.XPATH, value=f'//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]/div[{i}]/div/div[2]/div/span')
                prices_info[pair.text] = float(price.text[0:-2])
                i += 1
        except Exception as err:
            if ("Unable to locate element" in err):
                print("end")
        return (prices_info)

def get_sundae_swap_prices():
    driver = init_driver()
    scroll_to_bottom(driver)
    old = None
    while True:
        prices = find_prices(driver)
        prices = json.dumps(prices)
        with open("./sundae_prices.txt", 'w') as f:
            f.write(str(prices))
            f.close()
        driver.quit()
        return
        old = prices
        driver.refresh()
        time.sleep(15)
    return(prices)