from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
import textwrap
import animation
from clint.textui import colored, puts  # used to manage CLI backend and a bit of frontend
from Server.ServerTemplate import MyServer


class CroTorrents(MyServer):
    def __init__(self):
        """
        constructor for CroTorrents class.
        :return: None
        """
        super().__init__()

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
            pass  # do nothing.

        # if games are found, then get more data...
        else:
            for game in availableGames:
                # initializing local variables
                gameRequirements = None
                gameDescription = None

                # get game webpage
                webpage = BeautifulSoup(requests.get(game).content, 'html.parser')

                # get magnet URL
                gameDLink = ''
                try:
                    # look for href attribute in a tag which contains the magnet link
                    links = webpage.find_all('a')
                    for link in links:
                        if re.search('^magnet:?', link['href']):
                            gameDLink = link['href']
                except KeyError:
                    # if there is no href attribute present or no magnet link is found then...
                    gameDLink = 'Not Available'

                # get name of the game from the website
                gameName = webpage.title.string.partition(' Torrent')[0]

                # get system requirements from the website
                heading_tags = ['h1', 'h2', 'h3']
                for heading in webpage.find_all(heading_tags):
                    if re.search('^System.+Requirements$', heading.get_text().strip()):
                        gameRequirements = heading.find_next('ul', {'class': 'bb_ul'}).get_text()
                        break
                gameRequirements = list(filter(None, gameRequirements.split('\n')))

                # get description from the website
                try:
                    # try to find the <div> that contains description.
                    gameDescription = webpage.find('div', {'class': 'game_area_description'}).get_text()

                except AttributeError:
                    # if the description is not defined in the div tag, then get it from the p tag after the heading.
                    for head_tag in webpage.find_all(heading_tags):
                        if re.search('Overview$', head_tag.get_text().strip()):
                            gameDescription = head_tag.find_next('p').get_text()

                # save the data in a dictionary and add it to the global list.
                game = {
                    'name': gameName,
                    'download_link': gameDLink,
                    'weblink': game,
                    'description': gameDescription,
                    'sysreq': gameRequirements
                }
                self.gameData.append(game)

    def croVerbosePrinter(self):
        """
        A method to verbose print the game data obtained from Crotorrent server.
        :return: None
        """

        puts(colored.blue('\n[Crotorrents] -> Found {} game(s) related to the search.\n'.format(len(self.gameData))))
        for game in self.gameData:
            puts(colored.red("-+-" * 35))
            self.croVerboseGamePrinter(game['name'])
            puts(colored.red("-+-" * 35))

    def croVerboseGamePrinter(self, name):
        """
        A method to verbose print the specific game filtered by input name.
        :return: None
        """

        for currentGame in self.gameData:
            if currentGame['name'] == name:

                puts(colored.green('\n[>] Name: \n'))
                print('\t\t' + currentGame['name'])

                puts(colored.green('\n[>] Magnet Link: \n'))
                magnet = textwrap.TextWrapper(width=80).wrap(text=currentGame['download_link'])
                for link in magnet:
                    print('\t\t' + link)

                puts(colored.green('\n[>] Webpage Link: \n'))
                print('\t\t' + currentGame['weblink'])

                puts(colored.green('\n[>] Description: \n'))
                desc = textwrap.TextWrapper(width=80).wrap(text=currentGame['description'])
                for text in desc:
                    print('\t\t' + text)

                puts(colored.green('\n[>] System Requirements: \n'))
                for req in currentGame['sysreq']:
                    print('\t\t' + req)
                print()
                break

    def croGamePrinter(self, name):
        """
        A method to print the specific game filtered by input name.
        :return: None
        """

        for currentGame in self.gameData:
            if currentGame['name'] == name:

                puts(colored.green('\n[>] Name: \n'))
                print('\t\t' + currentGame['name'])

                puts(colored.green('\n[>] Magnet Link: \n'))
                magnet = textwrap.TextWrapper(width=80).wrap(text=currentGame['download_link'])
                for link in magnet:
                    print('\t\t' + link)

                puts(colored.green('\n[>] Description: \n'))
                desc = textwrap.TextWrapper(width=80).wrap(text=currentGame['description'])
                for text in desc:
                    print('\t\t' + text)
                print()
                break

    def croPrinter(self):
        """
        A method to print less information on game data obtained from Crotorrent server.
        :return: None
        """

        puts(colored.blue('\n[Crotorrents] -> Found {} game(s) related to the search.\n'.format(len(self.gameData))))
        for game in self.gameData:
            puts(colored.red("-+-" * 35))
            self.croGamePrinter(game['name'])
            puts(colored.red("-+-" * 35))

    @animation.wait('bar', text='[!] Fetching Data from CroTorrent Server', speed=0.1, color='green')
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
