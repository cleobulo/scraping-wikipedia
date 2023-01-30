import re

class ParserHTML:

    def __init__(self, parser = 'html.parser'):
        self._puller = None
        self.parser = parser

    def loadPage(self, puller, html: bytes):
        self._puller = puller(html, self.parser)

    def getTagA(self, regex: str):
        return self._puller.find_all('a', {'href': re.compile(regex)})
