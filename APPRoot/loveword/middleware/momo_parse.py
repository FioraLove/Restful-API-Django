# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：陌陌
目标url：APP分享链接或web网页端
爬取思路：
    1. 通过APP里的分享获取视频url，获取其feedid
    2. 对https://m.immomo.com/inc/microvideo/share/profiles发送post请求，获取json数据
"""


class MoMo(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Host": "m.immomo.com",
            "Origin": "http://m.immomo.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # 处理url，获取视频id
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]

        # 获取mobile端feedid
        pattern = re.compile("v2/(.*?).htm", re.S)
        vid_list = re.findall(pattern, deal_url)
        if len(vid_list) < 1:
            # 获取PC端时的feedid
            feedid = re.findall("momentids=(\w+)", deal_url, re.S)[0]
        else:
            feedid = vid_list[0]

        try:
            # 用户的单个视频
            base_url = "https://m.immomo.com/inc/microvideo/share/profiles"
            """
            目标用户的所有视频的api：https://m.immomo.com/inc/microvideo/share/getUserVideos 
            data = {"feedids":"at8984164801"}
            """
            data = {
                "feedids": feedid,
                "name": "",
                "avatar": ""
            }
            response = self.session.post(url=base_url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                doc = response.json()
                title = doc["data"]["list"][0]["content"]
                location = doc["data"]["list"][0]["video"]["city"]
                cover = doc["data"]["list"][0]["video"]["cover"]["l"]
                video = doc["data"]["list"][0]["video"]["video_url"]
                info = {
                    "title": title,
                    "city": location,
                    "cover": cover,
                    "video": video
                }
                return json.dumps(info, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)