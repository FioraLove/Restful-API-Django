# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：VUE Vlog
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 请求url后，并不能找到视频相关信息，真实的视频页面的地址其实就是在网页源代码
"""


class Vue(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
            deal_url = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36"
            }
            title_pattern = re.compile('<title>(.*?)</title>', re.S)
            cover_pattern = re.compile('<meta name="twitter:image" content="(.*?)">', re.S)
            video_pattern = re.compile('<meta name="twitter:player" content="(.*?)">', re.S)
            result = self.session.get(url=deal_url, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    info = {
                        "title": re.findall(title_pattern, result.text)[0],
                        "cover": re.findall(cover_pattern, result.text)[0],
                        "video_url": re.findall(video_pattern, result.text)[0],
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)