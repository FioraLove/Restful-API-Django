# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：虎牙直播
目标url：APP/web端 视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 请求url后，并不能找到视频相关信息，真实的视频页面的地址：
        https://liveapi.huya.com/moment/getMomentContent?videoId=XXXXXXX
"""


class HuYa(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile("/(\d+).html", re.S)
            vid = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "referer": "https://v.huya.com/"
            }
            params = {
                "videoId": str(vid)
            }
            api = "https://liveapi.huya.com/moment/getMomentContent"
            result = self.session.get(url=api, params=params, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    res = result.json()
                    url = res["data"]["moment"]["videoInfo"]["definitions"][0]["url"]
                    cover = res["data"]["moment"]["videoInfo"]["videoCover"]
                    title = res["data"]["moment"]["videoInfo"]["videoTitle"]
                    info = {
                        "summary": title,
                        "cover": cover,
                        "url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)