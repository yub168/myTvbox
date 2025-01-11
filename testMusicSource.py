
import requests

source={
	"至尊源":{
		"host":"http://110.42.36.53:1314",
		"Headers":{
			"API_KEY":""
		}
	},
	"Nya":{
		"host":"http://103.40.13.21:9866",
		"Headers":{
			"API_KEY":"nya"
		}
	},
	"ikunshare":{
		"host":"https://lxmusic.ikunshare.com:9763",
		"Headers":{
			"API_KEY":"ikunsource"
		}
	},
	"Huibq":{
		"host":"https://render.niuma666bet.buzz",
		"Headers":{
      'Content-Type': 'application/json',
      'User-Agent': 'lx-music-android/v1.2.0',
			"API_KEY":"share-v2"
		}
	}
}

def test():
  for value in source.values():
    url=value['host']+"/url/wy/187995/128k"
    headers=value['Headers']
    try:
      r=requests.get(url,headers=headers, timeout=3.0)
      print(r)
      if r.status_code==200:
        r.encoding='utf-8'
        #print(r)
    except requests.exceptions.RequestException as e:  
      print(e)

test()