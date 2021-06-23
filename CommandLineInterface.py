from __future__ import print_function, unicode_literals  # used by PyInquirer

import os  # used to implement some required system commands

import pyfiglet  # used to get ascii art of a text
import animation
from PyInquirer import prompt  # used to prompt user and get input
from clint.textui import colored, puts  # used to manage CLI backend and a bit of frontend
from examples import custom_style_3  # used to change the style of PyInquirer

from CroTorrent import CroTorrents


class CLI:

    def __init__(self, gameData):
        self.searchQuery = ''
        self.gameData = gameData

    # a method to print title
    def header(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        # printing Title and adding colour to it
        heading = pyfiglet.figlet_format('GReap', 'standard')
        puts(colored.blue(heading))

    def title(self):
        # clearing the terminal screen
        self.header()
        about = f'''
    Author: KodeLogger [https://github.com/kode-logger]

    [+] This program is recommended for personal use only.
    [+] Use of this program for exploiting or any other illegal usage will not be accepted.
    [+] Checkout the github link above to get the contact details of Author, if needed.
    [+] This program does not intend to harm any developers, it was created to get details of a game.
                '''
        note = '    [!] This program is still under development.'

        puts(colored.blue(about))
        puts(colored.red(note))
        print('\n')

    def main_menu(self):
        self.title()
        # basic main-menu
        menu = {
            'type': 'list',
            'name': 'menu',
            'message': 'Pick your choice:',
            'choices': ['Search', 'Help', 'Exit']
        }

        user = prompt(menu, style=custom_style_3, qmark='[<]')

        if user['menu'] == 'Search':
            self.searchGame()
        elif user['menu'] == 'Help':
            self.greapHelp()
        elif user['menu'] == 'Exit':
            puts(colored.green('[#] Thank you for using Game Reaper.'))
            exit(0)

    def searchGame(self):
        self.header()
        search = {
            'type': 'input',
            'name': 'searchQuery',
            'message': 'Enter the name of the Game:'
        }

        user = prompt(search, style=custom_style_3, qmark='[<]')
        self.searchQuery = user['searchQuery']
        self.gatherData()

    @animation.wait('ellipses', text='Fetching Data', speed=0.1, color='blue')
    def gatherData(self):
        # add further server process in future
        self.gameData['crotorrents'] = CroTorrents().croProcess(self.searchQuery)

    def greapHelp(self):
        print('Help section, need to fill it up')


if __name__ == '__main__':
    CLI().main_menu()
