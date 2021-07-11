# python packages
from requests.exceptions import ConnectionError
import json

# third-party packages
import argparse
from clint.textui import colored

# custom packages
from Server.CroTorrent.CroTorrent import CroTorrents
from CommandLineInterface import CLI

# global variables
gameData = {'crotorrents': None}

try:
    with open('meta.json', 'r') as file:
        meta_data = json.load(file)

except FileNotFoundError:
    print(colored.red("[!] Source Data is Corrupt, try reinstalling the program."))
    print(colored.green("[->] Visit this link for further help: https://github.com/kode-logger/game-reaper/wiki"))
    exit(0)


def program_description():
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

    return help_content


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=program_description(), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-g', '--game', help='Search string, used to search for the game on available servers.')
    parser.add_argument('-s', '--server',
                        help='Name of the server to use. See help to know the Available server names')
    parser.add_argument('-v', '--verbose', action='store_true', help='Views more detail on the game')
    arguments = parser.parse_args()

    cmdArgs = vars(arguments)

    try:
        searchQuery = cmdArgs['game']
        if searchQuery is None:
            CLI(gameData=gameData).main_menu()
        else:
            if cmdArgs['server'] is not None:
                if cmdArgs['server'] == '1':
                    croBoi = CroTorrents()  # A crotorrent Object to access all the methods.
                    gameData['crotorrents'] = croBoi.croProcess(searchQuery)  # getting Game Data from the cro server
                    croBoi.croVerbosePrinter() if cmdArgs[
                        'verbose'] else croBoi.croPrinter()  # Do verbose print if requested

    except ConnectionError as con_error:
        print('\n[!] Cannot access Internet.')
    except KeyboardInterrupt as key_interrupt:
        print('\n[#] You terminated me without showing any mercy. :(')
