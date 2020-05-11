# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.5
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    async def get_js_info(self):
        with open('threesevenwangyou.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('td', pwd)

            return results_pwd

    async def handle_request(self, url, headers=None):
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            return response.content.decode()

    async def login(self):
        times = int(time.time()*1000)
        results_pwd = await self.get_js_info()

        url = f'https://my.37.com/api/login.php?callback=jQuery183020993838473119997_1589202381530&action=login&login_account={user}&password={results_pwd}&ajax=0&remember_me=1&save_state=1&ltype=1&tj_from=100&s=1&tj_way=1&_={times}'

        headers = {
            'Host': 'my.37.com',
            'Referer': 'https://www.37.com/',
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
