# coding=utf-8
# usr/bin/eny python

import urllib2
import pymysql.cursors
import requests
from bs4 import BeautifulSoup
import bs4
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class Medical(object):
    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='douban', charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql_info = "INSERT IGNORE INTO `douban_mov` VALUES(%s,%s,%s,%s,%s,%s)"

    def getHTMLText(url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""

    def fillUnivList(ulist, html):
        soup = BeautifulSoup(html, "html.parser")
        for tr in soup.find('tbody').children:
            if isinstance(tr, bs4.element.Tag):
                tds = tr('td')
                ulist.append([tds[0].string, tds[1].string, tds[3].string])

    def printUnivList(ulist, num):
        tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
        # print(tplt.format("排名","学校名称","总分",chr(12288)))
        print("{:^10}\t{:^6}\t{:^10}".format("排名", "学校名称", "总分"))
        for i in range(num):
            u = ulist[i]
            #   print(tplt.format(u[0],u[1],u[2],chr(12288)))
            print("{:^10}\t{:^6}\t{:^10}".format(u[0], u[1], u[2]))