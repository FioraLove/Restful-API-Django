# -*- coding:utf-8 -*-
import requests
import time
import json
import hashlib

"""
目标APP：小咖秀
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：https://mobile.xiaokaxiu.com/video?id=6552159704691249152
    2. 通过id发送Ajax请求：https://appapi.xiaokaxiu.com/api/v1/web/share/video/视频id?time=时间戳
    3. 请求头headers里的x-sign签名算法必不可少

x-sign签名算法原理：
    1. 全局搜索x-sign，可以发现两个文件：
        - axios.js：
            str = md5(str)
            config.headers['X-Sign'] = str
        - app.d82b2f62.js：
            var t = (new Date).valueOf();
            t = String(t).substring(0, 10);
            var n = ""
              , r = "";
            if (n = "S14OnTD#Qvdv3L=3vm",
            e.url = "https://appapi.xiaokaxiu.com" + e.url + "?time=" + t,
            e.params) {
                var i = JSON.parse(o()(e.params));
                i.time = t,
                r = n + "&" + f(i)
            } else {
                var c = {};
                c.time = t,
                r = n + "&" + f(c)
            }
            return r = m()(r)

签名算法总结：字符串由固定字符”S14OnTD#Qvdv3L=3vm“ 加上 固定字符”&“ 加上 ”十位的时间戳“，最后将完整的字符串进行md5加密
"""


class XiaoKaXiu(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        try:
            # 处理url,获取视频id
            vid = (self.url).split("=")[1]
            deal_url = "https://appapi.xiaokaxiu.com/api/v1/web/share/video/{}".format(str(vid))
            timer = int(time.time())
            # 处理md5
            x_sign = "S14OnTD#Qvdv3L=3vm&time=" + str(timer)
            md = hashlib.md5()
            md.update(x_sign.encode("utf-8"))
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "origin": "https://mobile.xiaokaxiu.com",
                "referer": "https://mobile.xiaokaxiu.com/",
                "x-sign": str(md.hexdigest())
            }
            params = {
                "time": str(timer)
            }
            response = self.session.get(url=deal_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                try:
                    res = response.json()
                    doc = res["data"]["video"]
                    title = doc["title"]
                    cover = doc["cover"]
                    video_url = doc["url"][-1]
                    info = {
                        "title": title,
                        "cover": cover,
                        "url": video_url
                    }

                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
