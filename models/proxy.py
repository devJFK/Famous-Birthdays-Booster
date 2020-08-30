class Proxy():
    def __init__(self, proxy, pType):
        self.proxy = proxy
        self.pType = pType

    def getProxy(self):
        if self.proxy is None or self.pType is None:
            return None
        return {
            'http':f'{self.pType}://{self.proxy}',
            'https':f'{self.pType}://{self.proxy}'
        }

