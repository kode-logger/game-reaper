from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
import textwrap
import argparse

gameData = {'crotorrents': [], 'skidrow': []}

def getServerNames():
    serverName = "\n"
    for index, name in enumerate(gameData.keys()):
        serverName += "[{}] {}\n".format(index + 1, name)
    return serverName

class CroTorrents:
    def __init__(self):
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
        self.searchLink = urljoin('https://crotorrents.com/', f'?s={self.searchString}')

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
                    gameDescription = re.split('(?i)\n{1,2}' + gameName + ' Overview[:\n\t]+', webpage.get_text())[0].split('\n\n')  # split the whole text by '\n\n'
                    # the description was always found at 77th index of the list, for any input that satisfies the above if condition
                    try:
                        # some descriptions had '<game-name> Overview\n' string with the description and those were removed here
                        gameDescription = gameDescription[77].split('\n')[1]
                    except IndexError:
                        # these descriptions doesn't contain '<game-name> Overview\n'.
                        gameDescription = gameDescription[77]
                else:  # if description retrieval is direct from the webpage, then
                    gameDescription = re.split('(?i)\n{1,2}' + gameName + ' Overview[:\n\t]+', webpage.get_text())[1].split('\n\n')[0]
                # save the data in a dictionary and add it to the global list.
                game = {'name': gameName, 'download_link': gameDLink, 'weblink': game, 'description': gameDescription,
                        'sysreq': gameRequirements}
                gameData['crotorrents'].append(game)

    def croVerbosePrinter(self):
        i = 1
        print(f"[Crotorrents] -> Found {len(gameData['crotorrents'])} game(s) related to the search.")
        for game in gameData['crotorrents']:
            print(f"\n----------------------[{i}]----------------------")
            print(' Name: \n\t' + game['name'])
            print('\n Magnet Link: \n\t' + game['download_link'])
            print('\n Webpage Link: \n\t' + game['weblink'])
            print('\n Description:')
            desc = textwrap.TextWrapper(width=80).wrap(text=game['description'])
            for text in desc:
                print('\t' + text)
            print('\n System Requirements:')
            for req in game['sysreq']:
                print('\t' + req)
            i += 1

    def croProcess(self, search):
        """
        The driver method to search for a game from crotorrents server.
        :param search: Search string entered by the user.
        :return:
        """
        self.set_searchString(search)
        self.set_searchData()
        self.getPageLink()
        self.croVerbosePrinter()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="A program to get details of a game from Third-Party websites.")
    parser.add_argument('-g','--game', help='Search string, used to search for the game on available servers.')
    parser.add_argument('-s','--server', help='Name of the server to use. Available servers: \n' + getServerNames())
    arguments = parser.parse_args()

    cmdArgs = vars(arguments)

    try:
        searchQuery = cmdArgs['game']
        if searchQuery is None:
            searchQuery = input("Enter the name of the game: ")
        if cmdArgs['server'] is not None:
            print(cmdArgs['server'])
        CroTorrents().croProcess(searchQuery)
    except requests.exceptions.ConnectionError:
        print("Cannot access Internet.")
