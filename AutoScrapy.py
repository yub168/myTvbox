import requests
import json
import ast
import re
import json5
list={
  'fatCat':'http://肥猫.live',
  'YourSmile':'https://agit.ai/Yoursmile7/TVBox/raw/branch/master/XC.json',
  '香雅情':'https://ghproxy.net/https://raw.githubusercontent.com/xyq254245/xyqonlinerule/main/XYQTVBox.json'
  }
configList={}
customConfig={}
headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
for key,value in list.items():
  r=requests.get(value,headers=headers)
  if r.status_code==200:
    r.encoding='utf-8'
    configList[key]=json5.loads(r.text)
    

#配置主体内容
if 'fatCat' in configList:
  customConfig=configList['fatCat']
elif 'YourSmile' in configList:
  customConfig=configList['YourSmile']
elif '香雅情' in configList:
  customConfig=configList['香雅情']
if customConfig :
  #提取解析parses
  #parses=[]
  if '香雅情' in configList:
    parses=configList['香雅情']['parses']
    customConfig['parses']=parses
  #提取lives
  #lives=[]
  if 'YourSmile' in configList:
    lives=configList['YourSmile']['lives']
    customConfig['lives']=lives

  #配置customConfig及写入文件
  with open("./config.json", "w",encoding='utf-8') as file:
    # 使用json.dump将数据写入文件
    print(customConfig)
    json.dump(customConfig,file,ensure_ascii=False)
    



