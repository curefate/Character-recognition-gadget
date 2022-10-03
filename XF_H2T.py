import base64
import hashlib
import json
import time

import requests


class Help(object):
    def __init__(self, path='asset/ConsoleInformation.json'):
        with open(path, 'r') as f:
            ConInf = json.load(f)

        self.APPID = ConInf['Setting'][2]['APPID']
        self.APIKey = ConInf['Setting'][2]['APIKey']
        self.AudioPath = "asset/testImage.png"

    def imgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def get_url(self):
        return "https://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"

    def get_header(self):
        curTime = str(int(time.time()))
        param = "{\"language\":\"" + "cn|en" + "\",\"location\":\"" + "false" + "\"}"
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = self.APIKey + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def get_body(self):
        audioData = self.imgRead(self.AudioPath)
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        data = {'image': content, }
        return data

    def call_url(self):
        if self.APPID == '' or self.APIKey == '':
            return 'Appid 或APIKey 为空！请打开json文件，填写相关信息。'
        else:
            body = self.get_body()
            headers = self.get_header()
            response = requests.post(self.get_url(), data=body, headers=headers, timeout=8)
            status_code = response.status_code
            if status_code != 200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/words/formula-discern/API.html")
                return "Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                # print(respData)
                if len(respData["data"]["block"][0]["line"]) != 0:
                    str = ''
                    for i in range(len(respData["data"]["block"][0]["line"])):
                        if i != 0:
                            str += '\n'
                        str += respData["data"]["block"][0]["line"][i]["word"][0]["content"]
                    print(str)
                    return str
                else:
                    print("识别失败")
                    return "识别失败"
