#! /usr/bin/env python
# coding:utf-8

from selenium import webdriver
import selenium
import time
import os
import yzmsb
from PIL import Image

def getCheckImg(driver, x0, y0, x1, y1):
    u'''''获取验证码
    （startx，xstarty）---------------------------------
                      |     要截取的图片范围           |
                      |                                |
                      ---------------------------------- (endx,endy)
    '''
    imScreenPath = 'imsp.jpg'
    imgPath = 'checknum.jpg'
    driver.get_screenshot_as_file(imScreenPath)
    imGetScreen = Image.open(imScreenPath)
    box = (x0, y0, x1, y1)
    img = imGetScreen.crop(box)
    img.save(imgPath)

    cn = yzmsb.CheckNum()
    checknum = cn.getCheckNum(imgPath)
    return checknum

brower = webdriver.Firefox()

brower.get('http://cpzjwyy.bjchp.gov.cn/fr/login.aspx')

brower.find_element_by_id('txtUsername').send_keys('612726198611070010')
brower.find_element_by_id('txtPassword').send_keys('860413')
cn = yzmsb.CheckNum()

brower.get_screenshot_as_file(os.getcwd()+r'\abc.jpg')

chkImgEle = brower.find_element_by_id('chkImg')
location = chkImgEle.location
size = chkImgEle.size
print size

img = Image.open(os.getcwd()+r'\abc.jpg')
img1 = img.crop((location['x'], location['y'], location['x']+size['width'], location['y']+size['height']))
img1.save(os.getcwd()+r'\1abc.jpg')

time.sleep(0.5)
yzm = cn.getCheckNum(os.getcwd()+r'\1abc.jpg')
brower.find_element_by_id('txtCheckcode').send_keys(yzm)

brower.find_element_by_id('btnlogin').click()

time.sleep(0.5)

brower.get('http://cpzjwyy.bjchp.gov.cn/fr/revform.aspx?l=0&b=24')

brower.find_element_by_id('ddlRevDate').send_keys('2016-10-21')

brower.find_element_by_id('txtPhone').send_keys('18911763612')

brower.get_screenshot_as_file(os.getcwd()+r'\def.jpg')

chkImgEle = brower.find_element_by_id('chkImg')
location = chkImgEle.location
size = chkImgEle.size
print location
print size

img = Image.open(os.getcwd()+r'\def.jpg')
img1 = img.crop((location['x'], location['y'], location['x']+size['width'], location['y']+size['height']))
img1.save(os.getcwd()+r'\1def.jpg')

time.sleep(0.5)
yzm = cn.getCheckNum(os.getcwd()+r'\1def.jpg')


brower.find_element_by_id('txtCode').send_keys(yzm)

brower.find_element_by_id('lbtnNext').click()

brower.close()