import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import json

url = 'http://localhost/v1/workflows/run'
api_key = 'app-zQiMzWrT8E0jbEZE89TrWJkB'

headers = {
    'Authorization': 'Bearer app-zQiMzWrT8E0jbEZE89TrWJkB',
    'Content-Type': 'application/json',
}

driver = webdriver.Chrome()

# 打开登录页面
driver.get("https://www.zhipin.com/web/user/?ka=header-login")

input("按回车键关闭浏览器...")

# 打开选择应用界面
driver.get("https://www.zhipin.com/web/geek/jobs?city=100010000&position=100101,100116&jobType=1902&experience=108&industry=100020&scale=304")
input("按回车键关闭浏览器...")





cards = driver.find_elements(By.CLASS_NAME,"card-area")
for card in cards:
    card.click()
    time.sleep(1)
    text  = driver.find_elements(By.CLASS_NAME,"desc")[1].text
    
    print(text)
    # 构建完整请求数据
    data = {
        "inputs": {"page":text },
        "response_mode": "blocking",
        "user": "eehf"
    }

    try:
        # 发送请求并处理响应
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response)
        response.raise_for_status()  # 检查请求是否成功
        response_data = response.json()
        response_text = response_data.get('data', {}).get('outputs', {}).get('output',{}).get('output','')
        if response_text == "Y":
            # chat = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/a[2]')
            # chat.click()
            # time.sleep(1)
            #cancel =  driver.find_element(By.CLASS_NAME,"cancel-btn").click()
            #input("按回车键关闭浏览器...")
            print("符合要求")
        elif response_text == "N":
            print("不符合要求")           
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
    




