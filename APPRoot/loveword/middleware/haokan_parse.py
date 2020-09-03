# -*- coding:utf-8 -*-
import requests
import json
import re


class HaoKan(object):
    def __init__(self, url):
        self.url = url

    def get_url(self):
        vid = self.url
        if len(vid) >= 25:
            vid = str(vid).split("=")[1]
        base_url = "https://haokan.baidu.com/v?vid=" + str(vid)
        headers = {
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }
        try:
            response = requests.get(url=base_url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    pattern = re.compile('"clarityUrl":\[(.*?)\]', re.S)
                    res = "[" + re.findall(pattern, response.text)[0] + "]"
                    rows = json.loads(res)
                    items = []
                    for row in rows:
                        items.append(
                            {"key": row.get("key", ""), "title": row.get("title", ""), "video_url": row.get("url", "")})
                    return json.dumps(items, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
