# -*- coding:utf-8 -*-
import base64
import requests
import json
import re
import execjs

"""
# 方法一：
class MeiPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        with open("static/loveword/js/meipai_encrypt.js", "r", encoding="utf-8") as f:
            resource = f.read()
        self.ctx = execjs.compile(resource)

    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.meipai.com",
            "Referer": "http://www.meipai.com/"
        }
        pattern = re.compile('data-video="(.*?)"', re.S)
        pattern2 = re.compile('<meta name="description" content="(.*?)"', re.S)
        try:
            response = self.session.get(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                video_bs64 = re.findall(pattern, response.text)[0]
                title = re.findall(pattern2, response.text)[0]
                video_url = self.ctx.call("getmp4", video_bs64)
                info = {
                    "title": title,
                    "video": "https:"+video_url
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
"""


# 方法二
class MeiPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def getHex(self, a):
        hex_1 = a[:4][::-1]
        str_1 = a[4:]
        return str_1, hex_1

    def getDec(self, a):
        b = str(int(a, 16))
        c = list(b[:2])
        d = list(b[2:])
        return c, d

    def substr(self, a, b):
        k = int(b[0])
        c = a[:k]
        d = a[k:k + int(b[1])]
        temp = a[int(b[0]):].replace(d, "")
        result = c + temp
        return result

    def getPos(self, a, b):
        b[0] = len(a) - int(b[0]) - int(b[1])
        return b

    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.meipai.com",
            "Referer": "http://www.meipai.com/"
        }
        pattern = re.compile('data-video="(.*?)"', re.S)
        pattern2 = re.compile('<meta name="description" content="(.*?)"', re.S)
        try:
            response = self.session.get(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                video_bs64 = re.findall(pattern, response.text)[0]
                title = re.findall(pattern2, response.text)[0]
                str1, hex1 = self.getHex(video_bs64)
                pre, tail = self.getDec(hex1)
                d = self.substr(str1, pre)
                kk = self.substr(d, self.getPos(d, tail))
                a = base64.b64decode(kk)
                info = {
                    "title": title,
                    "video": "https:"+a.decode(encoding='utf-8')
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
