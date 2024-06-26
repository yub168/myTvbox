# -*- coding: utf-8 -*-

import requests
import json
import ast
import re
import json5
import datetime
import base64
from Crypto.Cipher import AES



def FindResult(content,key):
  if isJson(content):
    return content
  pattern = re.compile(r"[A-Za-z0]{8}\*\*")
  result = pattern.search(content) 
  #print(content.index(result.group()))
  try:
    if result:
      content = content[content.index(result.group()) + 10:]
      data=base64.b64decode(content).decode('utf-8')
      #print(data)
      return data
    if content.startwith('2423'):
      return None
    elif key and isJson(content):
      aes = AES.new(key,AES.MODE_ECB)
      return aes.decrypt(content)
  except Exception as e:
    return None
  
def isJson(content):
  try:
    data=json5.loads(content)
    return True
  except Exception as e:  
      print(e)
      return False
  
def getConfig(list):
  headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
  configList={}
  for key,value in list.items():
    try:
      r=requests.get(value,headers=headers, timeout=3.0)
      if r.status_code==200:
        r.encoding='utf-8'
        jsonText=FindResult(r.text,'')
        data=json5.loads(jsonText)
        configList[key]=data
    except requests.exceptions.RequestException as e:  
      print(e)
  return configList
def setConfig(configList):
  # 配置主体内容
  print('设置主配置',list(configList.keys()))
  
  if 'fatCat' in configList:
    customConfig=configList['fatCat']
  elif '饭太硬' in configList:
    customConfig=configList['饭太硬']
  elif 'OK佬' in configList:
    customConfig=configList['OK佬']
  elif '香雅情' in configList:
    customConfig=configList['香雅情']
  elif '道长' in configList:
    customConfig=configList['道长']
  return customConfig
  # 给主体添加部分site

def setParise(customConfig,configList):
  print('设置解析')
  if customConfig :
    # 提取解析parses
    parses=[]
    if '香雅情' in configList and not parses:
      parses=configList['香雅情']['parses']
      customConfig['parses']=parses
    if 'OK佬' in configList and not parses:
      parses=configList['OK佬']['parses']
      customConfig['parses']=parses
    

def setLives(customConfig,configList):
  # 提取lives
  print('设置直播')
  proxy='https://mirror.ghproxy.com/'
  url='https://mirror.ghproxy.com/github.com/yub168/myTvbox/raw/master/live.txt'
  lives=[]
  if 'mi' in configList and not lives:
    print('lives 配置为 mi')
    lives=configList['mi']['lives']
  if 'OK佬' in configList and not lives:
    print('lives 配置为 OK佬')
    lives=configList['OK佬']['lives']
    
  if lives:
    liveUrl=lives[0].get('url')
    if liveUrl:
      if '127.0.0.1:9978/proxy' in liveUrl:
        liveUrl=liveUrl.split('url=')[1]
      response = requests.get(liveUrl)
      # 检查请求是否成功
      if response.status_code == 200:
          # 获取响应内容
          data = response.text
          # 打开文件进行写入
          with open('./live.txt', 'w',encoding='utf-8') as file:
              file.write(data)
          #print('数据已保存到 live.txt')
          lives[0]['url']=url
          customConfig['lives']=lives
      else:
          print('请求失败，状态码:', response.status_code)
    else:
      print('没有live地址！')

def saveConfig(customConfig):
  
  if customConfig:
  # 配置customConfig及写入文件
    print('保存配置')
    with open("./config.json", "w",encoding='utf-8') as file:
      # 使用json.dump将数据写入文件
      print('抓取时间：\t',datetime.datetime.now())
      json.dump(customConfig,file,ensure_ascii=False)

def testInterface(url):
  headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
  try:
      r=requests.get(url,headers=headers, timeout=3.0)
      if r.status_code==200:
        r.encoding='utf-8'
        jsonText=FindResult(r.text,'')
        data=json5.loads(jsonText)
        print(data)
  except requests.exceptions.RequestException as e:  
      print(e)

def start():
  list={
  'fatCat':'http://like.肥猫.com/你好',
  '饭太硬':"http://www.饭太硬.com/tv",
  'mi':"http://mi.xxooo.shop",
  "王小二":"http://tvbox.xn--4kq62z5rby2qupq9ub.xyz/",
  '道长':'https://pastebin.com/raw/5NHaxyGR',
  '香雅情':'https://ghproxy.net/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json',
  'OK佬':'http://ok321.top/tv',
  }
  
  configList=getConfig(list)
  customConfig=setConfig(configList)
  setLives(customConfig,configList)
  setParise(customConfig,configList)
  saveConfig(customConfig)

if "__name__==__main__":
  # url='http://ok321.top/tv'
  # testInterface(url)
  start()

