#coding:utf-8
#!/usr/bin/env python

import itchat
import jieba
import math
import numpy as np
import os
from os import listdir
import random
import matplotlib.pyplot as plt

from wordcloud import WordCloud, ImageColorGenerator

import PIL.Image as Image


#����ϵͳ�����ַ�����г��룬����ͨ����enableCmdQR��ֵΪ�ض��ı������е���
#Xshell�ͻ�������Ҫ���������С<10,����ΪCourier, ��ɫ����
itchat.auto_login(enableCmdQR=1)

if not os.path.isdir('img'):
	os.mkdir("img")

def getFriendHeadImg():
	num = 0
	friends = itchat.get_friends(update=True)[0:]

	for f in friends:
		img = itchat.get_head_img(userName=f["UserName"])
		fileImage = open("img/" + str(num) + ".jpg",'wb')
		fileImage.write(img)
		fileImage.close()
		num += 1

def createJointImg():
	x = 0
	y = 0

	pics = listdir("img")
	random.shuffle(pics)

	toImage = Image.new('RGBA', (640, 640))
	eachsize = int(math.sqrt(float(640 * 640) / len(pics)))
	numline = int(640 / eachsize)

	for i in pics:
		try:
			img = Image.open("img/" + i)
		except IOError:
			print("Error: û���ҵ��ļ����ȡ�ļ�ʧ��")
		else:
			#��СͼƬ
			img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
			#ƴ��ͼƬ
			toImage.paste(img, (x * eachsize, y * eachsize))

		x += 1
		if x == numline:
			x = 0
			y += 1

	toImage.save("all.jpg")

	itchat.send_image("all.jpg", 'filehelper')

def getFriendSex():
	friends = itchat.get_friends(update=True)[0:]
	sex = dict()

	for f in friends:
		if f["Sex"] == 1: #Man
			sex["man"] = sex.get("man", 0) + 1
		elif f["Sex"] == 2: #Women
			sex["women"] = sex.get("women", 0) + 1
		else:
			sex["unknown"] = sex.get("unknown", 0) + 1

	for i, key in enumerate(sex):
		plt.bar(key, sex[key])
	plt.show()

	print(sex)

def getFriendSignature():
	siglist = []
	f = open('signature.txt', 'w')
	friends = itchat.get_friends(update=True)[0:]
	for i in friends:
		name = i['RemarkName']
		nickname = i['NickName'] 
		# ����ƥ����˵�emoji���飬����emoji1f3c3��
		signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
		siglist.append(signature)

		f.write((name + "," + nickname + "," + signature +'\n').encode('UTF-8'))

	f.close()
	text = "".join(siglist)

	#�ִ�
	wordlist = jieba.cut(text, cut_all=True)
	word_space_split = " ".join(wordlist)

	#���ƴ���
	coloring = np.array(Image.open("./all.jpg"))#�Զ�����Ƶ�ͼƬ
	my_wordcloud = WordCloud(background_color="white", max_words=200,
			mask=coloring, max_font_size=60, random_state=42,
			font_path='/usr/share/fonts/truetype/droid/DroidSansFallback.ttf',scale=2).generate(word_space_split)

	my_wordcloud.to_file("wc.jpg")
	itchat.send_image("wc.jpg", 'filehelper')

	#image_colors = ImageColorGenerator(coloring)
	#plt.imshow(my_wordcloud.recolor(color_func=image_colors))
	#plt.imshow(my_wordcloud)
	#plt.axis("off")
	#plt.show()

def getChatRoom():
	#mpsList=itchat.get_chatrooms(update=True)[1:]
	mpsList = itchat.search_chatrooms(name='R')
	total=0
	for i in mpsList:
	    print(i['NickName'])
	    total=total+1

	print("Total chat room number: %d"  %total)


#getFriendHeadImg()
#createJointImg()
#getFriendSex()
#getFriendSignature()
getChatRoom()
