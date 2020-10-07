# -*- coding:utf-8 -*-
import requests
import re
import json
import base64

"""
目标网站：西瓜视频
目标url：APP分享链接或web网页url
注意点：西瓜视频与哔哩哔哩都将音视频分割开了，用户只有使用剪辑软件自己拼接
"""


class XiGua(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36 "
        }
        pattern_video = re.compile('"dynamic_video_list":\[(.*?)\],', re.S)
        pattern_audio = re.compile('"dynamic_audio_list":\[(.*?)\],', re.S)
        pattern_desc = re.compile('<meta data-react-helmet="true" name="description" content="(.*?)"/>', re.S)
        try:
            response = self.session.get(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    doc = response.text
                    desc = re.findall(pattern_desc, doc)[0]
                    videos = json.loads("[" + re.findall(pattern_video, doc)[0] + "]")
                    audios = json.loads("[" + re.findall(pattern_audio, doc)[0] + "]")
                    # 选择清晰度最高的那个音视频
                    quality = videos[-1]["definition"]
                    video_url = base64.b64decode(videos[-1]["main_url"])
                    audio_url = base64.b64decode(audios[-1]["main_url"])
                    title = desc.encode('raw_unicode_escape').decode()
                    info = {
                        "title": title.split("西瓜视频为您")[0],
                        "quality": quality,
                        "video_url": video_url.decode("utf-8"),
                        "audio_url": audio_url.decode("utf-8"),
                        "description": "api会优先选择视频清晰度最高的音视频源；西瓜视频的音视频是分离开的，请搭配使用剪辑软件拼接音视频源"
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)