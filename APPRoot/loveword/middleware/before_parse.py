# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：Before避风 【快手旗下】
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 对 https://hlg.xiatou.com/h5/feed/detail 发送get请求，获取json数据
"""


class Before(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.S)
            deal_url = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "origin": "https://m.hanyuhl.com",
                "Referer": "https://m.hanyuhl.com/"
            }
            # 获取vid
            vid = re.findall("detail/(\d+)", deal_url, re.S)[0]
            base_url = "https://hlg.xiatou.com/h5/feed/detail"
            params = {
                "id": vid
            }
            result = self.session.get(url=base_url, params=params, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    doc = result.json()
                    url = doc["data"][0]["mediaInfoList"][0]["videoInfo"]["url"]
                    title = doc["data"][0]["title"]
                    cover = doc["data"][0]["cover"][0]["url"]
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