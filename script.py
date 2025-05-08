import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://localhost/v1/workflows/run'
api_key = 'app-zQiMzWrT8E0jbEZE89TrWJkB'

headers = {
    'Authorization': 'Bearer app-zQiMzWrT8E0jbEZE89TrWJkB',
    'Content-Type': 'application/json',
}
# 创建一个新的 Chrome 用户数据目录（如果不存在）
chrome_profile_dir = os.path.join(os.getcwd(), "chrome_profile")  # 在当前目录下创建 chrome_profile 文件夹
os.makedirs(chrome_profile_dir, exist_ok=True)  # 如果目录不存在则创建

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_dir}")  # 使用绝对路径
options.add_argument("--no-first-run")  # 跳过首次运行向导
options.add_argument("--no-default-browser-check")  # 跳过默认浏览器检查

driver = webdriver.Chrome(options=options)
driver.maximize_window()
# 打开登录页面
driver.get("https://www.zhipin.com/web/user/?ka=header-login")

input("按回车键关闭浏览器...")

# 打开选择应用界面
driver.get("https://www.zhipin.com/web/geek/jobs?city=100010000&position=100101,100116&jobType=1902&experience=108&industry=100020&scale=303")
input("按回车键关闭浏览器...")


ans = 0
while True:
    if ans > 100:
        break
    cards = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, "card-area"))
                        )
    for i in  range(13):
        #cards = driver.find_elements(By.CLASS_NAME,"card-area")
        cards = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, "card-area"))
                        )
        # if i >= len(cards):
        #     break
        card = cards[i]
        card.click()
        elements = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#wrap > div.page-jobs-main > div.job-recommend-result > div > div > div.job-detail-container > div.job-detail-box > div.job-detail-body > p"))
                        )
        
        text  = elements.text
        
        # 构建完整请求数据
        data = {
            "inputs": {"page":text },
            "response_mode": "blocking",
            "user": "eehf"
        }

        try:
           
            # response = requests.post(url, headers=headers, data=json.dumps(data))
            # print(response)
            # response.raise_for_status()  # 检查请求是否成功
            # response_data = response.json()
            # response_text = response_data.get('data', {}).get('outputs', {}).get('output',{}).get('output','')
            # if response_text == "Y":
                #chat = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/a[2]')
                chat = WebDriverWait(driver, 10).until( 
                    EC.element_to_be_clickable((By.XPATH,'//*[@id="wrap"]/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/a[2]'))
                        )

                print(chat.text)
                if chat.text != "立即沟通":
                    print("没有立即沟通按钮")
                    continue
                chat.click()
                #cancel =  driver.find_element(By.CLASS_NAME,"cancel-btn").click()
                cancel = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME,"cancel-btn"))
                        )
                cancel.click()
                #input("按回车键关闭浏览器...")
                print(i)
                ans += 1
            # elif response_text == "N":
            #     print("不符合要求")           
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")
    driver.refresh()
driver.quit()       




