# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：6间房
目标url：web网页链接
爬取思路：
    1. 通过APP里的分享获取视频url，网页源代码里获取tid
    2. 对 https://v.6.cn/message/message_home_get_one.php?tid=XXX 发送get请求，获取json数据
    3. 这里使用的是web端链接，没有下载APP，原理都是要先获取tid
"""


class sixRoom(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        try:
            # 获取vid
            tid = ""
            rows = self.session.get(url=deal_url, headers=headers, timeout=10)
            if rows.status_code == 200:
                tid = re.findall("tid: '(\w+)',", rows.text, re.S)[0]
            try:
                params = {
                    "tid": tid
                }
                response = self.session.get(url="https://v.6.cn/message/message_home_get_one.php", headers=headers,
                                            params=params, timeout=10)
                if response.status_code == 200:
                    doc = response.json()
                    info = doc["content"]["content"][0]["content"]
                    title = info["title"]
                    cover = info["url"]
                    video = info["playurl"]
                    msg = {
                        "title": title,
                        "cover": cover,
                        "video_url": video
                    }
                    return json.dumps(msg, ensure_ascii=False)
                else:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)