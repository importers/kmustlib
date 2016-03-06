#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time,sqlite3
import mysql.connector

#con=sqlite3.connect('lib_record.db')
config={'host':'127.0.0.1',#默认127.0.0.1
    'user':'root',
    'password':'root',
    'port':3306 ,#默认即为3306
    'database':'lib_record',
    'charset':'utf8'#默认即为utf8
    }
try:
  cnn=mysql.connector.connect(**config)
  con=cnn.cursor()
except mysql.connector.Error as e:
  print('connect fails!{}'.format(e))
def gci(filepath):
#遍历filepath下所有文件，包括子目录
	files = os.listdir(filepath)
	lists=[]
	dirlists=[]
	for fi in files:
		fi_d = os.path.join(filepath,fi)            
		if os.path.isdir(fi_d):
		  ([lists.append(x) for x in gci(fi)])           
		else:
		  #print os.path.join(filepath,fi_d)
		  lists.append(fi_d)
	return lists	      
#递归遍历/root目录下所有文件
def run():
	dirlist=gci('.')
	for i in dirlist:
		if cun(i)==None:
			print '--------%s-empty!!!------------\r\n'%i
			continue
		else:
			print '--------%s-start!!!------------\r\n'%i
			numfind(i)
			stu_id=i[-23:-11]
			# stu_id,record_datas=cun(i)
			save_num(stu_id,numfind(i))	
		time.sleep(3)
def numfind(path):
	files=open(path,'r')
	record=[]
	#'还书 03001852209 超级记忆力训练．Ⅱ (美) 哈里·洛拉尼著 B842.3/57:2 呈贡三层中文图书藏阅区 中文图书 2015-03-28'
	rege='([借|还]{1}书).*?(\\d{11}).*?(\\d{4}-\\d{2}-\\d{2})'
	rec=re.compile(rege,re.S)
	data=re.findall(rec,files.read())
	print '----------------'
	for i in data:
		record.append([y for y in i])
	return record
	#records=([(stu_id,date,book_id) for date,book_id in data])

#保存数据到lib_record 数据库中
def save_num(stu_id,record_datas):
	#con=sqlite3.connect('lib_record.db')
	for i in range(len(record_datas)):
		if len(record_datas[i])<3:continue
		print '-------insert %s----%s----------'%(stu_id,i)	
		# cur=con.execute("insert into lib_record values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%\
		# (stu_id,record_datas[i][0],record_datas[i][1],record_datas[i][2],record_datas[i][3],record_datas[i][4],record_datas[i][5],record_datas[i][6],record_datas[i][7]))
		# con.commit
		cur=con.execute("insert into lib_record values('%s','%s','%s','%s')"%\
		(stu_id,record_datas[i][0],record_datas[i][1],record_datas[i][2]))
		#con.commit
	return True#cur.lastrowid

# run()	
def cun(path):
	stu_id=path[-23:-11]
	f=open(path,'r+')
	d=f.read()
	if len(d)<10: 
		f.close()
		return None
	f.close()
	#换行
	change = re.compile('借书')
	change1 = re.compile('还书')
	x = re.sub(change,"\n借书",d)
	x = re.sub(change1,"\n还书",x)
	# p=x.strip().split('\n')
	# print p[0]
	record_datas=[]
	#操作类型 条码号 题名 著者 索书号 馆藏地点 文献类型 处理时间
	for record in x.strip().split('\n'):
		record_datas.append([x for x in record[1:].strip().split(' ')])
		# for i in x.strip().split(' '):
		# 	print i
		#data=([(operation_type,barcode,title,Author,Call_Number,Collection_location,document_type,processing_time) 
	#保存数据记录到数据库
	return stu_id,record_datas
def createtable():
	con.execute('drop table lib_record')	
	con.execute('create table lib_record(stu_id char(15),operation_type char(10),barcode char(15),processing_time char(20))')	
	con.commit
	
#createtable()
run()	
	
