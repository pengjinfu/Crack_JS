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

    async def get_js_info(self ):
        with open('chuchujie.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('md5', pwd)

            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        results_pwd = await self.get_js_info()

        url = 'http://seller.chuchujie.com/sqe.php?s=/AccountSeller/login'

        data = {
            'username': '203021',
            'password': results_pwd,
            'login_type': '',
            'sms_code': '',
            'redirect_uri': '',
            'channle': '',
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'seller.chuchujie.com',
            'Origin': 'http://seller.chuchujie.com',
            'Referer': 'http://seller.chuchujie.com/sqe.php?s=/User/index',
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
