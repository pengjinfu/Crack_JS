# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.4
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
        with open('yitongdai.js', 'r') as file:
            js = file.read()
            password = execjs.compile(js).call('toMd5', pwd)

            return password

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        pwd = await self.get_js_info()
        url = 'https://app.etongdai.com/login/verifylogin'
        data = {
            'loginName': user,
            'password': pwd,
            'check': 'on',
            'next': 'null'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'app.etongdai.com',
            'Origin': 'https://app.etongdai.com',
            'Referer': 'https://app.etongdai.com/login/index',
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
