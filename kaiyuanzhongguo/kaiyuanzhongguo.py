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

    async def get_js_info(self):
        with open('kaiyuanzhongguo.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', pwd)

            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def login(self):
        results_pwd = await self.get_js_info()
        print('pwd:',results_pwd)
        url = 'https://store.steampowered.com/login/dologin/'

        data = {
            'pwd': results_pwd,
            'email': user,
            'verifyCode': '',
            'save_login': 1,
            'google_code': '03AGdBq26No7AFvX2LyQSSbHh_apPUfPe6xzya21h96n7UdmjdxhWpLD9B3LSCElOyWSJIBuvoRQVi4JzbhfIv02PvFYhoTcd9VcUe16YGaKxz_KtKJheXRRVhRG1JnatK8L5e5dOeBmoO5C4SgwW2nDB9PCDM5IvBPftMzSDjpg0yFCe9A-S0UNsQXBSOLAoY1vjNjvBZ1tSppJzrSE3euxN4-U2wpYJ-Q60gUCP67rDJhIj04vI7tIodRPRsMJf_T1XG_UIhp2YvY3vsIUiRVuJv5Bf3hUD-V40MzS8lj3ref8NG_jU6Nz9YTGH5KSiCwibD09FMG2BKZqr1nf02otYZjXQdB1TwFSHlZ7I9hD_Kf7SATPULM3HjPBjlvXMIHOElM-VbRa156G_V96poDsNtEzwef3qjvQ',
        }

        headers = {
            'Host': 'www.oschina.net',
            'Origin': 'https://www.oschina.net',
            'Referer': 'https://www.oschina.net/home/login?goto_page=https%3A%2F%2Fwww.oschina.net%2F',
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
