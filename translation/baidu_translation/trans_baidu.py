# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : trans_baidu.py
# Time       ：2022/11/9 16:52
# Author     ：Flynn
# version    ：python 3
# Description：
"""


# 未完成代码，acs token 待破解
# 1.第一次请求会得到token值  https://fanyi.baidu.com/
import requests
import execjs
session = requests.session()


class Baidu():
    def __init__(self, query):
        self.query = query
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Acs-Token": "1667977391114_1668062750002_KvQ+dbkRvZAAMQyW7YddNOTbB+KTlgwFzV5KKHukMve3nmKXmz3t+xuOr9lu9SEve1CFlg7V3wwVMPyYFYshZ3jHh/SlFWcYUevs3Vpq586hiQUSFYvvbE5jIIGExKMTOX6X+CFtBEgGcBi51pOAnhHzH7/UPj+hq3ATZkAgfOSKJPZa2ivFzm7prFUJoh59LnHOgpWI7bjOD8kucpS2+lNRCxWGz9SFgv+F3rfgO2W4bgn7qWQL7LuPIhQL3MDjEomqEGpyONtfvqZDlgpB1yZSTKhdA8i7D30Uyfe+NrFfjRhe0BzZsrLGVNJN6ydeHkAVf8omiw7zoi9XjErA/A==",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://fanyi.baidu.com",
            "Pragma": "no-cache",
            "Referer": "https://fanyi.baidu.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.index_url = "https://fanyi.baidu.com/"
        self.url = "https://fanyi.baidu.com/v2transapi"
        # 语言检测
        self.params = {
            "from": "en",
            "to": "zh"
        }

    def get_data_by_javascript(self):
        """
        调用js代码解密sign
        :return:
        """
        with open('baidu.js', 'r', encoding='utf-8') as f:
            baidu_js = f.read()
        sign = execjs.compile(baidu_js).call('e', self.query)
        print(sign)
        data = {
            "from": self.params['from'],
            "to": self.params['to'],
            "query": self.query,
            "simple_means_flag": "3",
            "transtype": "translang",
            "sign": str(sign),
            "token": "8208900a3f6a89b69a8afd1270da7fbf",
            "domain": "common"
        }
        return data

    def main(self):

        s = session.get(self.index_url, headers=self.headers)
        print(s.text)
        print(session.cookies.get_dict())
        data = self.get_data_by_javascript()
        cookies = {
            "BAIDUID": "8FE65EF4565898CCEBAC3325FC9B1B6C:FG=1",
            "BAIDUID_BFESS": "8FE65EF4565898CCEBAC3325FC9B1B6C:FG=1",
            "__bid_n": "1842be2c49efe0c2334207",
            "Hm_lvt_64ecd82404c51e03dc91cb9e8c025574": "1667814135",
            "APPGUIDE_10_0_2": "1",
            "REALTIME_TRANS_SWITCH": "1",
            "FANYI_WORD_SWITCH": "1",
            "HISTORY_SWITCH": "1",
            "SOUND_SPD_SWITCH": "1",
            "SOUND_PREFER_SWITCH": "1",
            "ZD_ENTRY": "google",
            "Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574": "1668048491",
            "RT": "\"z=1&dm=baidu.com&si=0uc2stf1lcnl&ss=laalgna8&sl=4&tt=268&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=5qp&ul=5jk&hd=5qy\"",
            "ab_sr": "1.0.1_NDU2YTdmNWFiYTQ4OTM1YzdkMDg5ZjExOTc2MzY0MTBhMDUyZDY0NDY1YTAyNDkxMTVjYWY0MDFmNDBhN2M2Y2E5ODBkYjQ5NDdmNWJiOTFiNDAxNDEyMWJlZWRmNTA0N2ZjMzk3MDk0MzI5OTliMDhmYWM3MTcwODYwODUxYWM0MzI3ZDdiZmFjN2NiNzJjODc0NzkwNmVmMDAyY2E5Zg=="
        }
        response = requests.post(self.url, headers=self.headers, params=self.params, data=data, cookies=cookies)
        # response = session.post(self.url, headers=self.headers, params=self.params, data=data)
        print(response.json())

if __name__ == '__main__':
    baidu = Baidu('nice')
    baidu.main()

