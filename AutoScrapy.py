# -*- coding: utf-8 -*-

import requests
import json
#import ast
import re
import json5
import datetime
import base64
from Crypto.Cipher import AES
import json_repair

def encodeBase64(content):
  content='**'+base64.b64encode(content.encode('utf-8')).decode('utf-8')
  #print(content)
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
    data=json_repair.loads(content)
    #data=json5.loads(content)
    return data
  except ValueError as e:  
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
      if jsonText:
        # 移除 // 注释
        #jsonText=replace_newlines_in_quoted_strings(jsonText)
        jsonText=supplementAddr(url,jsonText)
        #config=json5.loads(jsonText)
        config=json_repair.loads(jsonText)
        return config
  except requests.exceptions.RequestException as e:  
    print(e)
  

def getConfigs(list):
  configList={}
  sites=[]
  for key,value in list.items():
    config=getConfig(value)
    if config:
      configList[key]=config
      sites.append({"name":key,"url":value})
  return configList,sites

def setConfig(configList):
  # 配置主体内容
  print('设置主配置',list(configList.keys()))
  if configList:
    configs=list(configList.keys())
    customConfig=configList.get(configs[0])
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
  # parses=[
  #   {
  #     "name": "Json聚合",
  #     "type": 3,
  #     "url": "Demo"
  #   },
  #   {
  #     "name": "Web聚合",
  #     "type": 3,
  #     "url": "Web"
  #   },
  #   {
  #     "name": "qiyi[官源]",
  #     "type": 1,
  #     "url": "http://39.104.230.177:1122/lxjx/myyk.php?url="
  #   },
  #   {
  #     "name": "肥猫最可爱",
  #     "type": 1,
  #     "url": "http://xn--ihqu10cn4c.xn--z7x900a.live/jx.php?id=2&url=",
  #     "ext": {
  #       "flag": [ "qq","腾讯", "qiyi","爱奇艺","奇艺","youku","优酷","sohu","搜狐","letv","乐视","mgtv","芒果","rx","ltnb","bilibili","1905","xigua"]
  #     }
  #   }
  #   ]
  # if customConfig :
  #   customConfig['parses']=parses
    # 提取解析parses
    # if customConfig.get('parses'):
    #   customConfig['parses'].extend(parses)
    # else:
    #   customConfig['parses']=parses
    
def setLives(customConfig,configList):
  lives=[]
  mylive={
      "name": "yub168",
      "type": 0,
      "url": "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yub168/m3u-tester/master/lives.txt",
      "playerType": 1,
      "ua": "okhttp/3.15",
      "epg": "http://diyp2.112114.xyz/?ch={name}&date={date}",
      "logo": "http://diyp2.112114.xyz/logo/{name}.png"
    }
  lives.append(mylive)
  liveSource={}
  for site,config in configList.items():
    liveItem=config.get('lives',None)
    if liveItem:
      #lives.extend(liveItem)
      for item in liveItem:
        url=item.get('url','')
        if url:
          if "127.0.0.1" in url:
            path=url.split('url=')
            if len(path)>1:
              url=path[1]
            else:
              continue
          liveSource.update({site+"_"+item.get('name',''):url})

  if '晨瑞' in configList :
    print('lives 添加 晨瑞')
    lives.extend(configList['晨瑞']['lives'])
  if '俊佬线路' in configList :
    print('lives 添加 俊佬线路')
    lives.extend(configList['俊佬线路']['lives'])
  # if 'OK佬' in configList :
  #   print('lives 配置为 OK佬')
  #   lives.extend(configList['OK佬']['lives'])

  customConfig["lives"]=lives
  if liveSource:
    saveLiveSource(liveSource)

def saveLiveSource(data):
  try:
    with open('liveSource.json','w',encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False)
  except BaseException as e:
        print('保存json失败 %s' % e)


