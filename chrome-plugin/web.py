'''
title           : blockchain_client.py
description     : A blockchain client implemenation, with the following features
                  - Wallets generation using Public/Private key encryption (based on RSA algorithm)
                  - Generation of transactions with RSA encryption      
author          : Adil Moujahid
date_created    : 20180212
date_modified   : 20180309
version         : 0.3
usage           : python blockchain_client.py
                  python3 blockchain_client.py -p 8080
                  python3 web.py --port 8080
python_version  : 3.6.1
Comments        : Wallet generation and transaction signature is based on [1]
References      : [1] https://github.com/julienr/ipynb_playground/blob/master/bitcoin/dumbcoin/dumbcoin.ipynb
'''

from collections import OrderedDict
import binascii


import requests
from flask import Flask, jsonify, request, render_template
from selenium import webdriver
from time import sleep
import base64
import os
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By 
from sklMain import *
from capture import *


app = Flask(__name__)

Ename = ''
Efeature = []
Eflag = 0
def download(url,username,password):
    print (os.getcwd())
    downway = os.getcwd()+'\email'
    profile = webdriver.FirefoxProfile("./rust_mozprofile.WhXvBDcXFhpk")
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", downway)
    profile.set_preference("--headless",1)
    #profile.add_argument('--headless')
    #profile.add_argument('--disable-gpu')
    driver = webdriver.Firefox(profile)
    driver.get("https://mail.bupt.edu.cn")

    WebDriverWait(driver,20,0.5).until(
        EC.presence_of_element_located((By.ID, 'F_password')))  

    #driver.switch_to.frame(2)
    '''163
    driver.find_element_by_css_selector("[class='j-inputtext dlemail']").send_keys(username)
    driver.find_element_by_css_selector("[class='j-inputtext dlpwd']").send_keys(password)
    driver.find_element_by_id("dologin").click()
    '''
    driver.find_element_by_id("F_email").send_keys(username)
    driver.find_element_by_id("F_password").send_keys(password)
    driver.find_element_by_id("action").click()
    url_last = 'https://mail.bupt.edu.cn/' + url
    driver.get(url_last)
    return
    '''
    sleep(10)
    cookies = driver.get_cookies()
    #print(cookies)
    for cookie in cookies:
        if cookie['name'] == 'Coremail.sid':
            sid = cookie['value']
    #url = 'https://mail.163.com/js6/main.jsp?sid=' + sid + '&df=mail163_letter#module=read.ReadModule|{"area"%3A"normal"%2C"isThread"%3Afalse%2C"viewType"%3A""%2C"id"%3A"59%3A1tbiOwcMA1XlgutJIgAAbB"%2C"fid"%3A1}'
    url = url[0:38] + sid + url[70:]
    #print(url)
    driver.switch_to_default_content()
    driver.get(url)
    #print requests.head(url).headers['content-type']
    sleep(5)
    #path3 = "//*[@id='dvContainer']/div[2]/div[0]/div[0]/div[0]/div[0]"
    path3 = "//*[@class='nui-fIBlock py0']"
    print("!!!!!")
    name = driver.find_element_by_xpath(path3).text
    print("!!!!")
    path = "//*[@id='dvContainer']/div/header/div/div[3]/div[5]"
    driver.find_element_by_xpath(path).click()
    sleep(10)
    #driver.switch_to_default_content()#js-component-menu nui-menu
    path2 = "/html/body/div[6]/div[4]"
    #path2 = "//*[@class='js-component-menu nui-menu']"
    driver.find_element_by_xpath(path2).click()
    sleep(2)
    '''
    '''chrome
    options = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #options.add_experimental_option("prefs", prefs)
    prefs = {'safebrowsing': 'false'}
    #prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\email'}
    options.add_experimental_option('prefs', prefs)
    #options.add_argument("--disable-popup-blocking")
    #options.add_argument("safebrowsing.enabled" = true)

    driver = webdriver.Chrome(chrome_options = options)
    driver.get("https://mail.163.com/")


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
    #url = 'https://mail.163.com/js6/main.jsp?sid=' + sid + '&df=mail163_letter#module=read.ReadModule%7C%7B"area"%3A"normal"%2C"isThread"%3Afalse%2C"viewType"%3A""%2C"id"%3A"76%3A1tbiTB0LBlSIb4ivFAAAbc"%2C"fid"%3A1%7D'
    url = url[0:38] + sid + url[70:]
    driver.get(url)
    sleep(5)
    #path3 = "//*[@id='dvContainer']/div[2]/div[0]/div[0]/div[0]/div[0]"
    path3 = "//*[@class='nui-fIBlock py0']"
    print("!!!!!")
    name = driver.find_element_by_xpath(path3).text
    print("!!!!")
    path = "//*[@id='dvContainer']/div[2]/header/div/div[3]/div[5]"
    driver.find_element_by_xpath(path).click()
    sleep(5)
    path2 = "/html/body/div[5]/div[4]"
    driver.find_element_by_xpath(path2).click()
    sleep(5)
    '''
    #return name

#这个才是最新的
@app.route('/get_url1', methods=['GET'])
def get_url1():
    name = request.args.get('name')
    name = str(base64.b64decode(name),'utf-8')
    name = name.replace('&nbsp;',' ')
    pdfname = request.args.get('pdfname')
    if(pdfname == '1'):
        print('no pdf')
    sleep(3)
    global Ename
    Ename = name
    print(Ename)
    filename1 = "./email/"+name+".eml"
    filename2, feature, numfeature = extract_formal(filename1, name)
    print('file2'+filename2)
    global Efeature
    Efeature = numfeature
    result = predict(filename2)
    if result == 'Good email':
        global Eflag
        Eflag = 1
    if result == 'Phishing email':
        Eflag = 0
    response = {'feature':feature,'message': result}
    # print(result)
    # print(feature)
#    response = {'message': '该邮件为html格式'}
    return jsonify(response), 200

@app.route('/get_url', methods=['GET'])
def get_url():
    url = request.args.get('url')
    url = str(base64.b64decode(url),'utf-8')
    username = request.args.get('username')
    password = request.args.get('password')
    name = request.args.get('name')
    name = str(base64.b64decode(name),'utf-8')
    name = name.replace('&nbsp;',' ')
    download(url,username,password)
    response = {'message': '该邮件为html格式'}
    return jsonify(response), 200


@app.route('/back', methods=['GET'])
def back():
    flag = request.args.get('flag')
    name = request.args.get('name')
    name = name.replace('&nbsp;',' ')
    print(flag)
    print("/////")
    # # print(name)
    # print(Eflag)
    if flag =='true' and Eflag == 1:
        dataname = "./train/normal.txt"
        file_write = open(dataname, 'a+')
        file_write.writelines(Efeature + '\n')
        print(Efeature)
    if flag == 'true' and Eflag == 0:
        dataname = "./train/phishing.txt"
        file_write = open(dataname, 'a')
        file_write.writelines(Efeature + '\n')
        print(Efeature)
    if flag == 'false' and Eflag == 1:
        dataname = "./train/phishing.txt"
        file_write = open(dataname, 'a')
        file_write.writelines(Efeature + '\n')
        print(Efeature)
    if flag == 'false' and Eflag == 0:
        dataname = "./train/normal.txt"
        file_write = open(dataname, 'a')
        file_write.writelines(Efeature + '\n')
        print(Efeature)
    response = {'message': 'Thanks for your help, our Detction will be more accurate!'}
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
#    Ename = ''
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8089, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port,debug=True)