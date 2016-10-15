#! /usr/bin/env python
# coding:utf-8

import sys
import urllib2
import urllib
import cookielib
import zlib
from HTMLParser import HTMLParser
from yzmsb import CheckNum

## fix Chinese
reload(sys)
sys.setdefaultencoding("utf8")


#####################################################


class WebOp:
    def __init__(self):
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'max-age=0',
            #'Connection': 'keep-alive',
            'Host': 'cpzjwyy.bjchp.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
    def ungzip_html(self, response):
        try:  # try decompress
            data = ''
            origData = response.read()
            if ('Content-Encoding' in response.info()) and (response.info()['Content-Encoding'] == 'gzip'):
                data = zlib.decompress(origData, 16 + zlib.MAX_WBITS)
            return data
        except Exception, e:
            raise Exception('ungzip error:' + str(e))


    def brower(self, url, params=[]):
        try:
            if len(params)>0:
                req = urllib2.Request(url, urllib.urlencode(params))
            else:
                req = urllib2.Request(url)

            for headerKey in self.header.keys():
                req.add_header(headerKey,self.header[headerKey])

            res = self.opener.open(req)

            result = self.ungzip_html(res)

            print req.header_items()

            return result
        except Exception, e:
            print 'Brower url:[' + url +'] error, params:[' + str(params) +'], reason:[' + str(e)
            raise Exception('login error:' + str(e))

    def dlFile(self, url, filePath):
        req = urllib2.Request(url)
        for headerKey in self.header.keys():
            req.add_header(headerKey, self.header[headerKey])
        operate = self.opener.open(req)
        data = operate.read()

        if data == None:
            return

        file = open(filePath, "wb")
        file.write(data)
        file.flush()
        file.close()


class webParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.key = {'EVENTTARGET': '', 'EVENTARGUMENT': '', 'LASTFOCUS': '', 'VIEWSTATE':'', 'EVENTVALIDATION':''}

    def handle_starttag(self,tag,attrs):
        if tag == 'input' and attrs.__contains__(('id', '__EVENTTARGET')):
            for k,v in attrs:
                if k=='value':
                    self.key['EVENTTARGET']=v
        elif tag == 'input' and attrs.__contains__(('id', '__EVENTARGUMENT')):
            for k,v in attrs:
                if k=='value':
                    self.key['EVENTARGUMENT']=v
        elif tag == 'input' and attrs.__contains__(('id', '__LASTFOCUS')):
            for k,v in attrs:
                if k=='value':
                    self.key['LASTFOCUS']=v
        elif tag == 'input' and attrs.__contains__(('id', '__VIEWSTATE')):
            for k,v in attrs:
                if k=='value':
                    self.key['VIEWSTATE']=v
        elif tag == 'input' and attrs.__contains__(('id', '__EVENTVALIDATION')):
            for k, v in attrs:
                if k == 'value':
                    self.key['EVENTVALIDATION'] = v

    # def handle_data(self, data):
    #     if self.key['EVENTTARGET']:
    #         print 'EVENTTARGET:%s\t|' % data,
    #         self.key['EVENTTARGET'] = None
    #     elif self.key['EVENTARGUMENT']:
    #         print 'EVENTTARGET:%s\t|' % data,
    #         self.key['EVENTARGUMENT'] = None
    #     elif self.key['LASTFOCUS']:
    #         print 'LASTFOCUS:%s\t|' % data
    #         self.key['LASTFOCUS'] = None
    #     elif self.key['VIEWSTATE']:
    #         print 'VIEWSTATE:%s\t|' % data
    #         self.key['VIEWSTATE'] = None


class CPJW:
    web = WebOp()
    parser = webParser()
    first_url = 'http://cpzjwyy.bjchp.gov.cn/fr/login.aspx'
    login_url = 'http://cpzjwyy.bjchp.gov.cn/fr/main.aspx'
    checkimg_url = 'http://cpzjwyy.bjchp.gov.cn/common/CheckImage.aspx'
    fqgm_url = 'http://cpzjwyy.bjchp.gov.cn/fr/revform.aspx?l=0&b=24'
    checkimgPath = 'checknum.jpg'
    def login(self):
        result = self.web.brower(self.first_url)
        print '打开登陆网页成功'
        self.parser.feed(result)
        tmpParams = self.parser.key

        loginparams = {
            '__EVENTTARGET':tmpParams['EVENTTARGET'],
            '__EVENTARGUMENT':tmpParams['EVENTARGUMENT'],
            '__LASTFOCUS':tmpParams['LASTFOCUS'],
            '__VIEWSTATE:':tmpParams['VIEWSTATE'],
            '__EVENTVALIDATION':tmpParams['EVENTVALIDATION'],
            'RadioButtonList1':'1',
            'txtUsername':'612726198611070010',
            'txtPassword':'860413',
            'txtCheckcode':'1111',
            'btnlogin':r'登录',
        }
        self.getCheckNum()

        result = self.web.brower(self.login_url,loginparams)
        if result.__contains__('欢迎使用昌平区房产权属登记中心网上预约系统'):
            print '登录成功'


    def fqgm(self):
        result = self.web.brower(self.fqgm_url)
        if result.__contains__('登录预约平台'):
            print '登录'+self.fqgm_url+' error'
        else:
            print '登录'+self.fqgm_url+' success'

    def getCheckNum(self):
        cn = CheckNum()
        self.web.dlFile(self.checkimg_url, self.checkimgPath)

        checkNum = cn.getCheckNum(self.checkimgPath)
        print checkNum
        return checkNum


def run():
    cpjw = CPJW()
    cpjw.login()
    cpjw.fqgm()


if __name__ == '__main__':
    run()
