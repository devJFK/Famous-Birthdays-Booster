import os
import time
import requests
import threading
from json import decoder


class Main:
    def __init__(self):
        self.variables = {
            'success': 0,
            'errors': 0
        }

        self.celebrity = input('[>] URL: https://www.famousbirthdays.com/people/')
        if '.html' not in self.celebrity:
            self.celebrity = f'{self.celebrity}.html'
        print()

    def _booster(self, arg):
        try:
            boost = requests.post(
                'https://www.famousbirthdays.com/api/people/boost', data=f'url={self.celebrity}',
                proxies={'https': f'http://{arg}'}, timeout=5, headers={
                    'Content-type': 'application/x-www-form-urlencoded',
                    'Referer': f'https://www.famousbirthdays.com/people/{self.celebrity}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KH'
                                  'TML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
                }
            ).json()['status']
        except Exception:
            self.variables['errors'] += 1
        else:
            if boost == 'success':
                try:
                    rank = requests.get(
                        f'https://www.famousbirthdays.com/people/{self.celebrity}',
                        proxies={'https': f'http://{arg}'}
                    ).text.split('<div class="rank-no">')[1].split('</div>')[0]
                except Exception:
                    self.variables['errors'] += 1
                else:
                    self.variables['success'] += 1
                    print(f'[!] Success | Rank: {rank}')
            else:
                self.variables['errors'] += 1
                print(f'[!] Error | {boost}')

    def _update_title(self):
        while True:
            os.system(
                f'title [Famous Birthdays Booster] - Boosted: {self.variables["success"]} ^| Errors'
                f': {self.variables["errors"]}'
            )
            time.sleep(0.1)

    def _multi_threading(self):
        threading.Thread(target=self._update_title).start()

        while True:
            for proxy in self.proxies:
                attempting = True

                while attempting:
                    if threading.active_count() <= 300:
                        threading.Thread(target=self._booster, args=(proxy,)).start()
                        attempting = False

    def setup(self):
        error = False
        if os.path.exists((proxies_txt := 'Proxies.txt')):
            with open(proxies_txt, 'r', encoding='UTF-8', errors='replace') as f:
                self.proxies = [
                    line.replace(' ', '') for line in f.read().splitlines() if line not in ('', ' ')
                ]
            if len(self.proxies) == 0:
                error = True
        else:
            open(proxies_txt, 'a').close()
            error = True

        if error:
            print('[!] Paste HTTP proxies in Proxies.txt.')
            os.system(
                'title [Famous Birthdays Booster] - Restart required && '
                'pause >NUL && '
                'title [Famous Birthdays Booster] - Exiting...'
            )
            time.sleep(3)
        else:
            self._multi_threading()


if __name__ == '__main__':
    os.system('cls && title [Famous Birthdays Booster]')
    main = Main()
    main.setup()
