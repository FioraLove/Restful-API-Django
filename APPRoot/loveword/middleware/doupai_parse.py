# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：逗拍
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 对https://v2.doupai.cc/topic/XXXXXX.json发送post请求，获取json数据
"""


class DouPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile('(http[s]?://[^\s]+)', re.S)
            deal_url = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "origin": "https://p.doupai.cc"
            }
            # 获取vid
            vid = re.findall("topic/(.*?).html", deal_url, re.S)[0]
            base_url = "https://v2.doupai.cc/topic/{}.json".format(vid)
            result = self.session.get(url=base_url, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    doc = result.json()
                    url = doc["data"]["videoUrl"]
                    title = doc["data"]["name"]
                    cover = doc["data"]["imageUrl"]
                    info = {
                        "title": title,
                        "cover": cover,
                        "video_url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)