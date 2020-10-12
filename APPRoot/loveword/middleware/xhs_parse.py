# -*- coding:utf-8 -*-
import re
import json
import html
import requests

"""
目标APP：小红书
目标url：视频APP分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：http://xhslink.com/xvxMJ
    2. url重定向到真实跳转地址：简化后.,https://www.xiaohongshu.com/discovery/item/5f77dbcf000000000100491c...
"""


class XiaoHongShu(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "Host": "xhslink.com",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36"
        }
        source_headers = {
            "cookie": "xhsTrackerId=6e8cc536-0d57-4226-c27c-831a6e51c4cc; "
                      "Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1593488621,1593488692,1593488706; "
                      "xhsTracker=url=noteDetail&xhsshare=CopyLink; extra_exp_ids=gif_exp1,ques_exp1; "
                      "xhsuid=6KOIxzWIclOk5WsI; timestamp2=20201012ef45ffd4004e2dcc5b3efb33; "
                      "timestamp2.sig=Jr645nmjd1yv_OKiCv2Sv63XInSbvHfSrB57YdkppLg; xhs_spses.5dde=*; "
                      "xhs_spid.5dde=05e7787428e31fd4.1593488621.4.1602469704.1593498973.7788de5a-9875-44ab-9ac0"
                      "-200218254fbe ",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36"
        }
        try:
            # 处理url
            # 获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.S)
            deal_url = re.findall(pattern, self.url)[0]

            response = self.session.get(url=deal_url, headers=headers, allow_redirects=False, timeout=10)
            # 获取重定向后的简化url
            base_url = response.headers.get("Location")

            result = self.session.get(url=base_url, headers=source_headers, timeout=10)
            pattern_video = re.compile('<video .*? src="(.*?)".*?></video>', re.S)
            pattern_desc = re.compile('"description": "(.*?)",', re.S)

            if result.status_code == 200:
                try:
                    res = result.text
                    url = re.findall(pattern_video, res)[0]
                    description = re.findall(pattern_desc, res)[0]
                    info = {
                        "description": description,
                        "url": html.unescape(url)
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)