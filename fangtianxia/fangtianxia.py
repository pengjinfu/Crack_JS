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

    async def get_js_info(self):
        with open('fangtianxia.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', pwd)
            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        password = await self.get_js_info()

        url = 'https://passport.fang.com/login.api'

        data = {'uid': user,
                'pwd': password,
                'Service': ' soufun-passport-web',
                'AutoLogin': ' 1'}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'passport.fang.com',
            'Origin': 'https://passport.fang.com',
            'Referer': 'https://passport.fang.com/?backurl=http%3a%2f%2fmy.fang.com%2f',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        }

        response = await self.handle_request(url, data, headers)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
