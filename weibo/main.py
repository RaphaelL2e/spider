import re
import time

import requests
from lxml import etree

from weibo.sql.mysql import insert_hot_top, HotTop


# https://weibo.com/u/6361290192
# https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6
def list_top_hot():
    top_hot_url = 'https://s.weibo.com/top/summary'
    print("start ...")
    r = requests.get(top_hot_url)

    html = etree.HTML(r.text)
    tbody = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')

    thl = []
    i = 0
    for td in tbody:
        title = td.xpath('a/text()')[0]
        relative_path = td.xpath('a/@href')[0]
        if re.match(r'^/weibo.*top$', relative_path):
            hot_num = td.xpath('span/text()')[0].split(' ')[1]
            i += 1
            t = time.strftime("%Y%m%d%H%M", time.localtime())

            obj = [i, t, title, hot_num, 'https://s.weibo.com' + relative_path]
            thl.append(obj)
    return thl


def store_top_hot():
    top_hot_list = list_top_hot()
    data = []
    for hot_top_object in top_hot_list:
        ht = HotTop()
        ht.ranking = hot_top_object[0]
        ht.issue = hot_top_object[1]
        ht.title = hot_top_object[2]
        ht.heat = hot_top_object[3]
        ht.url = hot_top_object[4]
        data.append(ht)
        print(hot_top_object)
    insert_hot_top(data=data)


if __name__ == '__main__':
    while True:
        time.sleep(600)
        store_top_hot()

