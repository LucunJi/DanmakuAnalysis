from wordcloud import WordCloud,STOPWORDS
import jieba
import json
import re

print('Loading danmaku data...')
danmaku_dict = []
filename = 'av44625717_2019-02-25 to 2019-03-01' #文件名喽
with open(filename+'.json','r',encoding='utf-8') as jfile:
	danmaku_dict = json.load(jfile)
word_split = ''

print('Processing data...')
jieba.add_word('大鱼海棠')
jieba.del_word('大鱼')
jieba.del_word('海棠')

jieba.add_word('服务器') #“服务器”是一个完整词语
jieba.del_word('服务')
jieba.del_word('务器')

jieba.del_word('不是') #这些词代表的意思有点杂，而且观赏性不是很好
jieba.del_word('就是')
jieba.del_word('这个')
jieba.del_word('什么')
jieba.del_word('一个')
jieba.del_word('一般')

for i in danmaku_dict:
	word = ' '.join(jieba.cut(i['text'],cut_all=True))
	word_split = ' '.join([word_split,word])

print('Generating wordcloud image...')
wc = WordCloud(
	width = 1920,
	height=1080,
	font_path='C:\\Windows\\Fonts\\simhei.ttf', #一定要加个中文字体，否则显示不出来
	stopwords=['mc','服务器','游戏','世界'], #这几个词意义相对不大
	collocations=False,
	prefer_horizontal=1 #文字统一横排
	).generate(word_split)
wc.to_file(filename+'.png')