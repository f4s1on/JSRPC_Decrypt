# JSRPC_Decrypt
一个基于JSRPC实现的自动解密代理框架


## 原理图

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/465bf9cd-fbb2-4c92-b98e-3478f5988c0e)



## 参考文章：

https://zgao.top/%e7%bd%91%e7%ab%99%e5%8a%a0%e5%af%86%e4%bc%a0%e8%be%93%e5%9c%ba%e6%99%af%e4%b8%8b%e7%9a%84%e6%bc%8f%e6%b4%9e%e6%89%ab%e6%8f%8f%e6%80%9d%e8%b7%af/#%E5%AE%9E%E6%88%98%E6%B5%8B%E8%AF%95

## 使用方法
### 一、利用sekiro实现jsrpc

找到网站的加解密函数设置成全局变量

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/d85e8c75-5df1-49e8-b7cf-d33231786b35)


jsrpc.js需要修改的代码部分

每个网站需要根据实际的函数名称修改成对应的调用方式

如下面代码中的：encrypt(test, aesKey)、decrypt(request['text'], aesKey)对应上图中的encrypt(data, aesKey)、decrypt(data, aesKey)

```javascript
var client = new SekiroClient("ws://127.0.0.1:5612/business/register?group=test&clientId=" + Math.random());

client.registerAction("encrypt", function(request, resolve, reject) {
    test = JSON.parse(request['text']);
    response = encrypt(test, aesKey);
    resolve(response);
});
client.registerAction("decrypt", function(request, resolve, reject) {
    response = decrypt(request['text'], aesKey);
    response = JSON.stringify(response);
    resolve("'"+response+"'");
});
```

具体的细节不再赘述，最后达到的效果如下图即可，传入明文参数text，获得密文data

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/5a29bf64-09f9-435e-a731-8668eb87f441)

### 二、开启两个mitmproxy
由于证书问题，这里用于测试的浏览器需要通过如下命令启动

`chrome.exe  --ignore-certificate-errors`

两个代理启动的命令

第一个代理设置的上游代理即burp监听的代理不能设置成127.0.0.1，必须设置成内网地址

`mitmdump -s jsrpc_1.py -p 8079 --set block_global=false --mode upstream:http://10.33.94.41:8080 --ssl-insecure`

`mitmdump -s jsrpc_2.py -p 8020 --set block_global=false --ssl-insecure`

jsrpc_1.py和jsrpc_2.py需要修改两个地方：①target修改成目标域名，②密文匹配正则根据实际情况修改

这里示例的网站请求和响应格式为

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/e674b111-252a-4ed9-aa6b-edc0fef93787)

### 代理设置
浏览器的代理设置成第一个mitmproxy监听的端口

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/c3586c98-cf62-4ac6-b4bc-ff0e1a10d6ad)

burp开启内网地址的监听端口

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/3ad0bd81-6778-4790-9576-a950d0813c62)


burp的上游代理设置成第二个mitmproxy监听的端口

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/998e2c83-dfbf-479e-9e64-6eec51e624c8)

## 最终效果
burp直接抓到明文请求参数

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/a4258e5b-38d1-4590-adbc-6f641a962360)

burp直接收到的响应也是明文

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/d974d15f-756e-4095-b070-1f364897dd03)

可以进行重放

![image](https://github.com/f4s1on/JSRPC_Decrypt/assets/57355558/9a3eeb78-712a-4b8c-b1ec-69c4f365ef5b)
