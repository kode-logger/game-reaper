class MyServer:
    def __init__(self):
        """
        constructor for Server classes.
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
