# -*- coding:utf-8 -*-
import time
import requests
import json


class sixRoom(object):
    def __init__(self, url):
        self.url = url

    def get_video(self):

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        session = requests.Session()

        if len(self.url) <= 15:
            link = "https://v.6.cn/minivideo/auth.php"
            try:
                params = {
                    "act": "play",
                    "vid": self.url,
                    "_t": int(time.time() * 1000)
                }
                response = session.get(url=link, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    return json.dumps(response.json(), ensure_ascii=False)
                else:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据"}, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
        else:
            vid = str(self.url).split("=")[1]
            link = "https://v.6.cn/minivideo/auth.php"  # https://v.6.cn/minivideo/auth.php?act=play&vid=5384501&_t=1598672338821
            try:
                params = {
                    "act": "play",
                    "vid": vid,
                    "_t": int(time.time() * 1000)
                }
                response = session.get(url=link, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    return json.dumps(response.json(), ensure_ascii=False)
                else:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据"}, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)