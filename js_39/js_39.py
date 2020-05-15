# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:js
time:2020.5.15
"""
from info import user, pwd
import requests
import execjs
import asyncio
import time


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    async def get_js_info(self):
        with open('js_39.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('f0', pwd)
            results_user = execjs.compile(js).call('f0', user)

            return results_pwd, results_user

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.get(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.text

    async def login(self):
        results_pwd, results_user = await self.get_js_info()

        url = 'https://my.39.net/post.ashx?'

        data = {
            'callback': 'jQuery17209568488444353251_1589548414983',
            'action': 'jsonploginf0',
            'uname': results_user,
            'pwd': results_pwd,
            'safecode': '',
            'app': 29,
            '_': str(int(time.time() * 1000))
        }

        headers = {
            'referer': 'https://my.39.net/passport/Login.aspx?usertype=1&regauto=1&backurl=http://www.39.net/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = await self.handle_request(url, data, headers)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
