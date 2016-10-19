#! /usr/bin/env python
# coding:utf-8

from selenium import webdriver
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
    take_screenshot(driver, save_fn= imScreenPath)
    imGetScreen = Image.open(imScreenPath)
    box = (x0, y0, x1, y1)
    img = imGetScreen.crop(box)
    img.save(imgPath)

    cn = yzmsb.CheckNum()
    checknum = cn.getCheckNum(imgPath)
    return checknum



def take_screenshot(browser, url ='', save_fn="capture.png"):
    #browser = webdriver.Firefox() # Get local session of firefox
    #browser.set_window_size(1200, 900)
    #browser.get(url) # Load page
    if len(url)>0:
        browser.get(url)
    browser.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)

    for i in xrange(5):
        if "scroll-done" in browser.title:
            break
        #time.sleep(0.5)

    browser.save_screenshot(save_fn)

def take_screenshot1(browser, url ='', save_fn="capture.png"):
    #browser = webdriver.Firefox() # Get local session of firefox
    #browser.set_window_size(1200, 900)
    #browser.get(url) # Load page
    print save_fn
    if len(url)>0:
        browser.get(url)
    browser.execute_script("""
            window.scroll(0, 400);
    """)

    # for i in xrange(5):
    #     if "scroll-done" in browser.title:
    #         break
    #     time.sleep(0.5)

    browser.save_screenshot(save_fn)


brower = webdriver.Firefox()
#brower = webdriver.PhantomJS()

brower.get('http://cpzjwyy.bjchp.gov.cn/fr/login.aspx')

brower.find_element_by_id('txtUsername').send_keys('612726198611070010')
brower.find_element_by_id('txtPassword').send_keys('860413')
cn = yzmsb.CheckNum()

#brower.get_screenshot_as_file(os.getcwd()+r'\abc.jpg')
#take_screenshot(brower, save_fn=(os.getcwd()+r'\abc.jpg'))
brower.save_screenshot(os.getcwd()+r'\abc.jpg')

chkImgEle = brower.find_element_by_id('chkImg')
location = chkImgEle.location
size = chkImgEle.size
print location
print size

img = Image.open(os.getcwd()+r'\abc.jpg')
img1 = img.crop((location['x'], location['y'], location['x']+size['width'], location['y']+size['height']))
img1.save(os.getcwd()+r'\1abc.jpg')

#time.sleep(0.5)
yzm = cn.getCheckNum(os.getcwd()+r'\1abc.jpg')
brower.find_element_by_id('txtCheckcode').send_keys(yzm)
flag = True
while flag:
    try:
        brower.find_element_by_id('btnlogin').click()
        flag = False
    except Exception,e:
        flag = True
        time.sleep(0.1)
        print 'x'

#time.sleep(0.5)

brower.get('http://cpzjwyy.bjchp.gov.cn/fr/revform.aspx?l=0&b=24')

#brower.find_element_by_id('ddlRevDate').send_keys('2016-10-21')

brower.find_element_by_id('txtPhone').send_keys('18911763612')

#brower.get_screenshot_as_file(os.getcwd()+r'\def.jpg')
print 'windows size', brower.get_window_size()
print brower.find_element_by_class_name('divcenter').size

take_screenshot1(brower, save_fn=(os.getcwd()+r'\def.jpg'))
#lib = WebDriverLib(brower)
#lib.take_screenshot_on_element(brower, chkImgEle,os.getcwd() )

chkImgEle = brower.find_element_by_id('chkImg')
location = chkImgEle.location
size = chkImgEle.size
print location
print size

img = Image.open(os.getcwd()+r'\def.jpg')
img1 = img.crop((location['x'], location['y']-400, location['x']+size['width'], location['y']+size['height']-400))
img1.save(os.getcwd()+r'\1def.jpg')

yzm = cn.getCheckNum(os.getcwd()+r'\1def.jpg')



brower.find_element_by_id('txtCode').send_keys(yzm)

#brower.find_element_by_id('lbtnNext').click()

time.sleep(10)

brower.close()