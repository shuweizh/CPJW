#! /usr/bin/env python
# coding:utf-8

import urllib2
import cookielib
from os import path

import pytesseract
from PIL import Image
from PIL import ImageEnhance


#####################################################

class CheckNum:
    # 由于都是数字
    # 对于识别成字母的 采用该表进行修正
    rep = {'O':'0', 'I':'1', 'L':'1', 'Z':'2', 'S':'8', '?':'9'}

    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)


    def get_file(self,url):
        try:
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

            req = urllib2.Request(url)
            operate = opener.open(req)
            data = operate.read()
            return data
        except BaseException, e:
            print e
            return None


    '''
    保存文件到本地

    @path  本地路径
    @file_name 文件名
    @data 文件内容
    '''


    def save_file(self, file_name, data):
        if data == None:
            return

        file = open(file_name, "wb")
        file.write(data)
        file.flush()
        file.close()



    def getverify1(self, name):
        # 打开图片
        im = Image.open(name)
        # 切割
        #im = im.crop((6, 5, 40, 16))
        # 转化到灰度图
        imgry = im.convert('L')
        # 保存图像
        imgry.save(path.join(path.dirname(name), '1g'+path.basename(name)))
        # 二值化，采用阈值分割法，threshold为分割点
        out = imgry.point(self.table, '1')
        out.save(path.join(path.dirname(name), '1b'+path.basename(name)))
        out1=out.load()

        # 9宫格计算,去噪
        w = im.size[0]
        h = im.size[1]
        for x in range(w):
            for y in range(h):
                if self.sum_9_region(out, x, y) < 3:
                    out1[x,y]=1
                else:
                    out1[x,y]=0
        out.save(path.join(path.dirname(name), '19b'+path.basename(name)))
        #out1.save('b' + name)


        # 识别
        #text = pytesseract.image_to_string(out,config='-tessedit_char_whitelist=0123456789')
        text = pytesseract.image_to_string(out)
        # 识别对吗
        text = text.strip()
        text = text.upper()
        for r in self.rep:
            text = text.replace(r, self.rep[r])
        text = filter(lambda ch: ch in '0123456789', text)
            # out.save(text+'.jpg')
        return text

    def getverify2(self, name):
        # 打开图片
        im = Image.open(name)
        # 切割
        #im = im.crop((5 , 4, 41, 17))
        # 转化到灰度图
        imgry = im.convert('L')
        # 保存图像
        #imgry.save('g' + name)
        # 二值化，采用阈值分割法，threshold为分割点
        out = imgry.point(self.table, '1')
        out.save(path.join(path.dirname(name), '2g'+path.basename(name)))

        pixdata = im.load()
        pixdata_ry = out.load()
        width=im.size[0]
        hight=im.size[1]

        for x in range(width):
            for y in range(hight):
                r,g,b=pixdata[x,y]
                if r>(g+b)*1.1:
                    pixdata_ry[x,y] = 0
                else:
                    pixdata_ry[x, y] = 1
        out.save(path.join(path.dirname(name), '2b'+path.basename(name)))
        out1 = out.load()

        # 9宫格计算,去噪
        w = im.size[0]
        h = im.size[1]
        for x in range(w):
            for y in range(h):
                if self.sum_9_region(out, x, y) < 3:
                    out1[x, y] = 1
                else:
                    out1[x, y] = 0
        out.save(path.join(path.dirname(name), '29b'+path.basename(name)))
        # 识别
        #text = pytesseract.image_to_string(out,config='-tessedit_char_whitelist=0123456789')
        text = pytesseract.image_to_string(out)
        # 识别对吗
        text = text.strip()
        text = text.upper()
        for r in self.rep:
            text = text.replace(r, self.rep[r])
        text = filter(lambda ch: ch in '0123456789', text)

        return text

    def sum_9_region(self, img, x, y):
        """
        9邻域框,以当前点为中心的田字框,黑点个数
        :param x:
        :param y:
        :return:
        """
        # todo 判断图片的长宽度下限
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height

        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0

        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 4 - sum
            elif x == width - 1:  # 右上顶点
                sum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))

                return 4 - sum
            else:  # 最上非顶点,6邻域
                sum = img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 6 - sum
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = cur_pixel \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x, y - 1))
                return 4 - sum
            elif x == width - 1:  # 右下顶点
                sum = cur_pixel \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y - 1))

                return 4 - sum
            else:  # 最下非顶点,6邻域
                sum = cur_pixel \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x + 1, y - 1))
                return 6 - sum
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))

                return 6 - sum
            elif x == width - 1:  # 右边非顶点
                # print('%s,%s' % (x, y))
                sum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))

                return 6 - sum
            else:  # 具备9领域条件的
                sum = img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 9 - sum
    def getCheckNumByUrl(self,url):
        filePath = "checknum.jpg"
        self.save_file(filePath, self.get_file(url))
        self.getCheckNum(filePath)

    def getCheckNum(self,filePath):
        r1 = self.getverify1(filePath)
        print '验证码-F1:',r1
        r2 = self.getverify2(filePath)
        print '验证码-F2:', r2
        r=''
        if len(r1) != len(r2) and len(r1)==4:
            r = r1
        else:
            r = r2
        print '验证码-R:', r
        return r





if __name__ == '__main__':
    #run()
    url='http://cpzjwyy.bjchp.gov.cn/common/CheckImage.aspx'

    cn = CheckNum()
    cn.getCheckNumByUrl(url)
