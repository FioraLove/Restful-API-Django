# -*- coding:utf-8 -*-
import requests
import re
from pyquery import PyQuery as pq
import json


class ZuiYou(object):
    def __init__(self, url):
        self.url = "http" + url.split("http")[1]
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "Host": "share.izuiyou.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/84.0.4147.125 Safari/537.36 "
        }
        pattern = re.compile('"urlsrc":"(.*?)"', re.S)
        try:
            response = self.session.post(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    url = str(re.findall(pattern, response.text)[0]).encode("utf-8").decode("unicode_escape")
                    result = pq(response.text)
                    title = result(".SharePostCard__content").text()
                    info = {"title": title, "url": url}
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
