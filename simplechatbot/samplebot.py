#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
import os

from aip import AipSpeech
from recoder import *

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

KEY = 'KEY_ID'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = '我明了'
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg)
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

if __name__ == "__main__":

    APP_ID = 'APP_ID'
    API_KEY = 'API_KEY'
    SECRET_KEY = 'SECRET_KEY'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 开始对话
    while True:
        r = recoder()
        r.recoder()
        r.savewav("hello.wav")
        time.sleep(0.1)

        result = client.asr(get_file_content('hello.wav'), 'pcm', 16000, {
            'lan': 'zh',
        })
        
        if result['err_no'] == 0:
            print(result['result'][0])
            output = tuling_reply(result['result'][0])
            print(output)

            result = client.synthesis(str(output), 'zh', 1, {
                'vol': 5,
            })

            if not isinstance(result, dict):
                with open('hello.mp3', 'wb') as f:
                    f.write(result)

            time.sleep(0.1)
            os.system("mpg321 hello.mp3")

        time.sleep(0.5)
