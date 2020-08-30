from models.response_status import ResponseType
from models.proxy import Proxy
from models.valid import Valid
import requests
import re

import urllib3
urllib3.disable_warnings()

import traceback

class FamousBirthday():
    def check(self, celebrity, proxy):
        try:
            return self.checker(celebrity, proxy)
        except:
            print(traceback.format_exc())
            return ResponseType.BANNED

    def checker(self, celebrity, proxy):
        req = requests.session()
        req.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Referer':f'https://www.famousbirthdays.com/people/{celebrity}.html',
            'Content-Type':'application/x-www-form-urlencoded'
        }

        req.proxies = proxy.getProxy()
        req.verify = False

        Response = req.post('https://www.famousbirthdays.com/api/people/boost', f'url={celebrity}.html')

        if Response.status_code != 200 or 'status' not in Response.text:
            return ResponseType.BANNED
        
        Response = Response.json()

        if Response['status'] == 'success':
            Response = req.get(f'https://www.famousbirthdays.com/people/{celebrity}.html')

            if Response.status_code != 200:
                return ResponseType.BANNED

            Response = Response.text

            Rank = re.search(r'<div class="rank-no">(.*?)<', Response).group(1)

            return Valid(Rank)
        else:
            return ResponseType.FAILURE