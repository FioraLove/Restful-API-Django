# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：开眼
目标url：视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url，剥离出url中的vid
    2.新的url由"https://baobab.kaiyanapp.com/api/v1/video/(vid拼接出来)"
"""


class OpenEye(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36",
            "referer": "https://www.eyepetizer.net/"
        }
        try:
            # 获取视频id
            pattern = re.compile("vid=(\d+)&", re.S)
            vid = re.findall(pattern, self.url)[0]
            # 真实视频地址
            api = "https://baobab.kaiyanapp.com/api/v1/video/{}".format(vid)
            result = self.session.get(url=api, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    res = result.json()
                    cover = res["coverForFeed"]
                    name = res["title"]
                    video_url = res["playUrl"]
                    info = {
                        "title": name,
                        "cover": cover,
                        "url": video_url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)