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


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    async def get_js_info(self):
        with open('danglewang.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('rsa', pwd)

            return results_pwd

    async def handle_request(self, url, headers=None):
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            print(response.cookies)
            return response.text

    async def login(self):
        results_pwd = await self.get_js_info()

        url = f'https://oauth.d.cn/auth/login?display=web&name={user}&pwd={results_pwd}&to=https%253A%252F%252Fwww.d.cn%252F%253Ft%253D057ede67da48471a97f6809bf4bf11e6'

        headers = {
            'Host': 'oauth.d.cn',
            'Origin': 'https://oauth.d.cn/auth/goLogin.html',
            'Referer': 'http://seller.chuchujie.com/sqe.php?s=/User/index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = await self.handle_request(url, headers)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
