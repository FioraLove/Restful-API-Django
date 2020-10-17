# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：轻视频【哔哩哔哩旗下短视频平台】
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：https://bbq.bilibili.com/video/?id=1595388070040635173
    2. 对https://bbq.bilibili.com/bbq/app-bbq/sv/detail发送get请求获取数据
"""


class QinShiPin(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        # 处理url,获取视频id
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 ",
            "referer": str(deal_url)
        }
        try:
            # 获取vid
            vid = str(deal_url).split("=")[1]
            base_url = "https://bbq.bilibili.com/bbq/app-bbq/sv/detail"
            params = {
                "svid": vid,
                "version": "1.3.0",
                "platform": "h5"
            }
            response = self.session.get(url=base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                try:
                    res = response.json()
                    url = res["data"]["play"]["url"]
                    title = res["data"]["title"]
                    cover = res["data"]["cover_url"]
                    views = res["data"]["view"]
                    info = {
                        "title": title,
                        "cover": cover,
                        "video_url": url,
                        "views": views
                    }

                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)