# coding=utf-8
# usr/bin/eny python
import httplib

from GetPage import theme_page
from FullContents import kad
from Medcontent import Medical
from multiprocessing import Pool,cpu_count
import threading
import urllib2
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

page_infos = theme_page()
page_infos = page_infos.get_total_num()    # 主题&页数
# pool = Pool(cpu_count())
run = kad()

for page_info in page_infos:   # 遍历所有主题
    tags = page_info['主题']
    page = page_info['总页数']
    tag = urllib2.quote(tags.encode('utf8'))
    threads = []
    for i in range(int(page)):    # 每个主题下的所有页数
        url = 'http://search.360kad.com/?Pagetext={0}&pageIndex={1}'.format(tag,i)
        s = ""
        try:
            s = requests.get(url)
            s = s.content.decode('utf-8')
        except :
            continue
        Lists = run.searchURL(s)
        if Lists  is not None :
            for list in Lists:
                original_price = list['商品原价']
                sold_price = list['商品售价']
                inventory_status = list['库存状态']
                url = list['链接']
                try:
                    s = requests.get(url)
                    s = s.content.decode('utf-8')
                except :
                    continue
                lists = run.search(s,original_price,sold_price,inventory_status)
        print('--------------------------------------------------------------')
        time.sleep(1)
