# Game-Reaper

<img src="https://raw.githubusercontent.com/kode-logger/resource-data-storage/main/game-reaper/MainBanner.png" alt="Main Banner" width=100% height=80%>

A program that gathers data about a game from several third-party sites and gives you a short detail on the game that
you had searched.

Not only this, but you might be able to get download links to the game that is if you are not able to afford it and yet if you still want to experience the gameplay. But, it is strictly mentioned that this project does not support game piracy, and we recommend you to support the developers by buying the game from their official webpage.

This project was started to test my web scraping skills, but I thought why not help some gamers to search about games faster. It would be a lot of work to open a browser and search for a game to know more about it. If you are a person who loves to use console or command line programs then this might be useful for you.

Please make sure to STAR the repository so that you won't miss out any latest updates 😆

**Only for Educational Purpose, using for illegal purpose will not be appreciated.**

We will be releasing further updates and documentation soon.

This program will look good with **Windows Terminal** or some other modern terminals.

## 📢 Announcements

##### PROJECT ON HOLD   
- I am afraid to mention that I have kept this project development on **hold** as I am busy with learning other tools and frameworks. Don't worry, will be continuing soon. Until then I would be happy to recieve any feedbacks and feature requests.

##### Upcoming version: v0.0.3
- Some UI Improvements
- New Server will be added on a monthly basis.
- Proxy server can be expected in next release.

##### Latest version: v0.0.1-Alpha
- Introduced Interactive Commandline version
- Introduced Commandline arguments
- Now supports crotorrents server, discover about games from crotorrents
- Fixed some printing issues

## 📢 Hey, you want to contribute?

I would really appreciate if you can support my project by fixing up issues and bugs, especially adding new servers and stuff. To get a better understanding on the brains of this project, I suggest you to go through the [Developer Documentation](https://github.com/kode-logger/game-reaper/wiki/Dev-Doc). 

## 📢 Installing the tool

This program requires python 3.x.x and some other python packages which can be installed by following the given steps.

### Packages used:
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [argparse](https://pypi.org/project/argparse/)
- [pyfiglet](https://github.com/pwaller/pyfiglet)
- [clint](https://pypi.org/project/clint/)
- [PyInquirer](https://github.com/CITGuru/PyInquirer)
- [animation](https://github.com/bprinty/animation)

### 1.  Downloading / Cloning the repository

   You are free to **choose one of the following** instruction to download the program.

   - You can either download any version of the tool by going to [releases](https://github.com/kode-logger/game-reaper/releases) and download the zip file. Extract the zip file to your desired directory.
                                                                          
   - You can also clone the repository on your local machine to do the same but you need to be a bit familiar with Git and also must have Git desktop or bash version. Checkout [GitHub Clone Repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) to know more on cloning this repository.
     

### 2. Installing requirements:

   Execute the following commands on your desired terminal to install the necessary packages to run the program, without these packages the program will not be able to run.

   ```shell
      Windows:
      $> pip install -r requirements.txt

      Ubuntu:
      $> pip3 install -r requirements.txt
   ```


## 📢 Running the program

The program can be executed in two different methods. The first is `The Interactive Commandline` which is really an ... interactive commandline and the other method is `The Args` which is simply passing your arguments with your command so only output is displayed directly. 

I recommend you to use `The Interactive Commandline` as it is really user friendly and is easy to use.

- ### The Interactive Commandline:
```shell
   Windows:
   $> python greap.py
   
   Ubuntu:
   $> python3 greap.py
```
#### Sample Screenshots

![image](https://user-images.githubusercontent.com/55313761/126973338-06ee7921-f31a-4b14-a78f-090d14d82975.png)

![image](https://user-images.githubusercontent.com/55313761/126973512-d2ab5457-6596-40df-bda5-a52d7a9aac53.png)

- ### The Args:
```shell
   Windows:
   $> python greap.py --game "<game name>" --server 1 --verbose
                           (or)
   $> python greap.py -g "<game name>" -s 1 -v
                           
   Ubuntu:
   $> python3 greap.py --game <"game name"> --server 1 --verbose
                           (or)
   $> python3 greap.py -g "<game name>" -s 1 -v
   
```
#### Sample Screenshots

![image](https://user-images.githubusercontent.com/55313761/126973854-c7898c33-ae57-4c8f-9e88-e9cc7b34bd83.png)

## 📢 Project Documentation

The documentation is yet to be made, for now I suggest you to keep a tab on the [wiki](https://github.com/kode-logger/game-reaper/wiki) page.

## 📢 Have any doubts?

Proceed to [Discussions](https://github.com/kode-logger/game-reaper/discussions) and feel free to select the appropriate discussion section or channel to share your idea, questions and more.
