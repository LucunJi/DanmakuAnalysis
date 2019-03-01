import json
from datetime import datetime,time
import matplotlib.pyplot as plot

def danmaku2datetimes(danmaku_dict):
	danmaku_dict.sort(key=lambda i:i['row'])
	danmaku2date_times = [[],[]]
	for i in danmaku_dict:
		date_time = datetime(i['submit_time']['year'],i['submit_time']['month'],i['submit_time']['day'],i['submit_time']['hour'])
		if date_time not in danmaku2date_times[0]:
			danmaku2date_times[0].append(date_time)
			danmaku2date_times[1].append(1)
		else:
			danmaku2date_times[1][len(danmaku2date_times[1])-1] += 1
	return danmaku2date_times

def danmaku2vidtimes(danmaku_dict, div):
	danmaku_dict.sort(key=lambda i:i['appear_time']['min']*60+i['appear_time']['sec'])
	danmaku2vid_times = [[],[]]
	for i in danmaku_dict:
		vid_time = datetime(1,1,1,1,i['appear_time']['min'],i['appear_time']['sec']//div*div)
		if vid_time not in danmaku2vid_times[0]:
			danmaku2vid_times[0].append(vid_time)
			danmaku2vid_times[1].append(1)
		else:
			danmaku2vid_times[1][len(danmaku2vid_times[1])-1] += 1
	return danmaku2vid_times

def main():
	print('Loading danmaku data...')
	danmaku_dict = []
	filename = 'av44625717_2019-02-25 to 2019-03-01'
	with open(filename+'.json','r',encoding='utf-8') as jfile:
		danmaku_dict = json.load(jfile)

	# plot.subplot(1,2,1)
	# plot.plot(*danmaku2date_times)
	# plot.gcf().autofmt_xdate()
	# plot.subplot(1,2,2)

	print('Plotting data...')
	div = 5 #每5秒的弹幕算在一起
	danmaku2vid_times = danmaku2vidtimes(danmaku_dict, div)
	plot.plot(*danmaku2vid_times,'r-o')
	plot.xlim([datetime(1,1,1,1,0,0),datetime(1,1,1,1,12,30)]) #设置X轴范围
	plot.grid(True, linestyle='-.')

	div *= 3
	plot.xticks([datetime(1,1,1,1,i//60,i%60) for i in range(0,(12*60+30)+div,div)],
		[str(time(0,i//60,i%60))[3:] for i in range(0,(12*60+30)+div,div)],rotation=60) #划分X轴
	
	print('Generating image...')
	fig = plot.gcf()
	fig.set_size_inches(18.5,10.5)#设置图片大小
	fig.savefig('plot.png')
	plot.show()

if __name__ == '__main__':
	main()