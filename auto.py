from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


# 跳过登录页面
def skip_login(browser, url):
    browser.get(url)
    browser.add_cookie({'name': 'FSSBBIl1UgzbN7N443S', 'value': 'NnEQJ0CDxXqReaSxNLZIsoakHhe6Ivx1NENryvg3lRfduNMBMEQOA0GJgx9BjRP6'})
    browser.add_cookie({'name': 'FSSBBIl1UgzbN7N443T', 'value': '4Ke45LV9xe6GgakNryz3FVHJLHHJOjAE0TgDLKzgVUff_zEGgDq_WQWQhBoG4faHVG36ezGgccmvbT_MdPWOc.ANsajnrg4H4E37FVXsYfa1QUWCi_ERwhzSjSpIU_zwH6thmu1BxgQF5w20EgwNy8JBXxcYMSdEbqw9rXMOe1ryzXF2ZshJKxFci7unbLhr1ikYiOV4O7EoqLY.epf6wkT0D2Eemux.UHTPy2zXHm.JeoMtj2qf7fiRw5QNY1CEsPcTtX5.6ajC1G1PA.njrsUAEYIF.QgHC0BPf7cTwu4g9PFO0PWJGVhu0s9m2A_fQO.6m.Miu3Y77z0whS3QRxePxQzJq05dK8KAl4g736KTHRPpHOnsedPU7vvmkuI9m5Z9'})
    browser.add_cookie({'name': 'ASP.NET_SessionId', 'value': '0n1u3tlbbhnk1uvgmurks2vh'})
    browser.add_cookie({'name': '__SINDEXCOOKIE__', 'value': 'd8a459eb2d67b5fcb03b87f33cec9321'})

    browser.refresh()

def jump(browser, url='https://yjspy.cqut.edu.cn/student/yggl/qjsqb'):
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]')))
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/button[3]').click()

def main():
    url = 'https://yjspy.cqut.edu.cn/student/default/index'
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
    
    # 跳过登录页面
    skip_login(browser, url)
    # 跳转请假页面
    jump(browser)
    # 添加新表单
    add_new_form(browser)
    import time
    time.sleep(3)

if __name__ == '__main__':
    main()
