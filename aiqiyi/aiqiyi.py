# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.15
"""
import time

from info import user, pwd
import requests
import execjs
import asyncio


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }

    async def get_js_info(self):
        with open('aiqiyi.js', 'r') as file:
            js = file.read()
            passwd = execjs.compile(js).call('getPwd', pwd)
            return passwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        passwd = await self.get_js_info()
        url = 'https://passport.iqiyi.com/apis/reglogin/login.action'
        data = {
            'email': user,
            'fromSDK': 1,
            'sdk_version': '1.0.0',
            'passwd': passwd,
            'agenttype': 1,
            '__NEW': 1,
            'checkExist': 1,
            'lang': '',
            'ptid': '01010021010000000000',
            'nr': 2,
            'verifyPhone': 1,
            'area_code': 86,
            'dfp': 'a130f093610ff144e881fbcf7c30962f35f36e1d354649be2c6a2b1757c8e35876',
        }
        headers = {
            'Host': 'passport.iqiyi.com',
            'Origin': 'https://www.iqiyi.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.iqiyi.com/iframe/loginreg?ver=1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        response = await self.handle_request(url, data, headers)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
