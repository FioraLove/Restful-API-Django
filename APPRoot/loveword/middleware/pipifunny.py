# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：皮皮搞笑
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 请求url后，并不能在源代码里找到视频相关信息，真实的视频页面的地址其实就是发送post请求
        http://share.ippzone.com/ppapi/share/fetch_content
"""


class PiPiFunny(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.S)
            deal_url = re.findall(pattern, self.url)[0]
            # 获取处理后的url，获取vid
            mid = re.findall("mid=(\d+)", deal_url, re.S)[0]
            pid = re.findall("pid=(\d+)", deal_url, re.S)[0]

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "Origin": "http://share.ippzone.com",
                "Referer": deal_url,
                "Content-Type": "text/plain;charset=UTF-8"
            }
            data = {
                "mid": int(mid),
                "pid": int(pid),
                "type": "post"
            }
            result = self.session.post(url="https://h5.ippzone.com/ppapi/share/fetch_content", data=json.dumps(data),
                                       headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    # 获取视频真实地址
                    doc = result.json()
                    url = doc['data']['post']['videos'][str(doc['data']['post']['imgs'][0]['id'])]['url']
                    description = doc['data']['post']['content']
                    info = {
                        "title": description,
                        "url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)