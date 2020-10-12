# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标url：https://www.vmovier.com/
实现功能：解析出视频url
"""


class ChangKuVideo(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        api_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                          "/84.0.4147.125 Safari/537.36",
            "referer": self.url,
            "origin": "https://www.xinpianchang.com",
            "content-type": "application/json"
        }
        home_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                          "/84.0.4147.125 Safari/537.36",
            "upgrade-insecure-requests": "1"
        }

        key_pattern = re.compile('var modeServerAppKey = "(.*?)";', re.S)
        vid_pattern = re.compile('var vid = "(.*?)";', re.S)
        try:
            # 获取视频的post请求地址
            home_url = str(self.url).strip()
            response = self.session.get(url=home_url, headers=home_headers, timeout=10)
            if response.status_code == 200:
                key = re.findall(key_pattern, response.text)[0]
                vid = re.findall(vid_pattern, response.text)[0]
                # 组建完整的url
                base_url = "https://mod-api.xinpianchang.com/mod/api/v2/media/{}".format(vid)
                params = {
                    "appKey": key,
                    "extend": "userInfo,userStatus"
                }
                try:
                    result = self.session.get(url=base_url, params=params, headers=api_headers, timeout=10)
                    if result.status_code == 200:
                        doc = result.json().get("data")
                        cover = doc["cover"]
                        desc = doc["description"]
                        title = doc["title"]
                        videos = doc["resource"]["progressive"]
                        video = []
                        for i in videos:
                            info = {
                                "profile": i["profile"],
                                "url": i["url"]
                            }
                            video.append(info)
                        res = {
                            "cover": cover,
                            "desc": desc,
                            "title": title,
                            "videos": video
                        }
                        return json.dumps(res, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
