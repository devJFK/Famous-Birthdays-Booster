from multiprocessing.pool import ThreadPool as pool
from models.famousbirthday import FamousBirthday
from models.response_status import ResponseType
from utils.file_reader import readList
from models.console import Console
from models.status import Status
from models.proxy import Proxy
from threading import Lock
from rich import print
import random


CONSOLE = Console('FamousBirthdayBoost', 'zoony1337')
PROXIES = []
MODULE = FamousBirthday()
LOCK = Lock()
COUNTER = {
    'Success':0,
    'Failure':0,
    'Errors':0
}

def randomProxy():
    if len(PROXIES) == 0:
        return Proxy(None, None)
    return random.choice(PROXIES)

def loadProxyType():
    while True:
        CONSOLE.printName()
        print(f'[yellow]1 - HTTPS[/yellow]')
        print(f'[yellow]2 - SOCKS4[/yellow]')
        print(f'[yellow]3 - SOCKS5[/yellow]')
        print(f'[red]0 - PROXYLESS[/red]')
        Response = CONSOLE.askInteger('Please choose a proxy type from the list above')
        if Response == 1:
            return 'https'
        elif Response == 2:
            return 'socks4'
        elif Response == 3:
            return 'socks5'
        elif Response == 0:
            return None

def loadProxies():
    proxyType = loadProxyType()
    if proxyType is None:
        return []
    while True:
        CONSOLE.printName()
        Response = CONSOLE.askString('Please drag in your proxy file').strip("'")
        proxyFile = readList(Response)
        if proxyFile != Status.FAILURE:
            return [Proxy(proxy, proxyType) for proxy in proxyFile]

def loadThreads():
    while True:
        CONSOLE.printName()
        Response = CONSOLE.askInteger('How many threads should be utilized?')
        if Response == 0:
            return 1
        return Response

def loadCelebrity():
    CONSOLE.printName()
    print('Which celebrity should be boosted?')
    Response = CONSOLE.askString('https://www.famousbirthdays.com/people/')
    return Response.rstrip('.html')

def sendBoost(celebrity):
    global COUNTER
    while True:
        status = MODULE.check(celebrity, randomProxy())

        while status == ResponseType.BANNED:
            with LOCK:
                COUNTER['Errors'] += 1
                CONSOLE.setTitle(COUNTER)
            status = MODULE.check(celebrity,randomProxy())

        with LOCK:
            if status == ResponseType.FAILURE:
                COUNTER['Failure'] += 1
                CONSOLE.setTitle(COUNTER)
                print(f'[red][[x]] Failed Request![/red]')
            else:
                COUNTER['Success'] += 1
                CONSOLE.setTitle(COUNTER)
                print(f'[green][[!!]] Success! | Rank: {status.rank}[/green]')

def run():
    global PROXIES
    celebrity = loadCelebrity()
    PROXIES = loadProxies()
    threadCount = loadThreads()
    Pool = pool(threadCount)
    for _ in range(threadCount):
        Pool.apply_async(sendBoost, (celebrity,))
    Pool.close()
    Pool.join()

if __name__ == "__main__":
    run()