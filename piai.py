from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib


scriptDir = pathlib.Path().absolute()
url = "https://pi.ai/talk"

chrome_options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument(f"user-data-dir={scriptDir}\\chromedata")
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening browser window)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get(url)
sleep(5)

def querySender(query):
    xPathInput = "/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/div[2]/textarea"
    xPathSendBtn = "/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/button"    
    try:
        driver.find_element(by=By.XPATH, value=xPathInput).send_keys(query)
    except Exception as e:
        print('Error: Input xpath not found', str(e))

    sleep(1)
    
    try:
        driver.find_element(by=By.XPATH, value=xPathSendBtn).click()
    except Exception as e:
        print('Error: Send button xpath not found', str(e))
        
    sleep(1)

querySender("hi bro. whats's the time now?")
sleep(150)