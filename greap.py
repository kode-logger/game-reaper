# python packages
from requests.exceptions import ConnectionError
import json

# third-party packages
import argparse
from clint.textui import colored

# custom packages
from Server.CroTorrent.CroTorrent import CroTorrents
from Server.SkidrowReloaded.Skidrow import Skidrow
from CommandLineInterface import CLI

# global variables
gameData = {'crotorrents': None, 'skidrow': None}

# trying to load the meta data from the json
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

    parser = argparse.ArgumentParser(description=program_description(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-g', '--game', help='Search string, used to search for the game on available servers.')
    parser.add_argument('-s', '--server', help='Name of the server to use. See help to know the Available server names')
    parser.add_argument('-v', '--verbose', action='store_true', help='Views more detail on the game')
    arguments = parser.parse_args()

    cmdArgs = vars(arguments)

    try:
        searchQuery = cmdArgs['game']  # gets the search string
        if searchQuery is None:
            CLI(gameData=gameData).main_menu()
        else:
            if cmdArgs['game'] == '':
                print(colored.red("[!] Entered game name is empty !"))
            else:
                if cmdArgs['server'] is not None:
                    if cmdArgs['server'] == '1':
                        # A crotorrent Object to access all the methods.
                        croBoi = CroTorrents()
                        # getting Game Data from the cro server
                        gameData['crotorrents'] = croBoi.croProcess(searchQuery)
                        # Do verbose print if requested
                        croBoi.croVerbosePrinter() if cmdArgs['verbose'] else croBoi.croPrinter()

                    elif cmdArgs['server'] == '2':
                        # A skidrow Object to access all the methods.
                        skidBoi = Skidrow()
                        # getting Game Data from the skidrow server
                        gameData['skidrow'] = skidBoi.skidProcess(searchQuery)
                        # Do verbose print if requested
                        skidBoi.skidVerbosePrinter() if cmdArgs['verbose'] else skidBoi.skidPrinter()
                else:
                    print(colored.red('[!] game-reaper needs -g "<game name>" -s <server number> to process.'))
                    print(colored.red('[!] Use: -h or --help argument to checkout the server numbers and more.'))

    except ConnectionError as con_error:
        print('\n[!] Cannot access Internet.')
    except KeyboardInterrupt as key_interrupt:
        print('\n[#] You terminated me without showing any mercy. :(')
