# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：快手
目标url： APP视频分享链接/web端
爬取思路：
  - APP端：
    1. 通过APP里的分享获取视频url：https://v.kuaishou.com/5FGpDa
    2. url重定向到真实跳转地址：简化后.,
        "https://c.kuaishou.com/fw/photo/3xbjz7dvcx6qj3a?fid=2096594305&cc=share_copylink&followRefer=151&photoId=3xbjz7dvcx6qj3a&userId=3xkvt27kw2i6xbe"
    3. 提取重定向后的url地址中的photoId的值
    4. 对 https://video.kuaishou.com/graphql发送post请求，目标数据就在返回的json数据中
  - WEB端：
    1. web端的url形如：https://video.kuaishou.com/short-video/3x39cpt7868qp2i?authorId=3xk4tvmdvq72fqs&streamSource=find
"""


class KuaiShou(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            'content-type': 'application/json',
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 "
        }
        try:
            pattern = re.compile(r'(http[s]?://[^\s]+)', re.S)
            deal_url = re.findall(pattern, self.url)[0]
            # 处理url,获取视频id
            if len(deal_url) >= 36:
                photo_id = re.findall("video\/(.*?)\?", self.url, re.S)[0]
                headers["Host"] = "video.kuaishou.com"
                headers["Origin"] = "https://video.kuaishou.com"
                headers["Referer"] = deal_url
            else:
                response = self.session.get(url=deal_url, headers=headers, timeout=10)
                # 正则匹配提取photoId
                photo_id = re.findall("photoId=(.*?)&", response.url, re.S)[0]
            api = "https://video.kuaishou.com/graphql"
            data = {
                "operationName": "visionVideoDetail",
                "variables": {"photoId": "{}".format(photo_id), "page": "selected"},
                "query": "query visionVideoDetail($photoId: String, $type: String, $page: String) {\n  "
                         "visionVideoDetail(photoId: $photoId, type: $type, page: $page) {\n    status\n    type\n    "
                         "author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n "
                         "   photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n "
                         "     coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n    "
                         "  __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    "
                         "commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    __typename\n  "
                         "}\n}\n "
            }
            result = self.session.post(url=api, headers=headers, data=json.dumps(data), timeout=10)
            if result.status_code == 200:
                try:
                    res = result.json()
                    name = res["data"]["visionVideoDetail"]["author"]["name"]
                    description = res["data"]["visionVideoDetail"]["photo"]["caption"]
                    cover = res["data"]["visionVideoDetail"]["photo"]["coverUrl"]
                    duration = res["data"]["visionVideoDetail"]["photo"]["duration"]
                    like_count = res["data"]["visionVideoDetail"]["photo"]["likeCount"]
                    video_url = res["data"]["visionVideoDetail"]["photo"]["photoUrl"]
                    info = {
                        "author": name,
                        "description": description,
                        "duration": duration,
                        "like_count": like_count,
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