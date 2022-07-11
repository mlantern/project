from tracemalloc import start
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
import time

# 获取验证码图片
def get_code(browser, url):
    # 获取验证码图片
    browser.get(url)
    png = browser.find_element_by_id('imgVerifi')
    png.screenshot('capt.png')
    # 读取验证码图片
    image = Image.open('capt.png')
    # 将验证码图片转换为灰度图片
    image = image.convert('L')
    # 将灰度图片转换为二值图片
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')

    code = pytesseract.image_to_string(image)
    return code

def login(browser, url, username, password, code):
    # 进入登录页面
    # browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ff"]/div/div[1]/div[5]/button')))
    # 输入用户名
    username_input = browser.find_element_by_id('UserId')
    username_input.send_keys(username)
    # 输入密码
    password_input = browser.find_element_by_id('Password')
    password_input.send_keys(password)
    # # 输入验证码
    code_input = browser.find_element_by_id('VeriCode')
    code_input.send_keys(code)
    # 点击登录
    login_button = browser.find_element_by_xpath('//*[@id="ff"]/div/div[1]/div[5]/button')
    login_button.click()
    # 获取登录结果

def jump(browser, url='https://yjspy.cqut.edu.cn/student/yggl/qjsqb'):
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]')))
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/button[3]').click()

def text_input(browser, xpath, text):
    text_input = browser.find_element_by_xpath(xpath)
    text_input.clear()
    text_input.send_keys(text)

def add_new_form(browser):
    # 判断是否加载完成
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tagtr"]/td[2]/span/input[1]')))
    
    # 获取时间
    time_start, time_end = get_times()
    # 写入信息
    text_input(browser, '//*[@id="tagtr"]/td[2]/span/input[1]', '周边活动')
    text_input(browser, '//*[@id="tagtr"]/td[4]/span/input[1]', '周边活动(限12小时内)')
    text_input(browser, '//*[@id="qjkssj"]', time_start)
    text_input(browser, '//*[@id="qjjzsj"]', time_end)
    text_input(browser, '//*[@id="pjbxx"]/table/tbody/tr[6]/td[2]/span/input[1]', '1')
    # 提交表单
    browser.find_element_by_xpath('//*[@id="pjbxx"]/table/tbody/tr[13]/td/a[2]').click()

import datetime
def get_times():
    time_start = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(hours=+12.0)
    # 获取修改后的时间并格式化
    time_end = (time_start + offset).strftime('%Y-%m-%d %H:%M:%S')
    time_start = time_start.strftime('%Y-%m-%d %H:%M:%S')

    # 如果时间超过当天
    if time_end[0:10] != time_start[0:10]:
        time_end = time_start[0:10] + ' 22:59:59'
    return time_start, time_end

if __name__ == '__main__':
    url = 'https://yjspy.cqut.edu.cn/student/default/index'
    username = '52200313179'
    password = '52200313179'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["enable-logging", 'enable-automation'])
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
    browser.get(url)
    code = get_code(browser, url)
    # print(code)
    login(browser, url, username, password, code)
    time.sleep(3)

    # 跳转请假页面
    jump(browser)
    add_new_form(browser)