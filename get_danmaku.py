# -*- encoding: utf-8 -*-
import requests
import re
import sys
import json
import time
import datetime

aid='44625717' #就是av号
page=0 #我们一般说的“第xP”里的“x”就是这个值
date_start='2019-02-25' #起止日期
date_end='2019-03-01'
cookie_header={
    'Cookie': #填一个你的登录Cookie上去，隐私相关，注意不要泄露
    }

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
                    data_split = data[i].split(',') #浮点值秒数转整数的分和秒
                    second = int(float(data_split[0]))
                    minute = int(second/60)
                    second %= 60

                    mode = int(data_split[1])
                    size = int(data_split[2])
                    color = hex(int(data_split[3]))
                    submit_time = time.localtime(int(data_split[4])) #Unix格式时间转换成一般格式
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

    print('Getting cid...')
    cid = str(bilibili.video.get_cid(aid, page))
    print('Getting danmaku list...')
    all_danmaku = bilibili.video.danmaku.getall(date_start,date_end,cid,cookie_header)
    print(len(all_danmaku),'in total from',str(date_start),'to',str(date_end))
    all_danmaku.sort(key=lambda i:i['row'])
    print('Saving data...')
    with open('av'+aid+'_'+str(date_start)+' to '+str(date_end)+'.json','w',encoding='utf-8') as jfile:
        json.dump(all_danmaku, jfile,
            ensure_ascii=False,
            sort_keys=False,
            indent=2,
            separators=(',', ': ')
            )
    print('Finished')