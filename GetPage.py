# coding=utf-8
# usr/bin/eny python
import httplib
import urllib2
import requests
from lxml import etree
from bs4 import BeautifulSoup
import uniout
import re
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

'''
获取每个药物类型标签下有多少页内容  (没有输入，输出字典)
'''
class theme_page(object):
    def __init__(self):
        self.tags = [u"乙肝", u"肝纤维化", u"胆结石", u"胆囊炎", u"脂肪肝", u"肝硬化", u"黄疸", u"肝腹水", u"丙肝", \
                     u"肝性脑病", u"保肝护肝", u"免疫调节", u"肺癌", u"肝癌", u"胃癌", u"食道癌", u"结肠癌", u"肾癌", \
                     u"白血病", u"鼻咽癌", u"甲状腺", u"癌胰腺癌", u"乳腺癌", u"宫颈癌", u"卵巢癌", u"前列腺癌", u"淋巴瘤", \
                     u"膀胱癌", u"补充营养", u"缓解放化疗副作用", u"改善晚期肿瘤患者食欲和恶病质", u"缓解癌痛", u"痤疮(青春痘)",\
                     u"疤痕(瘢痕)", u"白癜风", u"银屑病（牛皮癣）", u"皮炎湿疹", u"疱疹", u"尖锐湿疣", u"灰指甲", u"黄褐斑", u"红斑狼疮", \
                     u"癣症/脚气", u"淋病梅毒", u"皮肤瘙痒", u"荨麻疹", u"扁平疣", u"过敏",u"癫痫", u"痴呆", u"帕金森", u"中风", u"偏头痛", \
                     u"神经性疼痛", u"小儿脑瘫", u"神经损伤", u"神经衰弱", u"偏瘫",u"抑郁症", u"焦虑症", u"精神分裂症", u"强迫症",\
                     u"睡眠障碍(失眠)", u"小儿多动症", u"烟草依赖",u"哮喘", u"支气管炎", u"咽喉炎", u"肺结核", u"扁桃体炎", u"呼吸道感染",\
                     u"痔疮", u"胃/十二指肠溃疡", u"反流性食管炎", u"结肠炎", u"卓-艾综合征（胃泌素瘤）", u"便秘腹泻", u"慢性胃炎", \
                     u"消化不良", u"克罗恩病",u"风湿病", u"骨关节炎", u"骨质疏松", u"类风湿性关节炎", u"骨质增生", u"痛风", u"跌打损伤",\
                     u"颈椎病", u"股骨坏死", u"腰肌劳损", u"强直性脊柱炎",u"坐骨神经痛", u"冠心病", u"心律失常", u"高血压", u"高血脂", \
                     u"心肌炎", u"心绞痛", u"脑血栓", u"心律失常", u"动脉粥样硬化", u"肾炎", u"肾结石", u"尿毒症", u"慢性肾功能不全",\
                     u"尿路感染", u"尿频尿急", u"尿路结石", u"阳痿早泄", u"少精无精", u"前列腺炎", u"前列腺增生", u"脱发少发", u"温肾壮阳", \
                     u"滋阴补肾", u"滋补肝肾", u"健脾补肾", u"益气健脾", u"综合滋补", u"盆腔炎", u"阴道炎", u"宫颈炎", u"保胎助孕", u"白带异常",\
                     u"月经不调", u"乳腺增生", u"子宫肌瘤", u"痛经", u"更年期综合症", u"小儿感冒", u"小儿厌食症", u"小儿支气管炎", u"小儿腹泻", \
                     u"驱虫", u"痱子湿疹", u"小儿低钙", u"风寒感冒", u"风热感冒", u"流行性感冒（流感）", u"解热镇痛", u"湿热上火", u"暑湿感冒",\
                     u"中暑", u"成人退烧", u"小儿退烧", u"物理降温/退热贴", u"止咳", u"祛痰", u"平喘", u"半夜咳重", u"久咳不止", u"伴便秘口臭",\
                     u"口服药", u"牙膏", u"散剂", u"含漱液", u"增强免疫力", u"腹痛", u"消化不良", u"胃酸过多", u"腹泻", u"便秘", u"蚊虫叮咬",\
                     u"痤疮（青春痘）", u"疤痕", u"痱子", u"皮肤过敏", u"脚气", u"花斑癣（汗斑）", u"头屑", u"创口护理", u"烧伤烫伤", u"肌肉酸痛", \
                     u"关节疼痛", u"扭伤", u"牙痛", u"头痛", u"关节疼痛", u"肌肉酸痛", u"神经痛", u"痛经", u"晕车药", u"外用药"
                     ]
        # self.tags = [u"胆囊炎"]

    def get_total_num(self):
        tags = self.tags
        total_num = []
        list = []
        for tag in tags:
            # print(tag)   #主题名称
            re_url = 'http://search.360kad.com/?Pagetext={}'.format(urllib2.quote(tag.encode('utf8')))
            # print(re_url)     # 主题链接
            try :
                s = requests.get(re_url)
                contents = s.content.decode('utf-8')
            except :
                continue
            # selector = etree.HTML(contents)
            # num = selector.xpath('//*[@id="content"]/div/div[1]/div[3]/a[10]/text()')
            # numlist = selector.xpath('//div[@class="waro-cont-l"]/div[3]/div/dl/dt/div[2]/span/text()')
            soup = BeautifulSoup(contents,"html.parser")
            page = soup.find('div', "countList")
            if page:
                pagesData = page.span.get_text().encode("utf-8")
                pagesNum = int(pagesData[pagesData.find('/')+2])
            # pagesNum = re.findall(re.compile(pattern=r'1 / (.*?)'), pagesData)
            total_num.append(pagesNum)
            list.append({
                '主题' : tag.encode('utf8'),
                '总页数' : pagesNum
            })
        return list

# if __name__ == '__main__':
#     run = theme_page()
#     url = 'http://www.360kad.com/product/4212.shtml?kzone=kadsearch&pagetext=盆腔炎'
#     s = requests.get(url)
#     s = s.text.decode('utf-8')
#     # run = run.get_total_num()
#     # print(str(run).decode('string_escape'))
#     run = run.searchTest(s)
#
#     # total_num = sum(run)
#     # print(total_num)
#     print('http://search.360kad.com/?Pagetext={}'.format(urllib2.quote(u'乙肝'.encode('utf8'))))
