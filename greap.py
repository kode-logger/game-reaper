import argparse
from requests.exceptions import ConnectionError

from CroTorrent import CroTorrents

gameData = {'crotorrents': [], 'skidrow': []}


def getServerNames():
    """
    A method to return the names of available servers.
    :return: None
    """
    serverName = "\n"
    for index, name in enumerate(gameData.keys()):
        serverName += "[{}] {}\n".format(index + 1, name)
    return serverName


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A program to get details of a game from Third-Party websites.')
    parser.add_argument('-g', '--game', help='Search string, used to search for the game on available servers.')
    parser.add_argument('-s', '--server', help='Name of the server to use. Available servers: \n' + getServerNames())
    parser.add_argument('-v', '--verbose', action='store_true', help='Views more detail on the game')
    arguments = parser.parse_args()

    cmdArgs = vars(arguments)

    try:
        searchQuery = cmdArgs['game']
        if searchQuery is None:
            searchQuery = input('[<] Enter the name of the game: ')

        # New Server feature
        # if cmdArgs['server'] is not None:
        #     print(cmdArgs['server'])
        #  Server feature is disabled for now.

        croBoi = CroTorrents()  # A crotorrent Object to access all the methods.

        gameData['crotorrents'] = croBoi.croProcess(searchQuery)  # getting Game Data from the cro server
        croBoi.croVerbosePrinter() if cmdArgs['verbose'] else croBoi.croPrinter()  # Do verbose print if requested

    except ConnectionError as con_error:
        print('\n[!] Cannot access Internet.')
    except KeyboardInterrupt as key_interrupt:
        print('\n[#] You terminated me without showing any mercy. :(')
