# -*- coding:utf-8 -*-
import json
import requests


class BiLiStat(object):
    def __init__(self, vmid):
        self.vmid = vmid
        self.session = requests.Session()
        self.headers = {
            "origin": "https://space.bilibili.com",
            # "referer": "https://space.bilibili.com/215893581/favlist",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }

    def get_stat(self):
        api_stat = "https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(self.vmid)
        try:
            response = self.session.get(url=api_stat, headers=self.headers, timeout=5)
            if response.status_code == 200:
                result = response.json()
                flowers = result["data"]["follower"]
                following = result["data"]["following"]
                return flowers, following
        except Exception as e:
            print(e)

    def get_upstat(self):
        api_upstat = "https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp".format(self.vmid)
        try:
            response = self.session.get(url=api_upstat, headers=self.headers, timeout=5)
            if response.status_code == 200:
                result = response.json()
                read = result["data"]["archive"]["view"]
                article = result["data"]["article"]["view"]
                likes = result["data"]["likes"]
                return read, article, likes
        except Exception as e:
            print(e)

    def run(self):
        _0x110, _0x120 = self.get_stat()
        _0b9527, _0b4396, _0b2200 = self.get_upstat()
        info = {
            "flowers": _0x110,
            "following": _0x120,
            "read": _0b9527,
            "article": _0b4396,
            "likes": _0b2200
        }
        return info


if __name__ == '__main__':
    stat = BiLiStat("215893581")
    stat.run()
