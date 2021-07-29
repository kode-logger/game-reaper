from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
import textwrap
import animation
from clint.textui import colored, puts  # used to manage CLI backend and a bit of frontend


class Skidrow:
    def __init__(self):
        """
        constructor for Skidrow class.
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
        A method to set the user search/query string into url query form. Example: "https://www.skidrowreloaded.com/?s=query"
        :return: None
        """

        self.searchString = self.searchString.replace(' ', '+')  # replaces spaces with '+' in the search query.
        self.searchLink = urljoin('https://www.skidrowreloaded.com/', '?s={}'.format(self.searchString))

    def getPageLink(self):
        """
        A method to get details from the page and stores the game information in a dictionary.
        :return: None
        """

        available_games = []
        webpage = BeautifulSoup(requests.get(self.searchLink).content, 'html.parser')

    def skidVerbosePrinter(self):
        """
        A method to verbose print the game data obtained from SkidrowReloaded server.
        :return: None
        """

        pass

    def skidVerboseGamePrinter(self, name):
        """
        A method to verbose print the specific game filtered by input name.
        :return: None
        """

        pass

    def skidGamePrinter(self, name):
        """
        A method to print the specific game filtered by input name.
        :return: None
        """

        pass

    def skidPrinter(self):
        """
        A method to print less information on game data obtained from Crotorrent server.
        :return: None
        """

        pass

    @animation.wait('bar', text='[!] Fetching Data from SkidrowReloaded Server', speed=0.1, color='green')
    def skidProcess(self, search):
        """
        The driver method to search for a game from skidrow server.
        :param search: Search string entered by the user. (String)
        :return: None
        """

        self.set_searchString(search)  # sets the search query to the current object.
        self.set_searchData()  # generates and stores the link to a class member.
        self.getPageLink()  # collecting game data.
        return self.gameData  # returning the collected game data.


if __name__ == '__main__':
    skidBoi = Skidrow()
    skidBoi.skidProcess(input("Enter game name: "))
