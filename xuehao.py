#coding=utf-8
'''实现功能：去除重复的qq号码 保存到num_qq_distinct,txt中'''
filename='xuehao.txt'

f=open(filename)
wc={}
for i in f:
	j=i[0:10]
	print j
	wc.setdefault(j,0)
	wc[j]+=1
f.close()
save_filename='xuehao_distinct.txt'
w_qq=open(save_filename,'a+')	
for qq in wc.keys():
	w_qq.write(qq+'\t')
w_qq.close()	
print u'%s去重写入成功！'%filename