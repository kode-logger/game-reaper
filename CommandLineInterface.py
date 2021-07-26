# python packages
from __future__ import print_function, unicode_literals  # used by PyInquirer
import json  # used to access and handle json file
import os  # used to implement some required system commands
import requests  # used tp handle network connection error

# third-party packages
import pyfiglet  # used to get ascii art of a text
from PyInquirer import prompt, Separator  # used to prompt user and get input
from clint.textui import colored  # used to manage CLI backend and a bit of frontend
from examples import custom_style_3  # used to change the style of PyInquirer

# custom packages
from Server.CroTorrent.CroTorrent import CroTorrents  # used to gather data from the crotorrents server

# trying to load the meta data from the json
try:
    with open('meta.json', 'r') as file:
        meta_data = json.load(file)

except FileNotFoundError:
    print(colored.red("[!] Source Data is Corrupt, try reinstalling the program."))
    print(colored.green("[->] Visit this link for further help: https://github.com/kode-logger/game-reaper/wiki"))
    exit(0)


def goBack():
    menuOpt = {
        'type': 'list',
        'name': 'menuOpt',
        'message': 'Press Enter to',
        'choices': ['Go Back']
    }
    prompt(menuOpt, style=custom_style_3, qmark='[<]')


def header():
    os.system('cls' if os.name == 'nt' else 'clear')

    # printing Title and adding colour to it
    heading = pyfiglet.figlet_format(meta_data['program']['name'].title(), 'digital')
    print(colored.blue(heading))


def title():
    # clearing the terminal screen
    header()
    about = f'''
Author: {meta_data['author']['name'].title()} [{meta_data['author']['link']}]
Version: {meta_data['program']['version']}

[+] This program does not intend to harm any developers, it was created to get details of a game.'''
    note = '[!] This program is still under development.'

    print(colored.blue(about))
    print(colored.red(note))
    print('\n')


class CLI:

    def __init__(self, gameData):
        self.searchQuery = ''
        self.gameData = gameData
        self.firstTimeVisit = True
        self.selectedServers = []
        self.serverGameList = []
        self.croBoi = None

    def main_menu(self):
        # if user is on the menu for the first time, then display author note. Else print only the heading.
        if self.firstTimeVisit:
            title()
            self.firstTimeVisit = False
        else:
            header()

        menu = {
            'type': 'list',
            'name': 'menu',
            'message': 'Pick your choice:',
            'choices': ['Search', 'Help', 'Exit']
        }

        user = prompt(menu, style=custom_style_3, qmark='[<]')

        if user['menu'] == 'Search':
            self.cli_process()
        elif user['menu'] == 'Help':
            self.greap_help()
        elif user['menu'] == 'Exit':
            print(colored.green('[#] Thank you for using Game Reaper.'))
            exit(0)

    def get_search_query(self):
        header()
        search = {
            'type': 'input',
            'name': 'searchQuery',
            'message': 'Enter the name of the Game:'
        }

        user = prompt(search, style=custom_style_3, qmark='[<]')
        self.searchQuery = user['searchQuery']

    def gather_data(self):
        # add further server process in future
        if len(self.selectedServers) > 0:
            for server in self.selectedServers:
                if server == 'crotorrents':
                    self.gameData['crotorrents'] = self.croBoi.croProcess(self.searchQuery)

    def showGameDetails(self, game_name, game_server):
        header()
        if game_server == 'crotorrents':
            self.croBoi.croVerboseGamePrinter(game_name)
        goBack()
        self.view_game_list()

    def search_result(self):
        server = {
            'type': 'checkbox',
            'name': 'serverView',
            'message': 'Select servers to view the results',
            'validate': lambda answer: 'You must choose at least one option.' if len(answer) == 0 else True,
            'choices': [dict(name=server) for server in list(self.gameData.keys())]
        }
        user = prompt(server, style=custom_style_3, qmark='[<]')
        return user['serverView']

    def view_game_list(self):
        header()
        i = 1
        if len(self.selectedServers) > 0:
            if len(self.serverGameList) == 0:
                for server in self.selectedServers:
                    self.serverGameList.append(
                        Separator(
                            '\n<========   ' + server + '   ========>\n'))  # adds server name as a section to the view
                    if len(self.gameData[server]) > 0:
                        for game in self.gameData[server]:
                            self.serverGameList.append({'name': str(i) + ') ' + game['name'], 'server': server})
                            i += 1
                    else:
                        self.serverGameList.append(Separator(' > This server doesn\'t contain the requested game <'))
                        continue
                self.serverGameList.append(Separator('\n   ---------------'))
                self.serverGameList.append("0) Go Back")

            viewGame = {
                'type': 'list',
                'name': 'option',
                'message': 'Select a game to know more about it:',
                'choices': self.serverGameList
            }
            user = prompt(viewGame, style=custom_style_3, qmark='[<]')

            if user['option'] == '0) Go Back':
                self.serverGameList = []
                self.main_menu()

            for currentGame in self.serverGameList:
                if type(currentGame) is dict and user['option'] == currentGame['name']:
                    self.showGameDetails(currentGame['name'][3:], currentGame['server'])
        else:
            print('No server was selected, please go back and try again.')
            goBack()
            self.main_menu()

    def cli_process(self):
        try:
            self.initServerObjects()
            self.get_search_query()  # get user search input
            print()  # print is used to improve ui visibility

            self.selectedServers = self.search_result()  # gets the user opted servers to view the filtered result.
            self.gather_data()  # searches for the game metadata on all the available servers and stores it

            self.view_game_list()  # prompts the user with available games
        except requests.exceptions.ConnectionError:
            print(colored.red('[!] Hey, I am not able to connect to the Internet.'))
            print(colored.red('[!] Please check your Internet connection !!'))

    def initServerObjects(self):
        self.croBoi = CroTorrents()

    def greap_help(self):
        header()
        help_content = colored.blue("\nAuthor: \n\t Name -> ") + colored.red(
            meta_data['author']['name']) + colored.blue(
            "\n\t Link -> ") + colored.red(meta_data['author']['link']) + colored.blue(
            "\n\nProgram: \n\t Name -> ") + colored.red(meta_data['program']['name']) + colored.blue(
            "\n\t Version -> ") + colored.red(meta_data['program']['version']) + colored.blue(
            "\n\t Link -> ") + colored.red(meta_data['program']['link']) + colored.blue(
            "\n\t Documentation / Help -> ") + colored.red(meta_data['program']['docs']) + colored.blue(
            "\n\nAvailable servers:")

        for index, server in enumerate(meta_data['program']['servers']):
            help_content += colored.red(f'\n\t {index + 1}. {server["name"]} [{server["link"]}]')

        help_content += '\n'

        print(help_content)
        goBack()
        self.main_menu()
