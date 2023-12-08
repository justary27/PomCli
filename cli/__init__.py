import os

from .github import client

from cli.base import Cli
from cli.commands import CliCommands
from cli.commands_types import CliCommandsTypes

class PomCli(Cli):
    """
    A pom.xml CLI parser for your GitHub repos.
    """

    def __init__(self) -> None:
        self.NAME = "PomCli"
        self.VERSION = "1.0.0"
        self.RUNNING = True

        self.prev_stage = [""]
        self.stage = ""

        self.github_client = client.GitHubClient()
        self.authenticated = self.github_client.authenticated

        self.commands = CliCommands(self)

    def run(self):
        """
        The runner function for PomCli
        """
        print(f"\033[96mRunning {self.NAME} v{self.VERSION} ....\033[0m")
        
        while self.RUNNING:
            print(f"\n\033[94m{self.NAME} >> {self.stage}\033[0m", end='')
            argument = CliCommandsTypes.exists(input())

            match argument:
                case CliCommandsTypes.LOGIN:
                    self.commands.login()
                    
                case CliCommandsTypes.LIST_REPOSITORIES:
                    self.commands.listAllRepositories()

                case CliCommandsTypes.SELECT_REPOSITORY:
                    self.commands.selectRepository()

                case CliCommandsTypes.SEARCH_REPOSITORY_FOR_POMFILES:
                    self.commands.searchForAllPomFiles()

                case CliCommandsTypes.LIST_POM_DEPENDENCIES:
                    self.commands.printDependenciesInPomFile()

                case CliCommandsTypes.HELP:
                    self.commands.help()
                    
                case CliCommandsTypes.GOTO_PREV_STAGE:
                    if len(self.prev_stage) == 1:
                        pass
                    else:
                        self.reset_stage()
                case CliCommandsTypes.CLEAR:
                    os.system('cls' if os.name == 'nt' else 'clear')

                case CliCommandsTypes.LOGOUT:
                    self.RUNNING = not self.commands.logout()
                    
                case CliCommandsTypes.EXIT:
                    self.RUNNING = False
                    print(f"\n\033[92mThank you for using {self.NAME} today!\033[0m")

                case _:
                    print("Invalid Command!")

    def save_stage(self):
        self.prev_stage.append(self.stage)

    def reset_stage(self):
        self.stage = self.prev_stage[-1]
        self.prev_stage.pop()

pom_cli = PomCli()
