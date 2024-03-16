from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import time
from dotenv import load_dotenv
import os


# 디스코드 웹훅 URL
load_dotenv()
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

# 확인할 사이트 URL
TARGET_URL = "https://kloa.gg/merchant"

sub_strs = ["카마인","웨이", "아만 카드", "아제나","바훈투르","바르칸","에버그레이스","모카모카","라하르트","페데리코","다르시","라자람","라카이서스"]


def server_select(server):
    time.sleep(0.5)
    
    #서버목록 선택
    element = driver.find_element(By.ID, "headlessui-combobox-input-:r2:")
    element.click()

    time.sleep(0.5)
    # #루페온
    # lupeon_element = driver.find_element(By.XPATH, "//span[text()='루페온']")
    select_server = driver.find_element(By.XPATH, f"//span[text()='{server}']")
    select_server.click()


def send_discord_message(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    
    if response.status_code != 204:
        raise ValueError(f"Request to discord returned an error {response.status_code}, the response is:\n{response.text}")
    

def check_strings(main_str, sub_strs, server):
    for sub_str in sub_strs:
        if sub_str in main_str:
            discord_send_message = f"{server} 서버에 {datetime.now().strftime('%H:%M')} {sub_str} 출현"
            send_discord_message(webhook_url, discord_send_message)
        else:
            print(f"'{sub_str}' 없음")
            
def card_checker(server):
    server_select(server)
    time.sleep(0.5)
    div_text = driver.find_element(By.CSS_SELECTOR, 'div.mb-\\[30px\\]').text
    time.sleep(0.5)
    check_strings(div_text, sub_strs, server)
    
options = webdriver.ChromeOptions()
options.add_argument('headless')
    
driver = webdriver.Chrome(options=options) 
driver.get(TARGET_URL)
# time.sleep(2)
driver.implicitly_wait(3)

card_checker("루페온")
card_checker("아만")