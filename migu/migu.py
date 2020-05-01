# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.1
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

    async def get_js_info(self, a):
        with open('migu.js', 'r') as file:
            js = file.read()
            results_user = execjs.compile(js).call('getUser', user, a)
            results_pwd = execjs.compile(js).call('getPwd', pwd, a)
            results_fingerPrint = execjs.compile(js).call('getfingerPrint', a)
            fingerPring = results_fingerPrint.get('result')
            fingerPringDetail = results_fingerPrint.get('detail')
            return results_user, results_pwd, fingerPring, fingerPringDetail

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()

    async def get_a(self):
        url = 'https://passport.migu.cn/password/publickey'
        return await self.handle_request(url, headers=self.headers)

    async def login(self):
        a = await self.get_a()
        results_user, results_pwd, fingerPring, fingerPringtDetail = await self.get_js_info(a)

        url = 'https://passport.migu.cn/authn'

        data = {
            'sourceID': '203021',
            'appType': '2',
            'relayState': 'login',
            'loginID': results_user,
            'enpassword': results_pwd,
            'captcha': '',
            'imgcodeType': '1',
            'fingerPrint': fingerPring,
            'fingerPrintDetail': fingerPringtDetail,
            'isAsync': 'true'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'passport.migu.cn',
            'Origin': 'https://passport.migu.cn',
            'Referer': 'https://passport.migu.cn/login?sourceid=203021&apptype=2&forceAuthn=true&isPassive=false&authType=&display=&nodeId=70027513&relayState=login&weibo=1&callbackURL=http%3A%2F%2Fwww.miguvideo.com%2Fmgs%2Fwebsite%2Fprd%2Findex.html%3FisIframe%3Dweb',
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
