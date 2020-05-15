# -*- encoding:utf-8 -*-
"""
company:IT
author:pengjinfu
project:migu
time:2020.5.14
"""
import time

from info import user, pw
import requests
import execjs
import asyncio


class Login():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Cookie': 'NTES_hp_textlink1=old; _ntes_nnid=876f1d2384dedc253c9971737623b18c,1589431121688; NNSSPID=2cd365bd8d3c4347b5b79b36c2855b60; _ihtxzdilxldP8_=30; UM_distinctid=172117a3e55902-091739c474f189-3c3f5a0c-1fa400-172117a3e569d8; l_s_163MODXOXd=5B4AE6BFF238CE247A553C01A50AC390B198E9925FA86A048BC8C7445962C9A3C31D8382AEB21F15D3AA81881B37822F5964271D719FE15FFAC2B5E43775D64F1942AA1C0589BC8ECECDBE50FE53EF0106A04C55E1EB1A7AA2AAFCFA65BB513DDB1578FFDDF3EDFC5D4CD68C2578D87C; _9755xjdesxxd_=32; YD00000710348764%3AWM_NI=KlMjzjMMrV82gAhDjrE4NSg5fXqVPahDOLvyFu%2BWsJXgJveJrQ4FQF0i3lhuInp7OsHa90YXxTt0vHzpIOr9Did4iXf3ODQKKqpBiLIkOpm1oYfo9eiUnSlpIHGjTB6ccDY%3D; YD00000710348764%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb1db80f79c88b7b765a58a8ea6d14b879f9ebbaa60839689d8bb4f8df5fdafc82af0fea7c3b92a89b4838bf9628f93beb7bb3aa59fa8a5e97a87ec82b4e63fa688bfb7d36bac9c81adf57386abe5b8f2429cb98697e842b28ffca7d44ef4b7fd8deb7f8bb2c0d8ce798cbff7d1dc54bc8cbcd1f544bab087b0f13388b7acd5ec54a6ed81a5d44189afc0a3ec488bb58191f03bad87aa90bc6fab8ba2b4ef7c8b98898bd74af6bdada5dc37e2a3; YD00000710348764%3AWM_TID=o3xpWFV6Bx9BFUEUBEZ%2BCRMHvsFK%2FmIV; gdxidpyhxdE=P%5C40P9W0TBfS1wbKy9VADEYuIYrSgxxM0700ZxJ%2BnPNCRp56NKmkv6YdPrGD3%2FbZpm6mREl%5Cx6VdJbRBG3O3mIHL2cqgYzYx%5Cl%2BmqqY6DnM3mGakadcPvaa%2BgMEiCp8X%2BxeTmmiXEI6znl1Zmtb0SK%2Fj4XU6AcgMDQaPsZfewrS9et7g%3A1589453380952; P_INFO=wind8288@163.com|1589452488|0|mail163|11&21|hen&1589448796&mail_client#gud&440300#10#0#0|&0|wydz_platform&mail163&a23_client|wind8288@163.com; THE_LAST_LOGIN=wind8288@163.com; nts_mail_user=wind8288@163.com:-1:1; JSESSIONID-WYTXZDL=NpIK4jYSTQveotdWDay0ufMbFHXIKFDJT8a8c2tijxuI4Nlc8v5RMGvDr690Zsf8fWKxRsG4%2BfpnIE1%2BFyS8w%2BOwd%2FDSZeT3g%2Fza3vPLMExMEODF%2FFbuimUbhOLX%2BJQi9Q%5CQ1nt6mttAzYMGPxhoiylqQS%2F9%5CbXNay%2BTSGttky4U%2B3hQ%3A1589504965361; utid=1f2QAH2Gx2zyEaweDlGdKpcjdNAj8WGq; l_s_mail163CvViHzl=2BDA1093FDDA9283AD02B57FFFEC7E0E4C9905FC68C95C06AD15D15EDC79C945E4E73BC4A0C9D87919F95E1933571940E8F68DE0ADC9AE57AD109CA9D412DA3B4B4282125FCCC17B388A8B4CC1EF32AD46D5B6359F4879B79A7E28EB8B73A25CEDDC10C4D9E428FF3B15102C634A721D',
            'Host': 'dl.reg.163.com',
            'Origin': 'https://dl.reg.163.com',
            'Referer': 'https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?cd=%2F%2Fmimg.127.net%2Fp%2Ffreemail%2Findex%2Funified%2Fstatic%2F2020%2F%2Fcss%2F&cf=urs.163.3262f873.css&MGID=1589504363443.6982&wdaId=&pkid=CvViHzl&product=mail163',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }

    async def get_js_info(self):
        with open('wangyi.js', 'r') as file:
            js = file.read()
            pwd = execjs.compile(js).call('getPwd', pw)
            rtid = execjs.compile(js).call('getRitd')
            return pwd, rtid

    async def handle_request(self, url, data=None, flag=1):
        if flag == 1:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        else:
            response = self.session.post(url, data=data, headers=self.headers)
            return response.text

    async def get_tk(self, rtid):
        url = f'https://dl.reg.163.com/dl/gt?un={user}&pkid=CvViHzl&pd=mail163&channel=0&topURL=https%3A%2F%2Fmail.163.com%2F&rtid={rtid}&nocache' \
              f'={int(time.time() * 1000)}'

        tk = await self.handle_request(url)
        return tk

    async def login(self):
        pwd, rtid = await self.get_js_info()
        tk = (await self.get_tk(rtid))['tk']
        print(tk)
        url = 'https://dl.reg.163.com/dl/l'

        data = {
            'channel': 0,
            'd': 10,
            'domains': "",
            'l': 0,
            'pd': "mail163",
            'pkid': "CvViHzl",
            'pw': pwd,
            'pwdKeyUp': 1,
            'rtid': rtid,
            't': str(int(time.time() * 1000)),
            'tk': tk,
            'topURL': "https://mail.163.com/",
            'un': user,
        }
        print(data)
        response = await self.handle_request(url, data, flag=2)
        return response

    async def run(self):
        print(await self.login())


if __name__ == '__main__':
    login = Login()
    task = login.run()
    asyncio.get_event_loop().run_until_complete(task)
