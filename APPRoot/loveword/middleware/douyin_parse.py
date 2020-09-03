# -*- coding:utf-8 -*-
import json
import re
import execjs
import warnings
import requests
from lxml import etree
warnings.filterwarnings('ignore')


class DouYin(object):

    def __init__(self, uid):
        self.uid = uid
        self.user_url = 'https://www.amemv.com/share/user/{}'
        self.video_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/'
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        self.ios_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1'
        }
        with open('static/loveword/js/encrypt.js', 'r', encoding='utf-8') as f:
            resource1 = f.read()

        self.ctx = execjs.compile(resource1)
        self.font_dict = {" &#xe603; ": "0", " &#xe60d; ": "0", " &#xe616; ": "0",
                          " &#xe602; ": "1", " &#xe60e; ": "1", " &#xe618; ": "1",
                          " &#xe605; ": "2", " &#xe610; ": "2", " &#xe617; ": "2",
                          " &#xe604; ": "3", " &#xe611; ": "3", " &#xe61a; ": "3",
                          " &#xe606; ": "4", " &#xe60c; ": "4", " &#xe619; ": "4",
                          " &#xe607; ": "5", " &#xe60f; ": "5", " &#xe61b; ": "5",
                          " &#xe608; ": "6", " &#xe612; ": "6", " &#xe61f; ": "6",
                          " &#xe60a; ": "7", " &#xe613; ": "7", " &#xe61c; ": "7",
                          " &#xe60b; ": "8", " &#xe614; ": "8", " &#xe61d; ": "8",
                          " &#xe609; ": "9", " &#xe615; ": "9", " &#xe61e; ": "9"}

    '''外部调用'''

    def run(self):
        try:
            response = self.session.get(self.user_url.format(self.uid), headers=self.headers)
            html = response.text
            for key, value in self.font_dict.items():
                if key in html:
                    html = html.replace(key, value)
            assert 'dytk' in html
            dytk = re.findall(r"dytk: '(.*?)'", html)[0]
            tac = re.findall(r"<script>tac='(.*?)'</script>", html)[0]
            html = etree.HTML(html)
            nickname = html.xpath('//p[@class="nickname"]/text()')[0]
            douyinid = ''.join(html.xpath('//p[@class="shortid"]/i/text()'))
            num_followers = ''.join(html.xpath('//span[@class="follower block"]/span[1]//text()')).strip()
            num_videos = ''.join(html.xpath('//div[@class="user-tab active tab get-list"]/span/i/text()'))

            try:
                # 获取signature
                signature = self.ctx.call('get_sign', self.uid, tac, self.headers['User-Agent'])
                # 获取视频作品列表
                params = {
                    'user_id': self.uid,
                    'sec_uid': '',
                    'count': '1000',
                    'max_cursor': '0',
                    'aid': '1128',
                    '_signature': signature,
                    'dytk': dytk
                }
                response = self.session.get(self.video_url, headers=self.headers, params=params)
                response_json = response.json()
                all_items = response_json['aweme_list']
                # 开始下载
                douyin_list = []
                for item in all_items:
                    savename = item['desc']
                    download_url = item['video']['play_addr']['url_list'][0]
                    douyin_list.append({"标题": savename, "视频地址": download_url})
                results = {
                    "昵称": nickname,
                    "抖音ID": douyinid,
                    "粉丝数量": num_followers,
                    "作品数量": num_videos,
                    "作品地址": douyin_list
                }
                return json.dumps(results, ensure_ascii=False)

            except Exception as e:
                return json.dumps({"info": str(e)}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "[Warning]: 用户ID输入可能有误, 请重新输入.同一用户ID多次输入确认." + str(e)}, ensure_ascii=False)
