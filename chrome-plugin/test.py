from selenium import webdriver
from time import sleep
import requests
#from pykeyboard import PyKeyboard
#from pymouse import PyMouse


username = "junji23"
password = "13223"

profile = webdriver.FirefoxProfile("C:\\Users\\邱俊基\\Desktop\\chrome-plugin\\rust_mozprofile.WhXvBDcXFhpk")
#profile = webdriver.FirefoxProfile()
#profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.dir", "D:\\email")
#profile.set_preference("browser.download.manager.showWhenStarting",False)
#profile.set_preference('browser.helpApps.alwaysAsk.force',False)
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/xhtml+xml,application/xml,application/x-msdownload,application/octet/octet-stream,application/exe,txt/csv,application/pdf,application/x-msexcl,application/x-excel,application/excel,image/png,image/jpeg,text/html,text/plain,text/x-c")
#profile.set_preference('browser.helpApps.alwaysAsk.force',False)
driver = webdriver.Firefox(profile)
driver.get("https://mail.163.com/")

sleep(5)
driver.switch_to.frame(2)
#path5 = "//*[@id='loginDiv']/iframe/#document/html"
#driver.find_element_by_xpath(path5)
#xf = driver.find_element_by_xpath('//*iframe*[@style="width: 100%; height: 100%; border: none; background: none;"]')
#driver.switch_to.frame(xf)
driver.find_element_by_css_selector("[class='j-inputtext dlemail']").send_keys(username)
driver.find_element_by_css_selector("[class='j-inputtext dlpwd']").send_keys(password)
driver.find_element_by_id("dologin").click()

sleep(5)
cookies = driver.get_cookies()
#print(cookies)
for cookie in cookies:
    if cookie['name'] == 'Coremail.sid':
        sid = cookie['value']
url = 'https://mail.163.com/js6/main.jsp?sid=' + sid + '&df=mail163_letter#module=read.ReadModule|{"area"%3A"normal"%2C"isThread"%3Afalse%2C"viewType"%3A""%2C"id"%3A"59%3A1tbiOwcMA1XlgutJIgAAbB"%2C"fid"%3A1}'
#url = url[0:38] + sid + url[70:]
#print(url)
driver.switch_to_default_content()
driver.get(url)
#print requests.head(url).headers['content-type']
sleep(5)
#path3 = "//*[@id='dvContainer']/div[2]/div[0]/div[0]/div[0]/div[0]"
path3 = "//*[@class='nui-fIBlock py0']"
print("!!!!!")
print (requests.head(url).headers['content-type'])
name = driver.find_element_by_xpath(path3).text
print("!!!!")
path = "//*[@id='dvContainer']/div[2]/header/div/div[3]/div[5]"
driver.find_element_by_xpath(path).click()
sleep(5)
driver.switch_to_default_content()
path2 = "/html/body/div[5]/div[4]"
driver.find_element_by_xpath(path2).click()
sleep(2)
'''
#driver.quit()
sleep(5)
driver.switch_to.frame(0)
driver.find_element_by_css_selector("[class='j-inputtext dlemail']").send_keys(username)
driver.find_element_by_css_selector("[class='j-inputtext dlpwd']").send_keys(password)
driver.find_element_by_id("dologin").click()

sleep(5)
cookies = driver.get_cookies()
for cookie in cookies:
    if cookie['name'] == 'Coremail.sid':
        sid = cookie['value']
url = 'https://mail.163.com/js6/main.jsp?sid=' + sid + '&df=mail163_letter#module=read.ReadModule%7C%7B"area"%3A"normal"%2C"isThread"%3Afalse%2C"viewType"%3A""%2C"id"%3A"76%3A1tbiTB0LBlSIb4ivFAAAbc"%2C"fid"%3A1%7D'
driver.get(url)
sleep(5)
path = "//*[@id='dvContainer']/div[2]/header/div/div[3]/div[5]"
driver.find_element_by_xpath(path).click()
sleep(5)
path2 = "/html/body/div[5]/div[4]"
driver.find_element_by_xpath(path2).click()
sleep(5)
#driver.quit()'''