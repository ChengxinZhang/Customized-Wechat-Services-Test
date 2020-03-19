# -*- coding: utf-8 -*-
import requests
import json
def talk(content,userId):
    #reqType = 0
    url = 'http://www.tuling123.com/openapi/api'
    apiKey = 'tuling账户的apikey'
#构建请求参数
    data = {      
        'key':apiKey,
        'info':content, 
        #'loc':loc,
        'userid':userId
    }
    json_data = json.dumps(data)
    req = requests.post(url,data = json_data)
#将返回值转为json格式去提取
    result = json.loads(req.text)
    if result['code'] == 200000:
        return result['text']+result['url']
    elif result['code'] == 100000:
        return result['text']



