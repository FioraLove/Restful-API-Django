# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：比心陪练APP
目标url：APP短视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url，获取其timelineId
    2. 对https://h5.hibixin.com/capi/bixin/timeline/shareTimeline发送post请求，获取json数据
"""


class BiXin(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Host": "h5.hibixin.com",
            "Origin": "https://h5.hibixin.com",
            "Content-Type": "application/json"
        }

        pattern = re.compile("dynamic_id=(\w+)", re.S)
        dynamic_id = re.findall(pattern, str(self.url).strip())[0]

        try:
            # 用户的单个视频
            base_url = "https://h5.hibixin.com/capi/bixin/timeline/shareTimeline"
            data = {
                "timelineId": dynamic_id
            }

            response = self.session.post(url=base_url, headers=headers, data=json.dumps(data), timeout=10)
            if response.status_code == 200:
                doc = response.json()
                title = doc["result"]["timelineInfo"]["content"]
                cover = doc["result"]["timelineInfo"]["videoInfoDTO"]["videoFirstImg"]
                video = doc["result"]["timelineInfo"]["videoInfoDTO"]["videoUrl"]
                info = {
                    "title": title,
                    "cover": cover,
                    "video": video
                }
                return json.dumps(info, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)