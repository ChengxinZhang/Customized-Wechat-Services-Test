# -*- coding: utf-8 -*-
from flask import Flask
import hashlib
import xml.etree.cElementTree as ET
from flask import render_template, request, make_response
import time
import tuling

app = Flask(__name__)


@app.route('/wx', methods=['GET', 'POST'])
def verification():
    if request.method == 'GET':
        data = request.args
        if len(data) == 0:
            return "hello, this is handle view"
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = "chengxin"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode("utf-8"))
        sha1.update(list[1].encode("utf-8"))
        sha1.update(list[2].encode("utf-8"))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return "shenmegui"
    if request.method == 'POST':
        xml = ET.fromstring(request.data)

        # str_xml = request.values
        # type_text = str(type(str_xml))
        # return self.render.reply_text(fromUser, toUser, int(time.time()), type_text)
        # xml = etree.fromstring(str_xml)

        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        userId = fromUser[0:15]
        reply = '''<xml>
	                       <ToUserName><![CDATA[%s]]></ToUserName>
	                       <FromUserName><![CDATA[%s]]></FromUserName>
	                       <CreateTime>%s</CreateTime>
	                       <MsgType><![CDATA[text]]></MsgType>
	                       <Content><![CDATA[%s]]></Content>
	                    </xml>'''

        if msgType == 'text':
            msgType = 0
            content = xml.find("Content").text
        elif msgType == 'image':
            msgType == 1
            imageUrl = xml.find("PicUrl").text
            content = ''
        elif msgType == 'voice':
            msgType == 0
            content = xml.find("Recognition").text
        # else:
        # 	response = make_response(reply % (fromUser, toUser, str(int(time.time())), ''))
        # 	response.headers['content-type'] = 'application/xml'
        # 	return response

        Sjsl = ['星','心','薪','欣']
        #if content != None: 
        if Sjsl[0] in content or Sjsl[1] in content or Sjsl[2] in content or Sjsl[3] in content:
        	reply_conent = '80W+奖金'+'\n'+'https://event.asus.com.cn/SJSL/'+'\n'+'快来点我报名吧~'
        	response = make_response(reply % (fromUser, toUser, str(int(time.time())), reply_conent))
        	response.headers['content-type'] = 'application/xml'
        	return response
        elif msgType == 1:
        	reply_conent = '对不起小A还看不懂图片...'
        	response = make_response(reply % (fromUser, toUser, str(int(time.time())), reply_conent))
        	response.headers['content-type'] = 'application/xml'
        	return response
        elif content == '':
         	reply_conent = '对不起小A不太理解您的意思...'
         	response = make_response(reply % (fromUser, toUser, str(int(time.time())), reply_conent))
         	response.headers['content-type'] = 'application/xml'
         	return response

        else:  
        	reply_conent = tuling.talk(content,userId)
        	response = make_response(reply % (fromUser, toUser, str(int(time.time())), reply_conent))
        	response.headers['content-type'] = 'application/xml'
        	return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
