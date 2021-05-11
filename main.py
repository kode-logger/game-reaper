from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from abc import ABCMeta, abstractmethod

gameData = {'crotorrents': [], 'steamunlocked': [], 'igg-games': []}


class Base(metaclass=ABCMeta):
    def __init__(self):
        self.searchLink = ''
        self.gameData = []
        self.searchString = ''

    @property
    @abstractmethod
    def set_searchData(self):
        pass

    @abstractmethod
    def get_searchData(self):
        pass


class CroTorrents(Base):
    def get_searchData(self):
        """
        A method to return the searchLink string.
        :return: searchLink (String), holds the website link of the search query.
        """
        return self.searchLink

    def set_searchString(self, search):
        self.searchString = search

    def set_searchData(self):
        """
        A method to set the user search/query string into url query form. Example: "https://crotorrents.com/?s=query"
        """
        self.searchString = self.searchString.replace(' ', '+')  # replaces spaces with '+' in the search query.
        self.searchLink = urljoin('https://crotorrents.com/', f'?s={self.searchString}')

    def getPageLink(self):
        """

        :return:
        """
        availableGames = []  # stores all the url of available games with similar tags or search string found in the site.
        webpage = BeautifulSoup(requests.get(self.searchLink).content, 'html.parser')  # get the search result webpage
        articleBlock = webpage.find_all('article')
        for content in articleBlock:
            links = content.find_all('a', {'class': ''})
            for link in links:
                if not re.search('/category/', link['href']):
                    availableGames.append(link['href'])

        if not availableGames:
            print('No such Game found in CroTorrents Server.')
        else:
            for game in availableGames:
                webpage = BeautifulSoup(requests.get(game).content, 'html.parser')
                links = webpage.find_all('a')
                for link in links:
                    if re.search('magnet:?', link['href']):
                        print(link['href'])

    def croProcess(self, search):
        self.set_searchString(search)
        self.set_searchData()
        self.getPageLink()


if __name__ == '__main__':
    searchQuery = input("Enter the game name to search: ")
    try:
        CroTorrents().croProcess(searchQuery)
    except requests.exceptions.ConnectionError:
        print("Cannot access Internet.")
