# -*- encoding: utf-8 -*-
import socket
import socks
import requests
import re
import sys
import json
import time
import datetime

aid='44625717' #这里是av号
page=0 #一般我们说的“P数”“第几P”就是这个
date_start='2019-02-25' #起止日期
date_end='2019-02-28'
cookie_header={
    'Cookie': #这里填上你的cookie，安全相关，别泄漏了
    }

def set_socks_proxy(host, port):
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, host, port)
    socket.socket = socks.socksocket

class bilibili:
    class video:
        def get_cid(aid, page):
            response = requests.get('https://api.bilibili.com/x/player/pagelist?aid='+str(aid))
            pagelist = response.json()
            cid = pagelist['data'][page]['cid']
            return cid

        class danmaku:

            def get_data(date, cid, cookie_header):
                data_out = []

                response = requests.get('https://api.bilibili.com/x/v2/dm/history?type=1&date='+str(date)+'&oid='+str(cid),headers=cookie_header)
                response.encoding = response.apparent_encoding
                xml_text = response.text

                data = re.findall('(?<=<d p=").*?(?=">)', xml_text)
                text = re.findall('(?<=">).*?(?=</d>)', xml_text)

                entry_count = 0
                for i in range(len(data)):
                    data_split = data[i].split(',') #浮点日期转换成分钟和秒
                    second = int(float(data_split[0]))
                    minute = int(second/60)
                    second %= 60

                    mode = int(data_split[1])
                    size = int(data_split[2])
                    color = hex(int(data_split[3]))
                    submit_time = time.localtime(int(data_split[4])) #Unix日期转换成一般格式
                    pool = int(data_split[5])
                    coded_uid = data_split[6]
                    rowID = int(data_split[7])

                    new_entry = {
                        'appear_time':{'sec':second,'min':minute},
                        'mode':mode,
                        'size:':size,
                        'color':color,
                        'submit_time':{
                            'year':submit_time[0],
                            'month':submit_time[1],
                            'day':submit_time[2],
                            'hour':submit_time[3],
                            'min':submit_time[4],
                            'sec':submit_time[5],
                            },
                        'pool':pool,
                        'uid':coded_uid,
                        'row':rowID,
                        'text':text[i]
                        }
                    data_out.append(new_entry)
                return data_out

            def getall(date_start, date_end, cid, cookie_header):
                data_all = []
                date_pointer = date_start
                while date_pointer <= date_end:
                    data = bilibili.video.danmaku.get_data(date_pointer, cid, cookie_header)
                    data_all.extend([i for i in data if i not in data_all])
                    date_pointer += datetime.timedelta(days=1)
                return data_all

if __name__=='__main__':
    date_start=datetime.date(*[int(i) for i in date_start.split('-')])
    date_end=datetime.date(*[int(i) for i in date_end.split('-')])

    #print('Setting proxy...') #在需要的时候打开代理，有的校园网封b站qaq
    #set_socks_proxy('127.0.0.1',1080)
    print('Getting cid...')
    cid = str(bilibili.video.get_cid(aid, page))
    print('Getting danmaku list...')
    all_danmaku = bilibili.video.danmaku.getall(date_start,date_end,cid,cookie_header)
    print('Saving data...')
    with open('av'+aid+'_'+str(date_start)+' to '+str(date_end)+'.json','w',encoding='utf-8') as jfile:
        json.dump(all_danmaku, jfile,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            separators=(',', ': ')
            )
    print('Finished')