# -*- coding: utf-8 -*-

import requests
import json,simplejson
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
  
  # 解析加密 以8个字母加**的内容
  pattern = re.compile(r"[A-Za-z0]{8}\*\*")
  result = pattern.search(content) 
  if result:
    try:
        #print(result.group())
        #print(content.index(result.group()))
        #print('8个字母开头加密')
        content = content[content.index(result.group()) + 10:]
        data=base64.b64decode(content).decode('utf-8')
        #print(data)
        return True,data
    except Exception as e:
      return False,e
    
  # 解析 以**开头的内容 主要在lives配置加密中
  if content.startswith('**'):
    try:
        #print(result.group())
        #print(content.index(result.group()))
        #print('**开头加密')
        content = content[2:]
        data=base64.b64decode(content).decode('utf-8')
        #print(data)
        return True,data
    except Exception as e:
      return False,e
    
  # 解析 以2423开头的内容
  if content.startswith('2423'):
        #print('2423开头加密')
        return False,'2423开头内容尚末解析'
  
  # 放后面主要防止不是json的为判断为json
  if isJson(content):
    #print('========= is json5')
    #print('无加密')
    return True,content
  
  elif key and isJson(content):
    try:
      aes = AES.new(key,AES.MODE_ECB)
      data=aes.decrypt(content)
      return True,data
    except Exception as e:
      return False,e
  
  else:
    return False,'无法解析内容'

def printLine(content,n):
  lines = content.split('\n')
  try:
      line_content = lines[n - 1]
      print(f"第{n}行的内容是: {line_content}")
  except IndexError:
      print(f"行号 {n} 超出字符串的行数范围。")

def replace_newlines_in_quoted_strings(text):
  # 正则表达式模式：匹配引号中的内容，包括换行符
  pattern = r'(["\'])([\s\S]*?)\1'

  # 替换函数：将匹配到的内容中的换行符替换为空格
  def replace_newlines_in_quotes(match):
      #print('内容：',match.group(0))
      return re.sub(r'\n', '', match.group(0))

  # 使用 re.sub 进行替换
  result = re.sub(pattern, replace_newlines_in_quotes, text)
  return result

def safePariseJson(content):
  import sys
  try:
    #print('json解析内容：',content)
    data=json5.loads(content)
    return data
  except Exception as e:  
    error_info = sys.exc_info()
    print("错误类型：", error_info[0])
    print("错误信息：", error_info[1])
    print("错误位置：", error_info[2])
    #printLine(content,1)
    partent=replace_newlines_in_quoted_strings(content)
    content = re.sub(r'(?<!http:)(?<!https:)//.*|/\*(.|\n)*?\*/', '',partent)
    data=json_repair.loads(content)
    if isinstance(data, dict):
      return data


def isJson(content):
  try:
    data=safePariseJson(content)
    #print("confing类型:",type(data))
    #data=json5.loads(content)
    return data
  except ValueError as e:  
      print('isJson解析json错误：',e)
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
      result,jsonText=FindResult(r.text,'')
      if result:
        jsonText=supplementAddr(url,jsonText)
        #config=json5.loads(jsonText,strict=False)
        #config=json.JSONDecoder(strict=False).decode(jsonText)
        config=safePariseJson(jsonText)
        return True,config
      else:
        return False,jsonText
    else:
      return False,'网络错误'
  except requests.exceptions.RequestException as e:  
    print(e)
    return False,e
  

def getConfigs(list):
  configList={}
  sites=[]
  for key,value in list.items():
    print(f'======开始抓取：{key}')
    result,config=getConfig(value)
    if result:
      configList[key]=config
      sites.append({"name":key,"url":value})
    else:
      print(f'====== {key} 抓取失败：{config}')
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
      if  item.get('ext') and 'danmu' in item.get('ext'):
        #print('====has danmu====')
        del item['ext']['danmu']
      if siteKey in item['name']:
        item['playerType']=category
  

