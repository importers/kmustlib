#!/usr/bin/python
# -*- coding: utf-8 -*- 
import re
a = "这是个中文不是"
#b = re.compile(u"[\u4e00-\u9fa5]{1,2}")
b = re.compile("[这|不]{1}是")

c = b.findall(a)
for i in  c:
    print i