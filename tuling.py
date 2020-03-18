# -*- coding: utf-8 -*-
import requests
import json
def talk(content,userId):
    #reqType = 0
    url = 'http://www.tuling123.com/openapi/api'
    apiKey = 'b086a72ed3eb4f9794a1a84e817a438c'
    data = {      
        'key':apiKey,
        'info':content, 
        #'loc':loc,
        'userid':userId
    }
    json_data = json.dumps(data)
    req = requests.post(url,data = json_data)
    result = json.loads(req.text)
    if result['code'] == 200000:
        return result['text']+result['url']
    elif result['code'] == 100000:
        return result['text']



