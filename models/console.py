from sys import platform
from rich import print
import ctypes
import os

class Console():
    def __init__(self, programName, author):
        self.programName = programName
        self.author = author
        self.defaultTitle()

    def defaultTitle(self):
        if platform == 'win32': # Allows for use on multiple OS's, not just Windows.
            ctypes.windll.kernel32.SetConsoleTitleW(f'{self.programName} by {self.author}')

    def setTitle(self, counter):
        if platform == 'win32':
            Success = counter['Success']
            Failure = counter['Failure']
            Errors = counter['Errors']
            ctypes.windll.kernel32.SetConsoleTitleW(f'{self.programName} by {self.author} | Successes: {Success} | Failures: {Failure} | Errors: {Errors}')

    def clearConsole(self):
        if platform == 'win32': # Checks if OS is Windows
            os.system('cls')
        else: # Assumes Linux/Mac
            os.system('clear')

    def printName(self):
        self.clearConsole()
        print(f'Welcome to [green]{self.programName}[/green] by [green]{self.author}[/green]')
        print()

    def askString(self, question):
        while True:
            print(f'[yellow]{question}[/yellow]')
            Response = input()
            if len(Response) > 0:
                return Response

    def askInteger(self, question):
        while True:
            print(f'[yellow]{question}[/yellow]')
            Response = input()
            if Response.isnumeric() and int(Response) >= 0:
                return int(Response)