# -*- coding:utf-8 -*-
import requests
import json
import re
from lxml import etree


class PearVideo(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.pearvideo.com"
        }
        pattern = re.compile("_\d+", re.S)
        try:
            feedid = re.findall(pattern, self.url)[0]
            # 用户的单个视频
            base_url = "https://www.pearvideo.com/video"+str(feedid)
            response = self.session.get(url=base_url, headers=headers, timeout=10)
            if response.status_code == 200:
                pattern2 = re.compile('srcUrl="(.*?)"', re.S)
                video_url = re.findall(pattern2, response.text)[0]
                # xpath初始化
                html = etree.HTML(response.text)
                title = html.xpath(".//h1[@class='video-tt']/text()")
                info = {
                    "title": title[0],
                    "video": video_url
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
