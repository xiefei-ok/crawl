# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : trans_youdao.py
# Time       ：2022/11/7 17:36
# Author     ：Flynn
# version    ：python 3
# Description：
"""
import random
import requests
import time
import hashlib
import execjs


class Youdao():
    def __init__(self, words):
        self.words = words
        self.header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://fanyi.youdao.com",
            "Pragma": "no-cache",
            "Referer": "https://fanyi.youdao.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {
            "OUTFOX_SEARCH_USER_ID": "-967679816@10.110.96.160",
            "OUTFOX_SEARCH_USER_ID_NCOO": "188633397.22078213",
            "JSESSIONID": "abcmKjqCc1uABbn2qYbry",
            "___rl__test__cookies": "1667810502376"
        }
        self.url = "https://fanyi.youdao.com/translate_o"
        self.params = {
            "smartresult": "rule"
        }

    def getparam_python(self):
        """
        改写加密方式
        :return: bv, ts, salt, sign
        """
        ua = self.header["User-Agent"]
        # 对UA进行MD5加密
        bv = hashlib.md5(ua.encode('utf-8')).hexdigest()
        # time stamp
        ts = str(int(time.time() * 1000))
        # 类似加盐操作，时间戳加上一个0到10的随机整数
        salt = ts + str(random.randint(0, 10))
        # md5（前固定字符+输入字符+经处理的时间戳变量+后固定字符）
        sign = hashlib.md5(("fanyideskweb" + self.words + salt + "Ygy_4c=r#e#4EX^NUGUc5").encode('utf-8')).hexdigest()
        return bv, ts, salt, sign

    def getparams_by_javascript(self):
        """
        调用js文件
        :return:
        """
        with open('youdao.js', 'r', encoding='utf-8')as f:
            youdao_js = f.read()
        params = execjs.compile(youdao_js).call('get_data', self.words, self.header["User-Agent"])
        return params.bv, params.ts, params.salt, params.sign

    def main(self):

        words = self.words
        # 选择两种解密方法
        # bv, lts, salt, sign = self.getparam_python()
        bv, lts, salt, sign = self.getparams_by_javascript()
        data = {
            "i": words,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }

        response = requests.post(self.url, headers=self.header, cookies=self.cookies, params=self.params, data=data)
        result = response.json()['translateResult'][0][0]['tgt']
        if 'smartResult' in response.json().keys():
            print('翻译成功', '*'*50)
            smart_result = [i.strip() for i in response.json()['smartResult']['entries'] if i.strip()]
            print(result, '\n智能引申', '*'*50)
            for i in smart_result:
                print(i)
        else:
            print('翻译成功', '*'*50)
            print(result)


if __name__ == '__main__':
    input_str = input('please input：')
    youdao = Youdao(str(input_str))
    youdao.main()