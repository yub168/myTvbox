import requests
import json
import ast
list={
  'fatCat':'http://肥猫.live',
  'YourSmile':'https://agit.ai/Yoursmile7/TVBox/raw/branch/master/XC.json'
  }
configList={}
headers={
  "User-Agent":"okhttp/3.15",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
  }
for key,value in list.items():
  r=requests.get(value,headers=headers)
  if r.status_code==200:
    start=r.text.index('{')
    end=r.text.rindex('}')
    configList[key]=json.loads(r.text[start:end+1])

#配置主体内容
if 'fatCat' in configList:
  customConfig=configList['fatCat']
elif 'YourSmile' in configList:
  customConfig=configList['YourSmile']

#提取解析parses

#提取lives
if 'YourSmile' in configList:
  lives=configList['YourSmile']['lives']

#配置customConfig及写入文件
if customConfig :
  customConfig['lives']=lives
  with open("./config.json", "w",encoding='utf-8') as file:
    # 使用json.dump将数据写入文件
    json.dump(customConfig,file,ensure_ascii=False)
    



