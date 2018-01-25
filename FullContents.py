# coding=utf-8
# usr/bin/eny python

# 字段包括： 商品编码(product_number) 商品名称(product_name) 通用名称（common_name） 药品类型(medicine_type)  剂型(dosage_form)
# 商品原价(original_price) 商品售价(sold_price) 包装规格(packing_specifications) 批准文号(approval_Number) 生产厂商(manufacturer)
# 库存状态(inventory_status) 有效期(valid_period) 适应症/功能主治（functions） 用法用量(usage_dosage)

import requests
from multiprocessing import Pool,cpu_count
import urllib2
from lxml import etree
import pymysql.cursors
from bs4 import BeautifulSoup
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
'''康爱多内容解读'''

__version__ = '0.0.1'
__author__ = 'avictory'

# tag = urllib2.quote(u''.encode('utf8'))
# url_1 = 'http://search.360kad.com/?Pagetext={}'.format(tag)

class kad(object):
    def __init__(self,*args,**kwargs):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='kad_medicine', charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql_info = "INSERT IGNORE INTO `kad_medic_prop` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def search(self,content,original_price,sold_price,inventory_status):
        '''
        爬取页面内药品信息
        '''
        try:
            lists = []
            soup = BeautifulSoup(content, "html.parser")
            header = soup.find('p', "w-dtl-snext-l").get_text()
            product_number = str(header).replace("商品编码：","")
            # print product_number
            # original_price = soup.find('span', id="saleprice_value").get_text()
            # original_price = soup.select('span[class="nophone-rspan2"]')
            # print original_price
            # sold_price = soup.find('span', "grey888 nophone-rspan3").get_text()
            # print sold_price
            # inventory_status = soup.find('span', "inf-rrzt-bule").get_text()
            # print inventory_status
            selector = etree.HTML(content)
            medicine_type = str(selector.xpath('//*[@class="wrap-dtl-nav"]/a[4]/text()')[0].strip())
            header1 = selector.xpath('//*[@class="infor-list"]/ul/li[1]/text()')[0].strip()
            product_name = str(header1).replace("商品名称：", "")
            # print product_name
            header2 = selector.xpath('//*[@class="infor-list"]/ul/li[2]/text()')[0].strip()
            packing_specifications = str(header2).replace("规格：", "")
            # print packing_specifications
            header3 = selector.xpath('//*[@class="infor-list"]/ul/li[3]/text()')[0].strip()
            manufacturer = str(header3).replace("生产企业：", "")
            # print manufacturer
            header4 = selector.xpath('//*[@class="infor-list"]/ul/li[4]/text()')[0].strip()
            common_name = str(header4).replace("通用名称：", "")
            # print common_name
            header5 = selector.xpath('//*[@class="infor-list"]/ul/li[6]/text()')[0].strip()
            valid_period = str(header5).replace("有效期：", "")
            # print valid_period
            header6 = selector.xpath('//*[@class="infor-list"]/ul/li[7]/text()')[0].strip()
            dosage_form = str(header6).replace("剂型：", "")
            # print dosage_form
            header7 = selector.xpath('//*[@class="infor-list"]/ul/li[8]/text()')[0].strip()
            approval_Number = str(header7).replace("批准文号：", "")
            # print approval_Number
            header8 = selector.xpath('//*[@class="infor-list"]/ul/li[9]/text()')[0].strip()
            functions = str(header8).replace("适应症/功能主治：", "")
            # print functions
            header9 = selector.xpath('//*[@class="infor-list"]/ul/li[10]/text()')[0].strip()
            usage_dosage = str(header9).replace("用法用量：", "")
            # print usage_dosage
            if product_number:
                lists.append({
                    '商品编码' : product_number,
                    '商品名称' : product_name,
                    '通用名称' : common_name,
                    '药品类型': medicine_type,
                    '剂型': dosage_form,
                    '商品原价': original_price,
                    '商品售价': sold_price,
                    '包装规格': packing_specifications,
                    '批准文号': approval_Number,
                    '生产厂商': manufacturer,
                    '库存状态': inventory_status,
                    '有效期' : valid_period,
                    '功能主治' : functions,
                    '用法用量' : usage_dosage,
                })
                if lists:
                    lists = lists.pop()
                else:
                    lists = u' '

                # print(lists)
                print (str(lists).decode('string_escape'))
                try:
                    self.cursor.execute(self.sql_info,(str(lists['商品编码']),str(lists['商品名称']),str(lists['通用名称']),
                                      str(lists['药品类型']),str(lists['剂型']),
                                      float(lists['商品原价']),float(lists['商品售价']),str(lists['包装规格']),str(lists['批准文号']),
                                      str(lists['生产厂商']), str(lists['库存状态']), str(lists['有效期']),str(lists['功能主治']),
                                      str(lists['用法用量'])))
                    self.conn.commit()
                except Exception as e:
                    print(e)
        except Exception as e:
            pass

    def searchURL(self, content):
        try:
            soup = BeautifulSoup(content, "html.parser")
            items = soup.find_all('div', "plist_li_i")
            sold_price = float(str(soup.find('span', "pri").get_text().encode("utf-8")).replace("￥",""))
            original_price = float(str(soup.find('p', "priceMarket").get_text().encode("utf-8")).replace("￥",""))
            inventory_status = str(soup.find('span', "kucun").get_text())
            linkList=[]
            for item in items:
                link = item.find('p', "t").a.get('href')
                linkList.append({
                    '商品原价': original_price,
                    '商品售价': sold_price,
                    '库存状态': inventory_status,
                    '链接': link
                })
            return linkList
        except Exception as e:
            print(e)

# if __name__ == '__main__':
#     run = kad()
#     url_1 = 'http://search.360kad.com/?pageText=%E7%9B%86%E8%85%94%E7%82%8E'
#     s = requests.get(url_1)
#     s = s.content.decode('utf-8')
#     urlLists = run.searchURL(s)
#     for urlList in urlLists:
#         # if urlList:
#         #     urlList = urlList.pop()
#         # else:
#         #     urlList = u' '
#         # print urlList
#         # print (str(urlLists).decode('string_escape'))
#         original_price = urlList['商品原价']
#         print original_price
#         sold_price = urlList['商品售价']
#         print sold_price
#         inventory_status = urlList['库存状态']
#         print inventory_status
#         link = urlList['链接']
#         print link
#         # for url in urlLists:
#         #     print url
