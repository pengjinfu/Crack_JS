# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.7
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

    async def get_js_info(self, results):
        with open('steam.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', results, pwd)

            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        data = {
            'donotcache': int(time.time() * 1000),
            'username': user
        }
        results = await self.handle_request(url='https://store.steampowered.com/login/getrsakey/', data=data)
        results_pwd = await self.get_js_info(results)

        url = 'https://store.steampowered.com/login/dologin/'

        data = {
            'donotcache': int(time.time()),
            'password': results_pwd,
            'username': user,
            'twofactorcode': '',
            'emailauth': '',
            'loginfriendlyname': '',
            'captchagid': -1,
            'captcha_text': '',
            'emailsteamid': '',
            'rsatimestamp': 439350600000,
            'remember_login': 'true',
        }

        headers = {
            'Host': 'store.steampowered.com',
            'Origin': 'https://store.steampowered.com',
            'Referer': 'https://store.steampowered.com/login/?redir=&redir_ssl=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = await self.handle_request(url, data, headers)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
