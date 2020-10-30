# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：皮皮虾
目标url：视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：https://h5.pipix.com/s/JAtW8Yg/
    2. url重定向到真实跳转地址：简化后.,https://h5.pipix.com/item/6869230768778909965
    3. 但真正视频地址确是在get请求中（误打误撞，发现里不加水印的视频地址）
        - 加水印：https://h5.pipix.com/bds/webapi/item/detail/?item_id=6869230768778909965&source=share
        - 不加水印：https://h5.pipix.com/bds/webapi/item/detail/?item_id=6869230768778909965 （PS：少了一个参数）
    4. 整理的API：
        - 用户信息：https://is-hl.snssdk.com/bds/user/user_profile/?user_id=1261832096452716（user-agent必须为mobile端）
"""


class PiPiXia(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36 "
        }
        try:
            response = self.session.get(url=self.url, headers=headers, timeout=10)
            # 获取重定向后的简化url
            base_url = str(response.url).strip().split("?app")[0]
            # 获取视频id
            pattern = re.compile("/(\d+)", re.S)
            vid = re.findall(pattern, base_url)[0]
            # 真实视频地址
            api = "https://h5.pipix.com/bds/webapi/item/detail/"
            params = {
                "item_id": vid
            }
            result = self.session.get(url=api, params=params, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    res = result.json()
                    title = res["data"]["item"]["content"]
                    url = res["data"]["item"]["video"]["video_download"]["url_list"][0]["url"]
                    name = res["data"]["item"]["author"]["name"]
                    description = res["data"]["item"]["author"]["description"]
                    info = {
                        "title": title,
                        "name": name,
                        "description": description,
                        "url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
