# -*- coding: utf-8 -*-
from flask import Flask
import hashlib
import xml.etree.cElementTree as ET
from flask import render_template, request, make_response
import time
import tuling

app = Flask(__name__)

#设置路由，get请求进入验证部分；post请求获取用户发送的信息
@app.route('/wx', methods=['GET', 'POST'])
#因为目前只需要信息的转发，这里只定义了一个函数
def verification():
#个人云服务器与微信服务器验证，进行绑定
    if request.method == 'GET':
        data = request.args
        if len(data) == 0:
            return "hello, this is handle view"
#获取微信后台传递的字符串
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = "chengxin"
        list = [token, timestamp, nonce]
        list.sort()
#采用hashlib库sha1方法加密
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode("utf-8"))
        sha1.update(list[1].encode("utf-8"))
        sha1.update(list[2].encode("utf-8"))
#获取加密后十六进制数据字符串值
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
#验证通过返回成功代码，验证失败返回“信息验证错误~”
        if hashcode == signature:
            return echostr
        else:
            return "信息验证错误~"
#对用户信息进行接收提取
    if request.method == 'POST':
#微信后台将用户信息用XML格式传递，查看开发手册提取信息的类型，用户名，接收名，用户ID
        xml = ET.fromstring(request.data)
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
#对信息进行分类，以便后期针对处理
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
#中途临时加入公司推广赛事，时间紧急遂没有制作单独分开的功能模块
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

#启动本地服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)

