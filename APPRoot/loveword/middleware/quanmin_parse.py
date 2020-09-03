# -*- coding:utf-8 -*-
import json
import requests
import re


class QuanMin(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_info(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "upgrade-insecure-requests": "1"
        }
        try:
            response = self.session.post(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                doc = response.text
                title = re.findall('<meta property="og:title" content="(.*?)">', doc, re.S)[0]
                cover = re.findall('<meta property="og:image" content="(.*?)">', doc, re.S)[0]
                video = re.findall('<meta property="og:videosrc" content="(.*?)">', doc, re.S)[0]
                return json.dumps({"title": title, "cover": cover, "video": video}, ensure_ascii=False)
        except Exception as e:
            json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
