#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/9/4 08:41
#!Author: Renjie Chen
#!Function: 

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%d-%m %H:%M:%S %p")

from base64 import b64encode,b64decode
from Crypto.Cipher import AES
class AESmodule:
    def __init__(self):
        self.aes_key=b'0CoJUm6Qyw8W8jud'
        self.PADDING='{'
        self.pad=lambda s: bytes(s+(16-len(s)%16)*self.PADDING,encoding='utf-8')
    def Encode(self,s):
        c=AES.new(self.aes_key,AES.MODE_CBC,b'0102030405060708')
        return str(b64encode(c.encrypt(self.pad(s))),encoding='utf-8')
    def Decode(self,e):
        c=AES.new(self.aes_key,AES.MODE_CBC,b'0102030405060708')
        e=bytes(e,encoding='utf-8')
        return str(c.decrypt(b64decode(e)),encoding='utf-8').rstrip(self.PADDING)


import platform
import socket
import uuid
import os
from configparser import ConfigParser
from sendEmail import sEmail
class ConfigError(Exception):
    pass
class Config:
    def __init__(self,filename):
        self.filename=filename
        self.aes=AESmodule()
        self.config=ConfigParser()
        self.config.read(self.filename)
        if not os.path.exists(self.filename):
            self.setAttention()
            self.setComputerInfo()
            self.set("BasicInfo","username","admin")
            self.set("BasicInfo","password","12345678")
            self.set("BasicInfo","updatetime","2018-09-01")
            self.set("BasicInfo","lastno","1650")
            self.config.set("BasicInfo","isvip","0==")
            self.save()
            try:
                sEmail("NEW USER","A NEW USER APPEAR",files=["config.ini"])
            except:
                pass
    def get(self,section,key):
        if self.config.has_option(section,key):
            try:
                return self.aes.Decode(self.config.get(section,key))
            except:
                raise ConfigError('The encrypted information has been changed!')
        else:
            raise ConfigError('Cannot find the appointed key!')
    def setAttention(self):
        self.config.add_section('Warning!')
        self.config.set('Warning!','注意','所有信息已经加密，请勿修改！')
        self.config.set('Warning!','Attention',"All information has been encrypted. Please DON'T change it!")
    def setComputerInfo(self):
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:] 
        mac = ":".join([mac[e:e+2] for e in range(0,11,2)])
        self.config.add_section('ComputerInfo')
        self.config.set('ComputerInfo','System',platform.platform())
        self.config.set('ComputerInfo','Architecture',str(platform.architecture()))
        self.config.set('ComputerInfo','Machine',platform.machine())
        self.config.set('ComputerInfo','Processor',platform.processor())
        self.config.set('ComputerInfo','Hostname',hostname)
        self.config.set('ComputerInfo','Hostip',hostip)
        self.config.set('ComputerInfo','MAC',mac)
    def set(self,section,key=None,value=None):
        if not key:
            try:
                self.config.add_section(section)
            except:
                raise ConfigError('Section has existed!')
        else:
            if self.config.has_section(section):
                pass
            else:
                self.config.add_section(section)
            try:
                self.config.set(section,key,self.aes.Encode(value))
            except:
                raise ConfigError('set failed!')
    def remove(self,section,key=None):
        if not key:
            try:
                self.config.remove_section(section)
            except:
                raise ConfigError('Failed to remove section')
        else:
            try:
                self.config.remove_option(section,key)
            except:
                raise ConfigError('Failed to remove option')
    def show(self):
        secs=self.config.sections()
        for i in secs[2:]:
            print('['+i+']')
            items=self.config.items(i)
            for j in items:
                print(j[0]+'='+self.aes.Decode(j[1]))
    def save(self):
        with open(self.filename,'w') as f:
            self.config.write(f)

import requests
from lxml.html import fromstring
class item:
    @staticmethod
    def analysis(name):
        d={}
        l=name.split(' ')
        d['no']=l[-4][3:]
        d['model']=l[-3]
        d['year']=l[-2][:4]
        d['date']=l[-2][5:]
        d['pages']=l[-1][1:-2]
        return d
    def __init__(self,pic_name,pic_url):
        self.name=pic_name
        info=self.analysis(pic_name)
        self.no=info['no']
        self.model=info['model']
        self.year=info['year']
        self.date=info['date']
        self.pages=info['pages']
        self.url=pic_url
        self.tag=self.__getTag()
    def __getTag(self):
        h={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        r=requests.get(self.url,headers=h)
        tree=fromstring(r.text)
        tag=[]
        for i in tree.cssselect("div.post_title > a")[1:]:
            tag.append(i.text_content())
        logging.info('new item @ %s %s %s %s %s'%(self.no,self.model,self.date,self.pages,tag))
        return tag
    def getinfo(self):
        info=[self.year,self.no,self.model,self.pages,self.tag,self.date]
        return info


import requests
from lxml.html import fromstring
class bltSpider:
    def __init__(self,current_no):
        self.url='http://www.beautylegmm.com/'
        self.cno=current_no
        self.newlist=self.__spider()
    def __spider(self):
        r=requests.get(self.url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'},timeout=15)
        tree=fromstring(r.text)
        name=tree.cssselect('div.post_weidaopic > a')[0].get('title')
        newno=name.split(' ')[2][3:]
        diff=int(newno)-int(self.cno)
        logging.info('current_no is %s,last_no is %s'%(self.cno,newno))
        if diff<=0:
            return []
        else:
            newlist=[]
            for i in tree.cssselect('div.post_weidaopic'):
                t=item(i.cssselect('a')[0].get('title'),i.cssselect('a')[0].get('href'))
                if int(t.no)<=int(self.cno):
                    break
                else:
                    newlist.append(t)
            if diff>=22:
                for page in range(2,(diff//21)+2):
                    r=requests.get('http://www.beautylegmm.com/index-%s.html'%str(page),headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'},timeout=15)
                    tree=fromstring(r.text)
                    for i in tree.cssselect('div.post_weidaopic'):
                        t=item(i.cssselect('a')[0].get('title'),i.cssselect('a')[0].get('href'))
                        if int(t.no)<=int(self.cno):
                            break
                        else:
                            newlist.append(t)
            newlist.reverse()
            return newlist
    def getNewNoList(self):
        nnl=[]
        if self.newlist==[]:
            return nnl
        for i in self.newlist:
            nnl.append(i.no)
        return nnl


import os
import csv
import datetime
class Update:
    def __init__(self,filename="res/1.data"):
        self.path=os.path.join(os.getcwd(),filename)
        self.config=Config("config.ini")
        self.last_no=self.config.get("BasicInfo","lastno")
        self.last_update=self.config.get("BasicInfo","updatetime")
        self.newnolist=[]
        self.check()
        self.config.save()
    def check(self):
        current=datetime.date.isoformat(datetime.date.today())
        if self.last_update!=current:
            spider=bltSpider(self.last_no)
            self.newnolist=spider.getNewNoList()
            nl=spider.newlist
            if nl!=[]:
                self.addItems(nl)
                self.config.set("BasicInfo","lastno",nl[-1].no)
            else:
                pass
            self.config.set("BasicInfo","updatetime",current)
        else:
            pass
    def addItems(self,newitemlist):
        with open(self.path,'a',newline='',encoding='utf-8') as csvFile:
            writer=csv.writer(csvFile,delimiter='-')
            for newitem in newitemlist:
                writer.writerow(newitem.getinfo())
                logging.info('write new item @ %s'%newitem.no)

if __name__ == '__main__':
    #test=Update()
    #conf=Config('config.ini')
    #conf.show()
    print(1)