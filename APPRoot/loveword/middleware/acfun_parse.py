# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：AcFun
目标url：视频分享链接
"""


class AcFun(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 "
        }
        try:

            # 获取视频id
            pattern_url = re.compile(r'"playUrls":\["(.*?)".*?\],', re.S)
            pattern_title = re.compile('var title = "(.*?)";', re.S)

            result = self.session.get(url=self.url, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    doc = result.text
                    # print(doc)
                    title = re.findall(pattern_title, doc)[0]
                    url = re.findall(pattern_url, doc)[0]
                    info = {
                        "title": title,
                        "url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    print(e)
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)