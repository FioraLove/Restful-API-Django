# -*- coding:utf-8 -*-
import re
import json
import requests
from pyquery import PyQuery as pq

"""
目标APP：绿洲短视频【微博旗下】
目标url：APP视频分享链接
难度系数: ★
爬取思路:
    1. 通过APP里的分享获取视频url
    2. 请求url后，真实的视频页面的地址其实就是在网页源代码
"""


class LvZhou(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile('(http[s]?://[^\s]+)', re.S)
            deal_url = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36"
            }

            result = self.session.get(url=deal_url, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    # 获取视频真实地址
                    doc = pq(result.text)
                    url = doc("video").attr("src")
                    title = doc(".content .title").text()
                    summary = doc(".content .text").text()
                    cover = doc(".video-container div:first-child").attr("style")
                    info = {
                        "title": title,
                        "cover": re.findall('(http[s]?://[^\s]+)', str(cover).split(")")[0], re.S)[0],
                        "url": url,
                        "summary": summary
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)