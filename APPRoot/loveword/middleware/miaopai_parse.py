# -*- coding:utf-8 -*-
import requests
import re
import json

"""
目标网站：秒拍APP
目标url：APP分享链接
注意点： 视频链接有效性只有一个小时
"""


class MiaoPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "Host": "n.miaopai.com",
            "Referer": self.url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36 "
        }
        # 获取smid
        smid = str(self.url).replace(".htm", "").split("/")[-1]
        params = {
            "smid": smid,
            "appid": 530,
            "_cb": "_jsonpnyyqvhx3q4"
        }
        base_url = "http://n.miaopai.com/api/aj_media/info.json"
        try:
            response = self.session.get(url=base_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                try:
                    doc = response.text
                    # 处理成标准的json
                    result = doc.replace("window._jsonpnyyqvhx3q4 && _jsonpnyyqvhx3q4(", "").replace(");", "")
                    res = json.loads(result, encoding="utf-8")
                    desc = res["data"]["description"]
                    cover = res["data"]["meta_data"][0]["pics"]["l"]
                    video = res["data"]["meta_data"][0]["play_urls"]["l"]
                    views_count = res["data"]["meta_data"][0]["views_count"]
                    author = res["data"]["user"]["nick"]
                    info = {
                        "title": desc,
                        "author": author,
                        "cover": cover,
                        "video_url": video,
                        "views_count": views_count,
                        "notes": "视频链接有效性只有一个小时,请及时惠存"
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
