from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from ast import literal_eval
import re
from pyquery import PyQuery as pq
import pymongo
from pyvirtualdisplay import Display
import time

search = '沙琪玛'
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MANGO_TABLE = search

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def save_to_mongo(result):
    try:
        if db[MANGO_TABLE].insert(result):
            print('储存到MongoDB成功!', result)
    except Exception:
        print('储存到MongoDB失败！', result)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        )


# display = Display(visible=1, size=(1600, 902))
# display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')

# chrome_options.add_argument("--start-maximized")
# driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=["--ssl-protocol=any", "--ignore-ssl-errors=true", "--load-images=false", "--disk-cache=true"])
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.set_page_load_timeout(8)
url = 'https://www.taobao.com'

# url1 = 'https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
directional_url = 'https://s.taobao.com/search?q='+search+'&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset={}&ntoffset={}&p4ppushleft=1%2C48&s={}'
driver.get(url)
driver.implicitly_wait(1)
driver.delete_all_cookies()

cookies = ''
cookie_module = {'expires':'',
    'domain': '.taobao.com',
    'path': '/',
    'httpOnly': False,
    'HostOnly': False,
    'Secure': False,
}

with open(r'E:\taobaocookies.txt', 'r') as f:
    cookies = f.read()
pattern = re.compile('"name": "(.*?)",.*?"value": "(.*?)"', re.S)
items = re.findall(pattern, cookies)

for item in items:
    cookie = cookie_module
    cookie['name'] = item[0]
    cookie['value'] = item[1]
    driver.add_cookie(cookie)



wait = WebDriverWait(driver, 1)
# submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
# submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))

# input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
# input.send_keys('美食')
# submit.click()
def write_script():
    try:
        driver.execute_script(js1)
        driver.execute_script(js2)
        driver.execute_script(js3)
        driver.execute_script(js4)
        driver.execute_script('''const originalQuery = window.navigator.permissions.query;
                        window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                        );''')
    except Exception:
        print('写入js脚本失败！')

def slider():
    print('进入滑块页面!')
    write_script()
    time.sleep(0.1)
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1_n1z')))

    button.click()
    atcion = ActionChains(driver)
    atcion.click_and_hold(button).perform()
    atcion.reset_actions()

        
    for x in get_track(310, 8):
        atcion.move_by_offset(x, 0).perform()
        atcion = ActionChains(driver)
        # time.sleep(0.1)
    atcion.release().perform()  # 释放左键
    time.sleep(0.2)

import random
def get_track(distance, times):
    while times > 0.2:
        if times < 0.5:
            for x in range(int(times / 0.2)):
                yield int((distance/(times/0.2)))
                
            times = 0
        else:
            a = round(random.uniform(times*0.3, times - (times*0.3)), 1)
            b = random.randint(int(distance*0.3), int(distance - (distance*0.3)))
            for x in range(int(a / 0.2)):
                yield int((b/(a/0.2)))
            distance = distance-b
            times = times - a
        
    
    


js1= '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
js2= '''window.navigator.chrome = { runtime: {},  }; '''
js3= '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
js4= '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''


# while 1:
#     driver.execute_script(js1)
#     time.sleep(0.5)



# print(11111111111)
def get_maxpage():
    try:
        driver.get(directional_url.format('6', '6', '0'))
        # input.send_keys(Keys.ENTER)
    except TimeoutException:
        driver.execute_script('window.stop()')
    # time.sleep(100)
    try:
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        total = int(re.compile('(\d+)').search(total.text).group(1))     
    except TimeoutException:
        slider()
        return get_maxpage()
    return total


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'href':item.find('.row .J_ClickStat').attr('href'),
            'price':item.find('.price').text().replace('\n', ' '),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title ').text().replace('\n', ' '),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        save_to_mongo(product)

def next_page(page_number):
    print('当前页数：', page_number)
    driver.set_page_load_timeout(2)
    arg1 = 9 + ( page_number * -3)
    arg2 = -44 + (page_number * 44)
    try:
        print(directional_url.format(str(arg1), str(arg1), str(arg2)))
        driver.get(directional_url.format(str(arg1), str(arg1), str(arg2)))
        # driver.implicitly_wait(10)
    except TimeoutException:
        driver.execute_script('window.stop();')
    try:
        # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # input.clear()
        # input.send_keys(page_number)
        # submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1_n1z')))
            slider()
        except TimeoutException:
            pass
        next_page(page_number)
# print(total)




if __name__ == "__main__":
    write_script()
    # try:
    #     driver.get(directional_url.format('6', '6', '0'))
    #     # input.send_keys(Keys.ENTER)
    # except TimeoutException:
    #     driver.execute_script('window.stop()')
    total = get_maxpage()
    print('获取第一页...')
    get_products()
    for i in range(2, total + 1):
        next_page(i)
    print('爬取完毕！')
    driver.close()
# with open('E:/taobao.html', 'w', encoding='utf-8') as f:
#     f.write(driver.page_source)
# print(driver.page_source)




