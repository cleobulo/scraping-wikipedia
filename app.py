from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.parser import ParserHTML
from utils.data import saveDataOnFile, readDataFromFile

URL_SEED = 'https://pt.wikipedia.org/'
TODO_LIST = [URL_SEED]
DONE_LIST = []
BLACKLIST = set()
MAX_LINKS_VISITED = 100

parserHTML = ParserHTML()

def getInternalLinksFrom(url):
    regexInternalWikiLinks = r"^(/wiki/)(.*)?$"
    html = urlopen(url)
    parserHTML.loadPage(BeautifulSoup, html.read())
    return parserHTML.getTagA(regexInternalWikiLinks)

def isLinkNotAlreadyKnow(pulledLink):
    if 'href' in pulledLink.attrs:
        newURL = urljoin(URL_SEED, pulledLink.attrs['href'])
        if newURL not in DONE_LIST and newURL not in TODO_LIST:
            return True, newURL
    return False, None

def scrapper():
    counterVisitedLinks = 0

    while TODO_LIST:
        nextLinkToExplore = TODO_LIST.pop(0)
        if nextLinkToExplore not in DONE_LIST:
            try:
                if nextLinkToExplore in BLACKLIST:
                    continue

                newLinksList = getInternalLinksFrom(nextLinkToExplore)
                DONE_LIST.append(nextLinkToExplore)

                print(f'done: {nextLinkToExplore} - internal links: {len(newLinksList)}')

                for newLinkItem in newLinksList:
                    isNotAlreadyKnow, newUrl = isLinkNotAlreadyKnow(newLinkItem)
                    
                    if isNotAlreadyKnow:
                        TODO_LIST.append(newUrl)
            except HTTPError as e:
                print(f'done: {nextLinkToExplore} - error: {e.errno}')
                BLACKLIST.add(nextLinkToExplore)
            
            counterVisitedLinks += 1

        if counterVisitedLinks == MAX_LINKS_VISITED:
            saveDataOnFile('TODO_LIST.txt', TODO_LIST)
            saveDataOnFile('DONE_LIST.txt', DONE_LIST)
            saveDataOnFile('BLACKLIST.txt', BLACKLIST)
            counterVisitedLinks = 0
            print('--> Data lists saved on files')

def start():
    global TODO_LIST
    global DONE_LIST
    global BLACKLIST

    TODO_LIST = readDataFromFile('TODO_LIST.txt') or TODO_LIST
    DONE_LIST = readDataFromFile('DONE_LIST.txt') or DONE_LIST
    BLACKLIST = readDataFromFile('BLACKLIST.txt') or BLACKLIST

    scrapper()

if __name__ == '__main__':
    try:
        print('--> Scraper running...')
        start()
    except KeyboardInterrupt:
        saveDataOnFile('TODO_LIST.txt', TODO_LIST)
        saveDataOnFile('DONE_LIST.txt', DONE_LIST)
        saveDataOnFile('BLACKLIST.txt', BLACKLIST)
        print('Bye bye!!')
