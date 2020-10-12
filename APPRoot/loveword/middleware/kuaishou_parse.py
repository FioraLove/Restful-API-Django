# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：快手
目标url：视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：https://v.kuaishou.com/5FGpDa
    2. url重定向到真实跳转地址：简化后.,https://c.kuaishou.com/fw/photo/3xzn3vrwrvigtui?fid=2096594305...
"""


class KuaiShou(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 "
        }
        try:
            # 处理url
            # 获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
            deal_url = re.findall(pattern, self.url)[0]

            response = self.session.get(url=deal_url, headers=headers, timeout=10)
            # 获取重定向后的简化url
            base_url = response.url
            result = self.session.get(url=base_url, headers=headers, timeout=10)
            pattern_video = re.compile('"src":"(.*?)",', re.S)
            pattern_title = re.compile('"caption":"(.*?)",', re.S)
            pattern_cover = re.compile('"poster":"(.*?)",', re.S)
            if result.status_code == 200:
                try:
                    res = result.text
                    url = re.findall(pattern_video, res)[0]
                    description = re.findall(pattern_title, res)[0]
                    cover = re.findall(pattern_cover, res)[0]
                    info = {
                        "description": description,
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