# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.3
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

    async def get_js_info(self ):
        with open('tianancaixian.js', 'r') as file:
            js = file.read()
            times = int(time.time() * 1000)
            jsonKey = execjs.compile(js).call('Encrypt', user,pwd,times)

            return jsonKey

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        jsonKey = await self.get_js_info()
        print(jsonKey)
        url = f'https://tianaw.95505.cn/tacpc/tiananapp/customer_login/taPcLogin?jsonKey={jsonKey}'
        data = {
            'jsonKey': jsonKey,
        }
        headers = {
            'Host': 'tianaw.95505.cn',
            'Origin': 'https://tianaw.95505.cn',
            'Referer': 'https://tianaw.95505.cn/tacpc/',
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


