# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：抖音（Ⅱ）
目标url：APP视频分享链接
爬取思路：
    1. 抖音短视频解析第二版：共发送两次重定向，一次get请求
    2. 机缘巧合，发现一篇csdn文章：https://blog.csdn.net/qq_44700693/article/details/108089085
      同【皮皮搞笑】，url中带有‘wm’表示有水印。删除wm后，必须模拟手机端的请求头
        - 有水印：https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f750000bsegsdpphaglno4mqd8g&ratio=720p&line=0
        - 无水印：https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200f750000bsegsdpphaglno4mqd8g&ratio=720p&line=0
    3. item_ids为APP分享的链接跳转后的url查询字符串
"""


class DouYin2(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        pc_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36"
        }
        oa_headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 "
        }
        try:
            # 处理url,获取视频id
            pattern = re.compile('(http[s]?://[^\s]+)', re.S)
            deal_url = re.findall(pattern, self.url)[0]
            # 第一重次定向，获取重定向后的简化url
            response = self.session.get(url=deal_url, headers=pc_headers, timeout=10)
            base_url = response.url
            # 获取跳转url中的item_ids
            item_ids = re.findall("/(\d+)/", base_url, re.S)[0]
            # 发送get请求，获取视频json数据
            api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}".format(item_ids)
            result = self.session.get(url=api, headers=pc_headers, timeout=10)
            if result.status_code == 200:
                try:
                    doc = result.json()
                    res = doc["item_list"][0]
                    title = res["desc"]
                    cover = res["video"]["origin_cover"]["url_list"][-1]
                    play_addr = res["video"]["play_addr"]["url_list"][-1]
                    quality = res["video"]["ratio"]
                    # 再次重定向获取真实视频url
                    rows = self.session.get(url=str(play_addr).replace("playwm", "play"), headers=oa_headers,
                                            timeout=10)
                    if rows.status_code == 200:
                        info = {
                            "title": title,
                            "cover": cover,
                            "quality": quality,
                            "video_url": rows.url
                        }
                        return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)