# -*- coding:utf-8 -*-
import requests
import json
import re

"""
目标APP：腾讯微视
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 请求url后，并不能找到视频相关信息，真实的视频页面的地址其实就是在url后面加上查询字符串 “&from=pc&orifrom=”
"""


class WeiShi(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.S)
            deal_url = re.findall(pattern, self.url)[0]
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "referer": deal_url
            }
            api = (str(deal_url) + "&from=pc&orifrom=")
            result = self.session.get(url=api, headers=headers, timeout=10)
            pattern_video = re.compile('"video_url":"(.*?)",', re.S)
            pattern_summary = re.compile('"weibo_summary":"(.*?)",', re.S)
            pattern_cover = re.compile('"weibo_pic_url":"(.*?)"', re.S)
            if result.status_code == 200:
                try:
                    res = result.text
                    url = re.findall(pattern_video, res)[0]
                    summary = re.findall(pattern_summary, res)[0]
                    cover = re.findall(pattern_cover, res)[0]
                    info = {
                        "summary": summary,
                        "cover": cover,
                        "video_url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
