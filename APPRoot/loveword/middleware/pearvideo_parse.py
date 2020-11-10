# -*- coding:utf-8 -*-
import re
import json
import random
import requests

"""
目标APP：梨视频
目标url：APP视频分享链接或web链接
爬取思路：
    1. 通过APP里的分享获取视频的feedid
    2. 对真实数据地址发送get请求
        - https://www.pearvideo.com/videoStatus.jsp
    4. 返回的json里的视频地址并不是真实是地址
        - json返回的url：https://video.pearvideo.com/mp4/adshort/20201109/时间戳-15473378_adpkg-ad_hd.mp4
        - 真实时评url：https://video.pearvideo.com/mp4/adshort/20201109/cont-1706046-15473378_adpkg-ad_hd.mp4
"""


class PearVideo(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.pearvideo.com",
            "Referer": deal_url,
            "X-Requested-With": "XMLHttpRequest"
        }
        pattern = re.compile("_(\d+)", re.S)
        try:
            feedid = re.findall(pattern, deal_url)[0]
            # 用户的单个视频
            base_url = "https://www.pearvideo.com/videoStatus.jsp?contId={}&mrd={}".format(feedid, random.random())
            response = self.session.get(url=base_url, headers=headers, timeout=10)
            if response.status_code == 200:
                doc = response.json()
                video = doc["videoInfo"]["videos"]["srcUrl"]
                cover = doc["videoInfo"]["video_image"]
                timer = doc["systemTime"]
                # 处理视频url，替换错误字符
                video_url = str(video).replace(timer, "cont-" + feedid)
                info = {
                    "title": "为增强程序的轻便性，暂不提供标题",
                    "cover": cover,
                    "video": video_url
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)