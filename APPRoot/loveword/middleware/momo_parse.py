# -*- coding:utf-8 -*-
import requests
import json
import re


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
        pattern = re.compile("at\d+|ak\d+", re.S)
        try:
            feedid = re.findall(pattern, self.url)[0]
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
                user = doc["data"]["list"][0]["user"]
                video = doc["data"]["list"][0]["video"]["video_url"]
                info = {
                    "title": title,
                    "user": user,
                    "video": video
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)