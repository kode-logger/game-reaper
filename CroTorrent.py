from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
import textwrap


class CroTorrents:
    def __init__(self):
        """
        User defined constructor for CroTorrents class.
        :return: None
        """
        self.gameData = list()
        self.searchLink = ''
        self.searchString = ''

    def get_searchData(self):
        """
        A method to return the searchLink string.
        :return: searchLink (String), holds the website link of the search query.
        """
        return self.searchLink

    def set_searchString(self, search):
        """
        A setter function to set the value of searchString
        :param search: A string that contains the user input
        :return: None
        """
        self.searchString = search

    def set_searchData(self):
        """
        A method to set the user search/query string into url query form. Example: "https://crotorrents.com/?s=query"
        :return: None
        """
        self.searchString = self.searchString.replace(' ', '+')  # replaces spaces with '+' in the search query.
        self.searchLink = urljoin('https://crotorrents.com/', '?s={}'.format(self.searchString))

    def getPageLink(self):
        """
        A method to get details from the page and stores the game information in a dictionary.
        :return: None
        """

        # get all available games from the search result and extract the game's main page Url.
        availableGames = []  # stores all the url of available games with similar tags or search string found in the site.
        webpage = BeautifulSoup(requests.get(self.searchLink).content, 'html.parser')  # get the search result webpage
        articleBlock = webpage.find_all('article')
        for content in articleBlock:
            links = content.find_all('a', {'class': ''})
            for link in links:
                if not re.search('/category/', link['href']):
                    availableGames.append(link['href'])

        # if no game is found, then it doesn't exist in crotorrents server.
        if not availableGames:
            print('No such Game found in CroTorrents Server.')

        # if games are found, then get more data...
        else:
            for game in availableGames:
                # get game webpage
                webpage = BeautifulSoup(requests.get(game).content, 'html.parser')

                # get magnet URL
                gameDLink = ''
                links = webpage.find_all('a')
                for link in links:
                    if re.search('magnet:?', link['href']):
                        gameDLink = link['href']

                # get name of the game from the website
                gameName = webpage.title.string.partition(' Torrent')[0]

                # get system requirements from the website
                gameRequirements = webpage.find('ul', {'class': 'bb_ul'}).get_text()
                gameRequirements = list(filter(None, gameRequirements.split('\n')))  # removing empty strings

                # get description from the website
                # if regex statement returns a list of length 1, then the description is a bit different to retrieve
                if len(re.split('(?i)\n{1,2}' + gameName + ' Overview[:\n\t]+', webpage.get_text())) == 1:
                    gameDescription = re.split('(?i)\n{1,2}' + gameName + ' Overview[:\n\t]+', webpage.get_text())[
                        0].split('\n\n')  # split the whole text by '\n\n'
                    # the description was always found at 77th index of the list, for any input that satisfies the above if condition
                    try:
                        # some descriptions had '<game-name> Overview\n' string with the description and those were removed here
                        gameDescription = gameDescription[77].split('\n')[1]
                    except IndexError:
                        # these descriptions doesn't contain '<game-name> Overview\n'.
                        gameDescription = gameDescription[77]
                else:  # if description retrieval is direct from the webpage, then
                    gameDescription = \
                        re.split('(?i)\n{1,2}' + gameName + ' Overview[:\n\t]+', webpage.get_text())[1].split('\n\n')[0]
                # save the data in a dictionary and add it to the global list.
                game = {'name': gameName, 'download_link': gameDLink, 'weblink': game, 'description': gameDescription,
                        'sysreq': gameRequirements}
                self.gameData.append(game)

    def croVerbosePrinter(self):
        """
        A method to verbose print the game data obtained from Crotorrent server.
        :return: None
        """

        print("[Crotorrents] -> Found {} game(s) related to the search.".format(len(self.gameData)))
        for index, game in enumerate(self.gameData):
            print('\n [{}>] {}'.format(index + 1, game['name']))
            print('\n\t[-] Magnet Link:')  # + game['download_link'])
            magnet = textwrap.TextWrapper(width=80).wrap(text=game['download_link'])
            for link in magnet:
                print('\t\t' + link)
            print('\n\t[-] Webpage Link: \n\t\t' + game['weblink'])
            print('\n\t[-] Description:')
            desc = textwrap.TextWrapper(width=80).wrap(text=game['description'])
            for text in desc:
                print('\t\t' + text)
            print('\n\t[-] System Requirements:')
            for req in game['sysreq']:
                print('\t\t' + req)

    def croPrinter(self):
        """
        A method to print less information on game data obtained from Crotorrent server.
        :return: None
        """

        print("[Crotorrents] -> Found {} game(s) related to the search.".format(len(self.gameData)))
        for index, game in enumerate(self.gameData):
            print('\n[{}>] {}'.format(index + 1, game['name']))
            print('\n\t[-] Magnet Link:')
            magnet = textwrap.TextWrapper(width=80).wrap(text=game['download_link'])
            for link in magnet:
                print('\t\t' + link)
            desc = textwrap.TextWrapper(width=80).wrap(text=game['description'])
            print('\n\t[-] Description: ')
            for text in desc:
                print("\t\t {}".format(text))

    def croProcess(self, search):
        """
        The driver method to search for a game from crotorrents server.
        :param search: Search string entered by the user. (String)
        :return: None
        """
        self.set_searchString(search)  # sets the search query to the current object.
        self.set_searchData()  # generates and stores the link to a class member.
        self.getPageLink()  # collecting game data.
        return self.gameData  # returning the collected game data.
