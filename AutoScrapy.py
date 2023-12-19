import requests
import json
import ast
import re
import json5
list={
  'fatCat':'http://肥猫.live',
  'YourSmile':'https://agit.ai/Yoursmile7/TVBox/raw/branch/master/XC.json',
  '道长':'https://pastebin.com/raw/5NHaxyGR',
  '香雅情':'https://ghproxy.net/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json',
  'OK佬':'https://github.moeyy.xyz/https://raw.githubusercontent.com/okcaptain/okjar/rm/ok.json',
  '小米':'http://xhww.fun:63/小米/DEMO.json'
  }
configList={}
customConfig={}
headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
for key,value in list.items():
  try:
    r=requests.get(value,headers=headers, timeout=3.0)
    if r.status_code==200:
      r.encoding='utf-8'
      configList[key]=json5.loads(r.text)
  except requests.exceptions.RequestException as e:  
    print(e)

# 配置主体内容
if 'fatCat' in configList:
  customConfig=configList['fatCat']
elif 'YourSmile' in configList:
  customConfig=configList['YourSmile']
elif '香雅情' in configList:
  customConfig=configList['香雅情']
elif '道长' in configList:
  customConfig=configList['道长']

# 给主体添加部分site
if '道长' in configList:
  # 添加农民site
  sites=configList['道长']['sites']
  for site in sites:
    if '农民' in site['key']:
      customConfig['sites'].append(site)
    if '秋霞影院' in site['key']:
      customConfig['sites'].append(site)
    if '奇优影院' in site['key']:
      customConfig['sites'].append(site)
    if '米爱影视' in site['key']:
      customConfig['sites'].append(site)
  

if customConfig :

  # 提取解析parses
  parses=[]
  if '香雅情' in configList and not parses:
    parses=configList['香雅情']['parses']
    customConfig['parses']=parses
  if 'OK佬' in configList and not parses:
    parses=configList['OK佬']['parses']
    customConfig['parses']=parses
  if '小米' in configList:
    parses=configList['小米']['parses']
    for parse in parses:
      if '稻香' in parse['name']:
        customConfig['parses'].append(parse)
      if 'YuMi-vip' in parse['name']:
        customConfig['parses'].append(parse)


  # 提取lives
  lives=[]
  if 'YourSmile' in configList and not lives:
    lives=configList['YourSmile']['lives']
    customConfig['lives']=lives
  if 'OK佬' in configList and not lives:
    lives=configList['OK佬']['lives']
    customConfig['lives']=lives

  # 配置customConfig及写入文件
  with open("./config.json", "w",encoding='utf-8') as file:
    # 使用json.dump将数据写入文件
    print(customConfig)
    json.dump(customConfig,file,ensure_ascii=False)
    



