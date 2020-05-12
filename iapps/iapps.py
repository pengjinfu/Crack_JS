# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.8
"""
from info import user, pwd
import requests
import execjs
import asyncio
import time
import time

class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    async def get_js_info(self):
        with open('iapps.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', pwd)

            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.text

    async def login(self):

        results_pwd = await self.get_js_info()
        print('pwd:', results_pwd)
        url = 'http://www.iappstoday.com/ajax/login'

        data = {
            'username': user,
            'password': results_pwd,
        }

        headers = {
            'Host': 'www.iappstoday.com',
            'Origin': 'http://www.iappstoday.com',
            'Referer': 'http://www.iappstoday.com/',
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
