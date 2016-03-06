#coding=utf-8
import requests,re,os
from pyquery import PyQuery as pq
from lxml import etree 

class libread:
	def __init__(self,rdid):
		self.rdid=rdid
		self.cookies={}
		self.get_cookie(rdid)
	def __del__(self):
		pass	
	def get_cookie(self,rdid):
		data={'rdid':rdid,'rdPasswd':'96e79218965eb72c92a549dd5a330112'} #用户登录数据
		headers={
			'Host':'222.197.202.32',
			'Origin':'http://222.197.202.32',
			'Referer':'http://222.197.202.32/opac/reader/login',
			#'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
		url='http://222.197.202.32/opac/reader/doLogin'
		r=requests.post(url,data=data,allow_redirects=False)
		print 'cookiie---->%s' % r.cookies['JSESSIONID']
		self.cookies=dict(JSESSIONID=r.cookies['JSESSIONID'])
	def getcontent(self,page=1):
		url = 'http://222.197.202.32/opac/loan/historyLoanList'
		data={'page':page,'rows':50}
		#print self.cookies
		r = requests.get(url,cookies = self.cookies,params=data)
		return r.text.encode('utf8')
	#创建新目录
	def mkdir(self,path):
	    path = path.strip()
	    # 判断路径是否存在
	    # 存在     True
	    # 不存在   False
	    isExists=os.path.exists(path)
	    # 判断结果
	    if not isExists:
	        # 如果不存在则创建目录
	        print u"新建了名字叫做",path,u'的文件夹'
	        # 创建目录操作函数
	        os.makedirs(path)
	        return True
	    else:
	        # 如果目录存在则不创建，并提示目录已存在
	        print u"名为",path,u'的文件夹已经创建成功'
	        return False	
	def findsave(self,data,name,path):
		v_source=pq(data) 
		paths='./%s'%path
		self.mkdir(paths)
		file=open('%s/%s_%s.txt'%(paths,self.rdid,name),'a')	
		#print v_source('table').find('td').text().encode('utf8')
		for i in v_source('table').find('tr'):
			# print u'------这是-------'
			# print pq(i).text().encode('utf-8')
			# print '\r\n'
			file.write(pq(i).text().encode('utf8'))
		file.close()
	def recored(self,data):
		if data==None:
			return None
		rege='<span class=\"disabled\">总共 (\\d+) 条记录数<\/span>'
		rename='欢迎您：(.*?)&nbsp;'
		rec=re.compile(rege,re.S)
		ren=re.compile(rename,re.S)
		recs=int(re.findall(rec,data)[0])
		renn=re.findall(ren,data)[0]
		print renn
		nums=recs/50
		if	recs>nums*50:
			nums+=1				
		return nums,renn
		#print v_recored('span').find('disabled')
	def run(self,path):
		nums,name=self.recored(self.getcontent('1'))
		#print name.decode('utf8')
		for i in range(nums):
			print '%s的第%d页'%(self.rdid,i+1)
			data=self.getcontent(i+1)	
			self.findsave(data,name.decode('utf8'),path)
