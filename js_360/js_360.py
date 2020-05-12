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
        with open('js_360.js', 'r') as file:
            js = file.read()
            results_pwd = execjs.compile(js).call('getPwd', pwd)

            return results_pwd

    async def handle_request(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.text

    async def login(self):
        url = f'https://login.360.cn/?func=jQuery1124017767003817678484_1589244046496&src=pcw_home&from=pcw_home&charset=UTF-8&requestScema=https&quc_sdk_version=6.8.4&quc_sdk_name=jssdk&o=sso&m=getToken&userName={user}&_={int(time.time()*1000)}'
        print(url)
        response = self.session.get(url,headers=self.headers)

        token =  (response.text).replace(' jQuery1124017767003817678484_1589244046496({"errno":0,"errmsg":"","token":"','').replace('"})','')

        results_pwd = await self.get_js_info()
        print('pwd:', results_pwd)
        url = 'https://login.360.cn/'

        data = {
            'src': 'pcw_home',
            'from': 'pcw_home',
            'charset': 'UTF-8',
            'requestScema': 'https',
            'quc_sdk_version': '6.8.4',
            'quc_sdk_name': 'jssdk',
            'o': 'sso',
            'm': 'login',
            'lm': 0,
            'captFlag': 1,
            'rtype': 'data',
            'validatelm': 0,
            'isKeepAlive': 1,
            'captchaApp': 'i360',
            'userName': user,
            'smDeviceId': '',
            'type': 'normal',
            'account': user,
            'password': results_pwd,
            'captcha': 'dymd',
            'token': token,
            'proxy': 'https://i.360.cn/psp_jump.html',
            'callback': 'QiUserJsonp244046655',
            'func': 'QiUserJsonp244046655',
        }

        headers = {
            'Host': 'login.360.cn',
            'Origin': 'https://i.360.cn',
            'Referer': 'https://i.360.cn/login/?src=pcw_home&destUrl=https://www.360.cn/',
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
