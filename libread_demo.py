import time
from kmustlib import libread
xu=([xc.split('\t') for xc in open('xuehao_distinct.txt')])
for inf in xu:
	for ix in inf: 
		ixx=ix+'01'
		print '------>>>start---%s-<<<<<<<<----'%ixx
		xuehao=([int(ixx)+x for x in range(60)])
		for xy in xuehao:
			try:
				lread=libread(xy)
				lread.run(ixx)
			except:
				
				continue
		time.sleep(5)	
#for xy in xuehao:
	#try:
# lread=libread('201210402125')
# lread.run('text')
	#except:
		
	#	continue		