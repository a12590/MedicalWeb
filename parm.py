#coding=utf-8

import urllib
import json #simplejson
from bs4 import BeautifulSoup

def get_content_from_keyword(keyword='鞋子',page=1):
    """
    根据页数和keywords采集内容
    """

    params = {'keyword':keyword,'page':page,'area':1,'enc':'utf-8'}
    data = urllib.urlencode(params)
    opener =  urllib.urlopen('http://search.jd.com/s.php?'+data)
    response = opener.read()
    opener.close()
    return response.decode('gbk').encode('utf-8')


def get_price_from_ids(*ids):
    '''
    [123,42,5,678,9123123]

    根据id采集到价格
    '''
    params = {'skuIds':','.join(['J_%s'%id for id in ids]),'type':1}
    data = urllib.urlencode(params)
    opener = urllib.urlopen('http://p.3.cn/prices/mgets?'+data)
    response = opener.read()
    opener.close()
    return json.loads(response)


if __name__ == "__main__":

    '''
    分析数据，生成干净的数据 res
    '''

    content = get_content_from_keyword(keyword="鞋子",page=4)
    soup = BeautifulSoup(content)
    mids = soup.find_all(sku=True)
    ids = [mid['sku'] for mid in mids]
    prices = get_price_from_ids(*ids)

    res = []
    for mid in mids:
        data = {}
        data['id'] = mid['sku']
        data['img'] =  mid.find('img')['data-lazyload']
        aobj = mid.find(class_ = 'p-name').find('a')
        data['url'] = aobj['href']
        data['title'] = aobj.text.strip()
        data['price'] = filter(lambda price:price['id'] == 'J_%s'%data['id'] ,prices)[0]['p']
        res.append(data)

    print res
