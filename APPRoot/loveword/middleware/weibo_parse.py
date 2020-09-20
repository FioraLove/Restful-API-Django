# -*- coding:utf-8 -*-
import requests
import json


class WeiBo(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        page = self.url.split("com")[1]
        vid = self.url.split("/")[-1]
        headers = {
            "origin": "https://weibo.com",
            "content-type": "application/x-www-form-urlencoded",
            "page-referer": str(page),
            "referer": self.url,
            # cookie必不可少重要
            "cookie":"SINAGLOBAL=1676767636636.8135.1597547191918; "
                     "SUB=_2AkMoBwW2f8NxqwJRmfgWzmjqb451zAvEieKeW_RtJRMxHRl"
                     "-yT9jqncotRB6A4crWXIm3ORTaVsOY_asOIe9wj8joIsm; "
                     "SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF46Ukknmd-Dmn5_D5YP8ws; "
                     "TC-V-WEIBO-G0=35846f552801987f8c1e8f7cec0e2230; _s_tentry=www.baidu.com; UOR=,,www.baidu.com; "
                     "Apache=6228607677168.163.1600579087592; "
                     "ULV=1600579087732:4:3:1:6228607677168.163.1600579087592:1600518702433; "
                     "XSRF-TOKEN=ctEUr6zk0bNzx3ZzgSw_kbaD; login_sid_t=76155e701a33c5709e5a86baa50b7266; "
                     "cross_origin_proto=SSL; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; "
                     "TC-V5-G0=799b73639653e51a6d82fb007f218b2f; WBStorage=70753a84f86f85ff|undefined; "
                     "wb_view_log=1536*8641.25",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/84.0.4147.125 Safari/537.36 "
        }
        params = {
            "page": str(page)
        }
        data = {
            "data": json.dumps({
                "Component_Play_Playinfo": {"oid": vid}
            })
        }
        base_url = "https://weibo.com/tv/api/component"
        try:
            response = self.session.post(url=base_url, params=params, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    result = (response.json())["data"]["Component_Play_Playinfo"]
                    author = result["author"]
                    cover = result["cover_image"]
                    title = result["title"]
                    urls = result["urls"]
                    info = {"author": author,
                            "title": title,
                            "cover": cover,
                            "urls": urls}
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)