# -*- coding:utf-8 -*-
"""
Author:Pengjinfu
Language:Python3.7
Date:2020.5.5
"""
import re

from info import pwd, user
import execjs
import requests
import time
import asyncio


class Login():

    def __init__(self):
        self.base_url = f'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTIzNDU2Nzg5&rsakt=mod&checkpin=1' \
                        f'&client=ssologin.js(v1.4.19)&_={int(time.time() * 1000)}'

        self.login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.session = requests.Session()
        self.headers = {'user': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

    async def handle_requests(self, url, data=None, flag=1):
        if flag == 1:
            response = self.session.get(url, data=data, headers=self.headers)
            if response.status_code == 200:
                return response.text
        else:
            response = self.session.get(url, data=data, headers=self.headers)
            if response.status_code == 200:
                response.encoding = 'GBK'
                return response.text

    async def get_info(self, pubkey=None, servertime=None, nonce=None, exectime=None, flag=1):
        with open('weibo.js', 'r') as file:
            js = file.read()
            if flag == 1:
                su = execjs.compile(js).call('getSu', user)
                return su
            else:
                su = execjs.compile(js).call('getSu', user)
                sp = execjs.compile(js).call('getPwd', pubkey, servertime, nonce, pwd)
                prelte = execjs.compile(js).call('getPrelte', exectime)

                return su, sp, prelte

    async def login(self):
        ts = re.sub(r'\.', '', str(time.time()))
        ts = ts[:13]
        su = await self.get_info()
        data = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': su,
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.15)',
            '_': ts
        }
        html = await self.handle_requests(self.base_url, data=data)
        date = eval(html.replace('sinaSSOController.preloginCallBack(', '').replace(')', ''))
        servertime = date['servertime']
        nonce = date['nonce']
        pubkey = date['pubkey']
        rsakv = date['rsakv']

        exectime = date['exectime']
        su, sp, prelte = await self.get_info(pubkey, servertime, nonce, exectime, flag=2)
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': '',
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': prelte,
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        html = await self.handle_requests(self.login_url, data=data, flag=2)
        print(html)


if __name__ == '__main__':
    spider = Login()
    asyncio.get_event_loop().run_until_complete(spider.login())
