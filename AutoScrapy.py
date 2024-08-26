# -*- coding: utf-8 -*-

import requests
import json
#import ast
import re
import json5
import datetime
import base64
from Crypto.Cipher import AES


def encodeBase64(content):
  content='**'+base64.b64encode(content.encode('utf-8')).decode('utf-8')
  print(content)
  return content

def replace_newlines_in_quoted_strings(text, replacement=" "):
    # 使用正则表达式移除单行注释
    #text= re.sub(r'(?<!http:)(?<!https:)//.*|/\*(.|\n)*?\*/', "", text, flags=re.MULTILINE)
    # 正则表达式匹配双引号内的换行符
    pattern = r'"[^"]+"'
    # 使用re.SUB标志进行全局替换
    #text=re.sub(pattern, lambda m: m.group(0).replace("\n", replacement), text, flags=0)
    
    return text

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
  print('json解析内容：',content)
  content=replace_newlines_in_quoted_strings(content)
  
  try:
    #print('json解析内容：',content)
    print_specific_line(content,147)
    data=json5.loads(content)
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
        jsonText=replace_newlines_in_quoted_strings(jsonText)
        supplementAddr(url,jsonText)
        config=json5.loads(jsonText)
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
    
'''
def setLives(customConfig,configList):
  # 提取lives
  print('设置直播')
  #proxy='https://mirror.ghproxy.com/'
  url='https://mirror.ghproxy.com/github.com/yub168/myTvbox/raw/master/live.txt'
  #url='http://127.0.0.1:9978/proxy?do=live&url=https://gitee.com/yub168/myTvbox/raw/master/lives.txt'
  #    http://127.0.0.1:9978/proxy?do=live&url=https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1722589153126/movie.txt
  lives=[]
  if '晨瑞' in configList and not lives:
    print('lives 配置为 晨瑞')
    lives=configList['晨瑞']['lives']
  if '俊佬线路' in configList and not lives:
    print('lives 配置为 俊佬线路')
    lives=configList['俊佬线路']['lives']
  if 'OK佬' in configList and not lives:
    print('lives 配置为 OK佬')
    lives=configList['OK佬']['lives']
    
  if lives:
    liveUrl=lives[0].get('url')
    if liveUrl:
      if '127.0.0.1:9978' in liveUrl:
        liveUrl=liveUrl.split('url=')[1]
      response = requests.get(liveUrl)
      # 检查请求是否成功
      if response.status_code == 200:
          # 获取响应内容
          response.encoding='utf-8'
          data = response.text
          #data=encodeBase64(data)
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
'''
def setLives(customConfig,configList):
  lives=[]
  mylive={
      
      "name": "yub168",
      "type": 0,
      "url": "https://mirror.ghproxy.com/https://github.com/yub168/m3u-tester/raw/master/lives.txt",
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
      lives.extend(liveItem)
      for item in liveItem:
        url=item.get('url','')
        if url:
          if "127.0.0.1" in url:
            url=url.split('url=')[1]
          liveSource.update({site+"_"+item.get('name',''):url})

  # if '晨瑞' in configList :
  #   print('lives 配置为 晨瑞')
  #   lives.extend(configList['晨瑞']['lives'])
  # if '俊佬线路' in configList :
  #   print('lives 配置为 俊佬线路')
  #   lives.extend(configList['俊佬线路']['lives'])
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
      print('抓取时间：\t',datetime.datetime.now())
      json.dump(mulConfig,file,ensure_ascii=False)

# 补充相对地址
def supplementAddr(url,config):

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
  '摸鱼儿':'http://我不是.摸鱼儿.top',# 点播直播都还行
  '南风':'https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json',##点播不错，直播慢
  '潇洒':'https://github.moeyy.xyz/https://raw.githubusercontent.com/PizazzGY/TVBox/main/api.json',#点播不错，直播放不了
  '拾光':'https://gitee.com/xmbjmjk/omg/raw/master/omg.json',# 点播还行，直播源超多，但有效的不太多
  '天微':'https://gitee.com/tvkj/tw/raw/main/svip.json',# 点播还行，直播源超多，但有效的不太多
  '毒盒':'https://毒盒.com/tv',#json 解析错误
  '茶余':'https://www.gitlink.org.cn/api/kvymin/TVRule/raw/config.json?ref=master',# 点播不太多，直播还行
  '饭太硬':"http://www.饭太硬.com/tv",
  "王小二":"http://tvbox.xn--4kq62z5rby2qupq9ub.xyz/",
  '俊佬线路':'http://home.jundie.top:81/top98.json',#  注意lives地址多
  'PG':'https://git.acwing.com/iduoduo/orange/-/raw/main/jsm.json',
  'OK佬':'http://ok321.top/tv',
  "香雅情":"https://github.moeyy.xyz/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json",
  #'道长':"https://bitbucket.org/xduo/libs/raw/master/index.json", #有4K专线很多无效
  'D老魔改':'https://download.kstore.space/download/2883/nzk/nzk0722.json',# 点播不行，直播 央卫视高峰期能放 分组词：央卫
  '晨瑞':'https://gitee.com/chenruihe/tvbox/raw/master/%E5%BC%80%E6%94%BE%E6%8E%A5%E5%8F%A3-%E5%BD%B1%E8%A7%86%E7%82%B9%E6%92%AD+%E5%A4%AE%E5%8D%AB%E8%A7%86',
  '欧歌':"https://xn--tkh-mf3g9f.v.nxog.top/m/111.php?ou=公众号欧歌app&mz=index&jar=index&123&b=欧歌tkh" #json 解析错误
  
  }


  configList,sites=getConfigs(list)
  customConfig=setConfig(configList)
  setLives(customConfig,configList)
  setParise(customConfig,configList)
  saveConfig(customConfig)
  saveMulConfig(sites)


def print_specific_line(text, line_number):
    # 将文本分割为行列表
    lines = text.split('\n')
    
    # 检查请求的行号是否在有效范围内
    if 1 <= line_number <= len(lines):
        # 输出指定行的内容
        print(f"Line {line_number}: {lines[line_number - 1]}")
    else:
        print(f"Error: Line number {line_number} is out of range.")

if "__name__==__main__":
  
  # url='https://xn--tkh-mf3g9f.v.nxog.top/m/111.php?ou=公众号欧歌app&mz=index&jar=index&123&b=欧歌tkh'
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
  