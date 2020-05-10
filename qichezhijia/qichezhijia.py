# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.4
"""
from info import user,pwd
import requests
import execjs
import asyncio


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    async def get_js_info(self):
        with open('qichezhijia.js', 'r') as file:
            js = file.read()
            password = execjs.compile(js).call('hex_md5', pwd)

            return password

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        pwd = await self.get_js_info()
        url = 'https://account.autohome.com.cn/Login/ValidIndex'
        data = {
            'name': user,
            'pwd': pwd,
            'validcode': '',
            'isauto': 'true',
            'type': 'json',
            'backurl': 'https%253A%252F%252Fwww.autohome.com.cn%252Fbeijing%252F',
            'url': 'https%3a%2f%2fwww.autohome.com.cn%2fbeijing%2f',
            'fPosition': 10001,
            'sPosition': 1000100,
            'platform': 1,
            'popWindow': '0',
            'geetest_challenge': '869a6a76e399194d1dcd9f8446551f448n',
            'geetest_seccode': '21f2c9cba6fa90e4cb2c0b55c67be09f|jordan',
            'geetest_validate': '21f2c9cba6fa90e4cb2c0b55c67be09f',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'account.autohome.com.cn',
            'Origin': 'https://account.autohome.com.cn',
            'Referer': 'https://account.autohome.com.cn/?backurl=https%253A%252F%252Fwww.autohome.com.cn%252Fbeijing%252F&fPosition=10001&sPosition=1000100&platform=1&pvareaid=3311228',
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
