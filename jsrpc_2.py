import requests
import re
import json
from mitmproxy import ctx
from urllib.parse import quote, unquote
target = "test.com"

def decrypt(encrypted_data):
    url="http://127.0.0.1:5612/business/invoke?group=test&action=decrypt&"
    data = {'text':encrypted_data}
    res=requests.post(url,data=data)
    res = json.loads(res.text)
    return res['data']

def encrypt(data):
    print(data)
    url="http://127.0.0.1:5612/business/invoke?group=test&action=encrypt&text={}".format(data)
    res=requests.get(url)
    print(res.text)
    res = json.loads(res.text)
    return res['data']

def request(flow):
    if flow.request.host != target:
        return
    try:
    # 获取数据包
        body = flow.request.get_text()
    # 调用 encrypt 函数进行加密
        encrypted_data = encrypt(body)
    # 设置修改后的请求 body 数据
        encrypted_body = '{"data":"'+encrypted_data+'"}'
        flow.request.set_text(encrypted_body)
        #ctx.log.warn("加密内容: "+str(flow.request.get_text()))
    except Exception as e:
        print("报文加密失败: {e}")

# 请求后的数据
def response(flow):
    if flow.request.host != target:
        return
    try:
        body = flow.response.get_text()
        regex = '^\"(.*)\"$'
        redata = re.search(regex,str(body))
        if(redata != None):
            data = redata.group(1)
    # 调用 decrypt 函数进行解密
            decrypted_data = decrypt(data)
            decrypted_data = decrypted_data.replace('\'','')
    # 设置修改后的请求 body 数据
            flow.response.set_text(decrypted_data)
    except Exception as e:
        print("报文解密失败: {e}")