def setParise(customConfig,configList):
  print('设置解析')
  parses=[
    { # 来自 潇洒 
      "name": "LX蓝光",
      "url": "http://llyh.xn--yi7aa.top/api/?key=5b317c16d457b31a3150d87c0a362a9e&url=",
      "flag": [
        "LXTX"
      ],
      "header": {
        "User-Agent": "Dalvik/2.1.0"
      },
      "type": "1"
    },
    { # 来自 潇洒 
      "name": "DJ专线",
      "url": "http://jx.voooe.cn/api/?key=aa70f97f8c109a3c6937ea27a98da6e0&url=",
      "flag": [
        "duanju"
      ],
      "header": {
        "User-Agent": "Dalvik/2.1.0"
      },
      "type": "1"
    },
    { # 来自 潇洒
      "name": "虾米",
      "type": 0,
      "url": "https://jx.xmflv.com/?url=",
      "ext": {
        "header": {
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
        }
      }
    },
    { # 来自 潇洒
      "name": "8090",
      "type": 0,
      "url": "https://www.8090g.cn/?url="
    },
    { # 来自 潇洒
      "name": "ckplayer",
      "type": 0,
      "url": "https://www.ckplayer.vip/jiexi/?url="
    },
    {
      "name": "夜幕",
      "type": 0,
      "url": "https://www.yemu.xyz/?url=",
      "ext": {
        "flag": [
          "qq",
          "腾讯",
          "qiyi",
          "iqiyi",
          "爱奇艺",
          "奇艺",
          "youku",
          "优酷",
          "mgtv",
          "芒果",
          "letv",
          "乐视",
          "pptv",
          "PPTV",
          "sohu",
          "bilibili",
          "哔哩哔哩",
          "哔哩"
        ]
      }
    },
    {
      "name": "冰豆",
      "url": "https://bd.jx.cn/?url=",
      "type": 0,
      "ext": {
        "flag": [
          "qiyi",
          "imgo",
          "爱奇艺",
          "奇艺",
          "qq",
          "qq 预告及花絮",
          "腾讯",
          "youku",
          "优酷",
          "pptv",
          "PPTV",
          "letv",
          "乐视",
          "leshi",
          "mgtv",
          "芒果",
          "sohu",
          "xigua",
          "fun",
          "风行"
        ]
      },
      "header": {
        "User-Agent": "Mozilla/5.0"
      }
    }
    ]
  if customConfig :
    customConfig['parses'].extend(parses)
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
      "url": "http://github.yub168.dpdns.org/raw.githubusercontent.com/yub168/m3u-tester/master/lives.txt",
      "playerType": 1,
      "ua": "okhttp/3.15",
      #"epg": "http://diyp2.112114.xyz/?ch={name}&date={date}",
      "epg": 'http://epg.51zmt.top:8000/api/diyp/?ch={name}&date={date}',
      "logo": "http://diyp2.112114.xyz/logo/{name}.png"
    }
  lives.append(mylive)
  liveSource={}
  for site,config in configList.items():
    #print(f'========site:{site},\n=========config:{config}')
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
  sites=[{'url':'http://github.yub168.dpdns.org/raw.githubusercontent.com/yub168/myTvbox/refs/heads/master/config.json','name':"yub168"}]
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
  '摸鱼儿':'http://我不是.摸鱼儿.com',# 点播高清较多，
  'fatCat':'http://肥猫.com/',
  '欧歌':"http://tv.nxog.top/m/" , #解析错误 https://tv.nxog.top/m/111.php?ou=公众号欧歌app&mz=index&jar=index&123&b=tv
  '南风':'http://github.yub168.dpdns.org/raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json',##点播不错，直播慢
  '潇洒':'http://github.yub168.dpdns.org/raw.githubusercontent.com/PizazzGY/TVBox/main/api.json',#点播不错，直播放不了
  #'拾光':'https://gitee.com/xmbjmjk/omg/raw/master/omg.json',# 点播还行，直播源超多，但有效的不太多
  #'天微':'https://gitee.com/tvkj/tw/raw/main/svip.json',# 点播还行，直播源超多，但有效的不太多
  #'毒盒':'https://毒盒.com/tv',#json 解析错误
  #'茶余':'https://www.gitlink.org.cn/api/kvymin/TVRule/raw/config.json?ref=master',# 点播不太多，直播还行
  '饭太硬':"http://www.饭太硬.com/tv",
  "王小二":"http://tvbox.xn--4kq62z5rby2qupq9ub.top/",
  '俊佬线路':'http://home.jundie.top:81/top98.json',#  注意lives地址多
  #'PG':'https://git.acwing.com/iduoduo/orange/-/raw/main/jsm.json',
  'OK佬':'http://ok321.top/tv', #解析错误 
  #"香雅情":"https://github.moeyy.xyz/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json",
  #'道长':"https://bitbucket.org/xduo/libs/raw/master/index.json", #有4K专线很多无效
  #'D老魔改':'https://download.kstore.space/download/2883/nzk/nzk0722.json',# 点播不行，直播 央卫视高峰期能放 分组词：央卫
  #'晨瑞':'https://ghproxy.cn:443/https://raw.githubusercontent.com/wagaga001/chenrui/refs/heads/main/ruiying_Built-in%20interfaces',
  
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
  print(type(config))
  #print(config)
  print(config[1]['sites'])
  return config

def jsonPariseTest():
  json_string = """
📢接口软件永远免费
📢长期维护切勿贩卖
📢智能AI已过滤广告"
              """
  if isJson(json_string):
    print('True')
  else:
    print('False')
  # 使用json.loads()解析JSON字符串
  #data = json5.loads(json_string)
  # json_string=replace_newlines_in_quoted_strings(json_string)
  # data = simplejson.loads(json_string)
  # print(data)  # 输出解析后的数据

if __name__=="__main__":
  #http://我不是.摸鱼儿.com
  #http://tvbox.xn--4kq62z5rby2qupq9ub.xyz/
  #testSite("https://tv.nxog.top/m/")
  #jsonPariseTest()
  start()
  # configList,sites=getConfigs(getSiteList())
  # sites=configList.keys()
  # print(sites)
  # print(list(sites)[0])

  