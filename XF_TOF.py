import base64
import hashlib
import hmac
import json
import datetime
import requests


class Help(object):
    def __init__(self, path='asset/ConsoleInformation.json'):
        with open(path, 'r') as f:
            ConInf = json.load(f)

        self.APPID = ConInf['Setting'][0]['APPID']
        self.Secret = ConInf['Setting'][0]['Secret']
        self.APIKey = ConInf['Setting'][0]['APIKey']
        self.AudioPath = "asset/testImage.png"

    def imgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + "rest-api.xfyun.cn" + "\n"
        signatureStr += "date: " + self.httpdate(datetime.datetime.utcnow()) + "\n"
        signatureStr += "POST" + " " + "/v2/itr" \
                        + " " + "HTTP/1.1" + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def get_url(self):
        return 'https://rest-api.xfyun.cn/v2/itr'

    def get_header(self, data):
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, "hmac-sha256", sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": "rest-api.xfyun.cn",
            "Date": self.httpdate(datetime.datetime.utcnow()),
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        audioData = self.imgRead(self.AudioPath)
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        BusinessArgs = {
            "ent": "teach-photo-print",
            "aue": "raw",
        }
        postdata = {
            "common": {"app_id": self.APPID},
            "business": BusinessArgs,
            "data": {
                "image": content,
            }
        }
        body = json.dumps(postdata)
        return body

    def call_url(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            return 'Appid 或APIKey 或APISecret 为空！请打开json文件，填写相关信息。'
        else:
            body = self.get_body()
            headers = self.get_header(body)
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
                if "region" in respData["data"]:
                    ret = respData["data"]["region"][0]["recog"]["content"]
                    ret = ret.replace('ifly-latex-begin', '')
                    ret = ret.replace('ifly-latex-end', '')
                    print(ret)
                    return ret
                else:
                    print("识别失败")
                    return "识别失败"
