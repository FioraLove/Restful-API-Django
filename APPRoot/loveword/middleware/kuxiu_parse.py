# -*- coding:utf-8 -*-
import re
import json
import time
import random
import hashlib
import requests

"""
目标APP：酷秀短视频
目标url：APP视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url
    2. 对 https://api.17kuxiu.com/dynamic/video/detail/guest 发送post请求，获取json数据
    3. 尤其是注意headers里的校验，post请求源代码：
    getParams: function(){
        var userId = fetchQueryString("userId") || '2355676';
        this.pubId = fetchQueryString("pubId") || 0;
        var secretKey = "792f28d6ff1f34ec702c08626d454b39";
        var timeRequest = fetchTimeStamp(), imei = fetchUUid();
        var _this = this;
        $.ajax({
        type: 'POST',
        contentType: "application/json;charset=UTF-8",
        url: apiUrl + '/dynamic/video/detail/guest',
        headers: {
            requestId: $.md5("web" + imei + timeRequest + secretKey).toString(),
            timestamp: timeRequest,
            version: '1.0.0',
            imei,
            os: 'web',
            mobileModel: 'web',
            loginType: 2,
            userId: userId
        },
        data: JSON.stringify({
            "latitude": 0,
            "longitude": 0,
            "pubId": this.pubId
        }),
        success: function(res){
            if(res.retCode == 200){

        }
    }  
"""


class KuXiu(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    @staticmethod
    def get_uid():
        return hex(int((1 + random.random()) * 65536) | 0)[3:]

    def parse(self):
        try:
            # 处理url，获取视频id
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 re.S)
            deal_url = re.findall(pattern, self.url)[0]
            # 获取mei
            mei = self.get_uid() + self.get_uid() + "-" + self.get_uid() + "-" + self.get_uid() + "-" + \
                  self.get_uid() + "-" + self.get_uid() + self.get_uid() + self.get_uid()

            # 获取十三位时间戳
            timer = str(int(time.time() * 1000))

            # 获取requestid
            h1 = hashlib.md5()
            keys = "web"+str(mei)+timer+"792f28d6ff1f34ec702c08626d454b39"
            h1.update(keys.encode("utf-8"))
            request_id = h1.hexdigest()

            # 获取vid
            vid = re.findall("pubid=(\w+)", deal_url, re.S)[0]

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36",
                "mobileModel": "web",
                "os": "web",
                "userId": "2355676",
                "loginType": "2",
                "version": "1.0.0",
                "timestamp": timer,
                "imei": mei,
                "Content-Type": "application/json;charset=UTF-8",
                "requestId": request_id,
            }

            base_url = "https://api.17kuxiu.com/dynamic/video/detail/guest"
            data = {
                "latitude": 0,
                "longitude": 0,
                "pubId": vid
            }
            result = self.session.post(url=base_url, data=json.dumps(data), headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    doc = result.json()
                    avatar = doc["data"]["avatarUrl"]
                    title = doc["data"]["text"]
                    cover = doc["data"]["video"]["videoCoverUrl"]
                    video = doc["data"]["video"]["videoUrl"]
                    address = doc["data"]["address"]
                    info = {
                        "title": title,
                        "avatar": avatar,
                        "address": address,
                        "cover": cover,
                        "video_url": video
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)