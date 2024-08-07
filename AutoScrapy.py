# -*- coding: utf-8 -*-

import requests
import json
#import ast
import re
import json5
import datetime
import base64
from Crypto.Cipher import AES
# import commentjson
# import jsonpickle
# import ujson
# import demjson3
import orjson

def encodeBase64(content):
  content='**'+base64.b64encode(content.encode('utf-8')).decode('utf-8')
  print(content)
  return content

def FindResult(content,key=None):
  if isJson(content):
    return content
  pattern = re.compile(r"[A-Za-z0]{8}\*\*")
  result = pattern.search(content) 
  if result:
    try:
        #print(result.group())
        #print(content.index(result.group()))
        content = content[content.index(result.group()) + 10:]
        data=base64.b64decode(content).decode('utf-8')
        #print(data)
        return data
    except Exception as e:
      return None
  if content.startswith('**'):
    try:
        #print(result.group())
        #print(content.index(result.group()))
        content = content[2:]
        data=base64.b64decode(content).decode('utf-8')
        #print(data)
        return data
    except Exception as e:
      return None
  if content.startswith('2423'):
        return None
  elif key and isJson(content):
    aes = AES.new(key,AES.MODE_ECB)
    return aes.decrypt(content)


def isJson(content):

  try:
    
    #print('json解析内容：',content)
    #data=json5.loads(remove_comments(content))
    #pattern=r'(".*?)(\r\n)+'
    #pattern=r'\r\n'
    #result=re.findall(pattern,content)
    #print("find result",result)
    #content=re.sub(pattern, r'', content)
    #data=commentjson.loads(content)
    #data = jsonpickle.decode(content)
    #data=ujson.loads(content)
    #data=demjson3.decode(content)
    data = orjson.loads(content)
    return True
  except Exception as e:  
      print('解析json错误：',e)
      return False
  
def getConfig(url):
  headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
 
  try:
    r=requests.get(url,headers=headers, timeout=3.0)
    if r.status_code==200:
      r.encoding='utf-8'
      jsonText=FindResult(r.text,'')
      #print(jsonText)
      if jsonText:
        supplementAddr(url,jsonText)
        config=json5.loads(jsonText)
        return config
  except requests.exceptions.RequestException as e:  
    print(e)
  

def getConfigs(list):
  configList={}
  for key,value in list.items():
    config=getConfig(value)
    if config:
      configList[key]=config
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
  elif 'mi' in configList:
    customConfig=configList['mi']
  elif '道长' in configList:
    customConfig=configList['道长']
  if customConfig:
    mofidyPlayType(customConfig)
  return customConfig
  # 给主体添加部分site

# 修改荐片playType 为1 （ijkplayer)
def mofidyPlayType(configs,siteKey='荐片',category='1'):
  
    for item in configs['sites']:
      #print(item)
      if siteKey in item['name']:
        item['playerType']=category
  

def setParise(customConfig,configList):
  print('设置解析')
  # if customConfig :
  #   # 提取解析parses
  #   parses=[]
  #   if '香雅情' in configList and not parses:
  #     parses=configList['香雅情']['parses']
  #     customConfig['parses']=parses
  #   if 'OK佬' in configList and not parses:
  #     parses=configList['OK佬']['parses']
  #     customConfig['parses']=parses
    

def setLives(customConfig,configList):
  # 提取lives
  print('设置直播')
  #proxy='https://mirror.ghproxy.com/'
  #url='https://mirror.ghproxy.com/github.com/yub168/myTvbox/raw/master/live.txt'
  url='http://127.0.0.1:9978/proxy?do=live&url=https://gitee.com/yub168/myTvbox/raw/master/lives.txt'
  lives=[]
  if '俊佬线路' in configList and not lives:
    print('lives 配置为 俊佬线路')
    lives=configList['俊佬线路']['lives']
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
          response.encoding='utf-8'
          data = response.text
          data=encodeBase64(data)
          # 打开文件进行写入
          with open('./lives.txt', 'w',encoding='utf-8') as file:
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


# 补充相对地址
def supplementAddr(url,config):

  # url='https://gitlab.com/duomv/dzhipy/-/raw/main/index.json'
  # config='''
  #         {
  #     "key": "hipy_js_爱看hd",
  #     "name": "爱看hd(drpy_t3)",
  #     "type": 3,
  #     "api": "./drpy_libs/drpy2.min.js",
  #     "searchable": 1,
  #     "quickSearch": 1,
  #     "filterable": 1,
  #     "order_num": 0,
  #     "ext": "./drpy_js/爱看hd.js"
  #   },
  #   {
  #     "key": "hipy_js_爱你短剧",
  #     "name": "爱你短剧(drpy_t3)",
  #     "type": 3,
  #     "api": "./drpy_libs/drpy2.min.js",
  #     "searchable": 1,
  #     "quickSearch": 1,
  #     "filterable": 1,
  #     "order_num": 0,
  #     "ext": "./drpy_js/爱你短剧.js"
  #   },
  #       '''
  host =url[:url.rfind('/')]
  #print('host:',host)
  pattern=r'"\./.*?"'
  config=re.sub(pattern,lambda x:"\""+host+x.group(0)[2:],config)
  #result=re.findall(pattern,config)
  #print(config)
  return config

def start():
  list={
  'fatCat':'http://肥猫.com/',
  '饭太硬':"http://www.饭太硬.com/tv",
  "王小二":"http://tvbox.xn--4kq62z5rby2qupq9ub.xyz/",
  '俊佬线路':'http://home.jundie.top:81/top98.json',# spider为相对地址 注意lives地址
  'PG':'https://git.acwing.com/iduoduo/orange/-/raw/main/jsm.json',
  'OK佬':'http://ok321.top/tv',
  'mi':"http://mi.xxooo.shop", # 解析josn错误
  }
  
  configList=getConfigs(list)
  customConfig=setConfig(configList)
  setLives(customConfig,configList)
  setParise(customConfig,configList)
  saveConfig(customConfig)

if "__name__==__main__":
  
  # url='http://ok321.top/tv'
  # config=getConfig(url)
  # print("config:",config)
  # lives=config['lives']
  # liveUrl=lives[0].get('url')
  # if liveUrl:
  #   if '127.0.0.1' in liveUrl:
  #     liveUrl=liveUrl.split('url=')[1]
  #     #liveUrl=liveUrl.split('proxy/')[1]
  #     print(liveUrl)
  #   response = requests.get(liveUrl)
  #   # 检查请求是否成功
  #   if response.status_code == 200:
  #       # 获取响应内容
  #       response.encoding='utf-8'
  #       data = response.text
  #       print(data)
  #       #print(FindResult(data,''))
  #supplementAddr('','')
  
  start()

