# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:js
time:2020.5.1
"""

from info import user, pwd
import requests
import execjs
import asyncio


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.url = 'http://j.esf.leju.com/ucenter/login'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools'
        }

    async def get_js_info(self):
        with open('xinlangershoufang.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', pwd)
            return results_pwd

    async def handle_request(self, url, data=None,flag=1):
        response = self.session.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            if flag ==1:
                return response.json()
            else:
                return response.text

    async def get_ckey(self):
        res = await self.handle_request(self.url,flag=2)
        ckey = res.split('name="ckey" value="')[1].split('" />')[0]
        return ckey

    async def login(self):
        password = await self.get_js_info()
        ckey = await self.get_ckey()
        data = {
            'username': user,
            'password': password,
            'imgcode': '',
            'ckey': ckey
        }

        response = await self.handle_request(self.url, data)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