def saveConfig(customConfig):
  
  if customConfig:
  # 配置customConfig及写入文件
    print('保存配置')
    with open("./config.json", "w",encoding='utf-8') as file:
      # 使用json.dump将数据写入文件
      print('抓取时间：\t',datetime.datetime.now())
      json.dump(customConfig,file,ensure_ascii=False)

# 写入多仓配置
def saveMulConfig(list):
  mulConfig={}
  sites=[{'url':'https://gitee.com/yub168/myTvbox/raw/master/config.json','name':"yub168"}]
  sites.extend(list)
  mulConfig['urls']=sites
  with open("./mulConfig.json", "w",encoding='utf-8') as file:
      # 使用json.dump将数据写入文件
      #print('抓取时间：\t',datetime.datetime.now())
      json.dump(mulConfig,file,ensure_ascii=False)

# 补充相对地址
def supplementAddr(url,config):

  host =url[:url.rfind('/')]
  # 解析：
  # ['"]：匹配单引号或双引号的字符集合。
  # (.*?)：非贪婪模式匹配任意字符，直到遇到下一个引号。
  # \1：引用第一个捕获组（即单引号或双引号），确保匹配的是相同类型的引号。
  pattern = r'(["\'])\.(/.*?)\1'  # 匹配双引号或单引号的内容
  config=re.sub(pattern,lambda x:"\""+host+x.group(2)+'\"',config)
  return config

def getSiteList():
  sitelist={
  '摸鱼儿':'http://我不是.摸鱼儿.top',# 点播高清较多，
  'fatCat':'http://肥猫.com/',
  '欧歌':"http://tv.nxog.top/m/" ,
  '南风':'https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json',##点播不错，直播慢
  '潇洒':'https://github.moeyy.xyz/https://raw.githubusercontent.com/PizazzGY/TVBox/main/api.json',#点播不错，直播放不了
  #'拾光':'https://gitee.com/xmbjmjk/omg/raw/master/omg.json',# 点播还行，直播源超多，但有效的不太多
  #'天微':'https://gitee.com/tvkj/tw/raw/main/svip.json',# 点播还行，直播源超多，但有效的不太多
  #'毒盒':'https://毒盒.com/tv',#json 解析错误
  #'茶余':'https://www.gitlink.org.cn/api/kvymin/TVRule/raw/config.json?ref=master',# 点播不太多，直播还行
  '饭太硬':"http://www.饭太硬.com/tv",
  "王小二":"http://tvbox.xn--4kq62z5rby2qupq9ub.xyz/",
  '俊佬线路':'http://home.jundie.top:81/top98.json',#  注意lives地址多
  'PG':'https://git.acwing.com/iduoduo/orange/-/raw/main/jsm.json',
  'OK佬':'http://ok321.top/tv',
  #"香雅情":"https://github.moeyy.xyz/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json",
  #'道长':"https://bitbucket.org/xduo/libs/raw/master/index.json", #有4K专线很多无效
  'D老魔改':'https://download.kstore.space/download/2883/nzk/nzk0722.json',# 点播不行，直播 央卫视高峰期能放 分组词：央卫
  '晨瑞':'https://gitee.com/chenruihe/tvbox/raw/master/%E5%BD%B1%E8%A7%86%E5%86%85%E7%BD%AE%E6%8E%A5%E5%8F%A3',
  '欧歌':"http://tv.nxog.top/m/" 
  
  }
  return sitelist
def start():
  configList,sites=getConfigs(getSiteList())
  customConfig=setConfig(configList)
  setLives(customConfig,configList)
  setParise(customConfig,configList)
  saveConfig(customConfig)
  saveMulConfig(sites)


def testSite(url):
  config=getConfig(url)
  print(config)

if __name__=="__main__":
  testSite("http://tv.nxog.top/m/")
  #start()
  # configList,sites=getConfigs(getSiteList())
  # sites=configList.keys()
  # print(sites)
  # print(list(sites)[0])

  