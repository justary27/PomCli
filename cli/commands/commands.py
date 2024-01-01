from interface.base import Cli
from enums.commands_types import CliCommandsTypes

from tabulate import tabulate


class CliCommands:
    """
    This class implements all the functions/commands that 
    PomCli provides. Acts in a pluggable way.
    """
    class Decorators:
        @staticmethod
        def Authenticate(innerFunc):
            def wrapper(self, *args, **kwargs):                
                if not self.cli_instance.authenticated:
                    print("You need to login first to use this command")
                    self.cli_instance.reset_stage()
                else:
                    result = innerFunc(self, *args, **kwargs)
                    return result

            return wrapper
    
    def __init__(self, cli_instance:Cli) -> None:
        self.cli_instance = cli_instance


    def login(self):
        """
        The login command, logs the user via the github 
        device code OAuth sevice.
        """
        if not self.cli_instance.authenticated:
            self.cli_instance.authenticated = self.cli_instance.github_client.login()
        else:
            print("You're already authenticated")

    @Decorators.Authenticate
    def listAllRepositories(self):
        """
        The listRepos command, lists top 30 of all the repositories 
        of the currently logged in user.
        """
        self.cli_instance.save_stage()

        self.cli_instance.stage = f"{CliCommandsTypes.LIST_REPOSITORIES.value} >> "

        print("All repositories are listed below:")
        repos = self.cli_instance.github_client.getAllRepositories()

        if len(repos) > 0:
            for i in range(len(repos)):
                print(f"{i+1}. \033[96m{repos[i].name}\033[0m  {repos[i].description}")
        else:
            print("\033[91mNo repos found for this user!\033[0m")
            self.cli_instance.reset_stage()

    @Decorators.Authenticate
    def selectRepository(self):
        """
        The selectRepo command, selects one of the repositories 
        to search for pom.xml files in it.
        """
        self.cli_instance.save_stage()        

        if self.cli_instance.prev_stage[-1] == f"{CliCommandsTypes.LIST_REPOSITORIES.value} >> ":
            if len(self.cli_instance.github_client.repositories) == 0:
                print("\n\033[94mNo repository to select!\033[0m")
            else:
                repoNo = None
                try:
                    repoNo = int(input("Enter the repository number to enter: "))
                    self.cli_instance.github_client.getRepository(repoNo-1)
                    self.cli_instance.stage += f"{CliCommandsTypes.SELECT_REPOSITORY.value}({self.cli_instance.github_client.current_repo.name}) >> "
                except (ValueError, IndexError):
                    print("\033[91mEnter a valid repository number!\033[0m")
                    self.cli_instance.reset_stage()

        else:
            print("You need to run listRepos command first!")
            self.cli_instance.reset_stage()

    @Decorators.Authenticate
    def searchForAllPomFiles(self):
        """
        The searchPom command, searches and lists all the pom.xml files 
        in the currently selected the repository.
        """
        self.cli_instance.save_stage()
        self.cli_instance.stage += f"{CliCommandsTypes.SEARCH_REPOSITORY_FOR_POMFILES.value} >> "

        
        if self.cli_instance.prev_stage[-1] == f"{CliCommandsTypes.LIST_REPOSITORIES.value} >> {CliCommandsTypes.SELECT_REPOSITORY.value}({self.cli_instance.github_client.current_repo.name}) >> ":
            print(f"All pom files found in {self.cli_instance.github_client.current_repo.name} are listed below:")
            files = self.cli_instance.github_client.getAllRepoPomFiles()

            if len(files) > 0:
                data = []
                for i in range(len(files)):
                    data.append([i+1,  files[i].name, files[i].path])
                print(tabulate(data, ["SNo.", "Name", "Path"], tablefmt="fancy_grid"))
            else:
                print("\033[91mNo pom.xml files found for this repo!\033[0m")
                self.cli_instance.reset_stage()

        else:
            print("You need to run selectRepo command first!")
            self.cli_instance.reset_stage()

    @Decorators.Authenticate
    def printDependenciesInPomFile(self):
        """
        The listPomDep command, lists all the dependencies of the currently 
        selected pom.xml file in the currently selected repository.
        """
        self.cli_instance.save_stage()

        if self.cli_instance.prev_stage[-1] == f"{CliCommandsTypes.LIST_REPOSITORIES.value} >> {CliCommandsTypes.SELECT_REPOSITORY.value}({self.cli_instance.github_client.current_repo.name}) >> {CliCommandsTypes.SEARCH_REPOSITORY_FOR_POMFILES.value} >> ":
            if len(self.cli_instance.github_client.repositories) == 0:
                print("\n\033[94mNo repository to select!\033[0m")
            else:
                fileNo = None
                try:
                    fileNo = int(input("Enter the file number to enter: "))
                    dependencies = self.cli_instance.github_client.getPomFile(fileNo-1)

                    if len(dependencies) > 0:
                        print(tabulate(dependencies, "keys", tablefmt="fancy_grid"))
                    else:
                        print("\033[91mNo dependencies found for this file!\033[0m")
                        self.cli_instance.reset_stage()

                except (ValueError, IndexError):
                    print("\033[91mEnter a valid file number!\033[0m")
                    self.cli_instance.reset_stage()
                
        else:
            print("You need to run searchPom command first!")
            self.cli_instance.reset_stage()

    def logout(self) -> bool:
        """
        The logout command, logs out the currently logged in user.
        """
        logout_status = self.cli_instance.github_client.logout()

        if logout_status:
            print("\033[92mLogged out successfully\033[0m")
        else:
            print("\033[91mYou're already logged out\033[0m")
        
        return logout_status

    # TODO: Not Implemented Properly
    def help(self):
        self.commands = [
            self.login, 
            self.listAllRepositories, 
            self.selectRepository, 
            self.searchForAllPomFiles, 
            self.printDependenciesInPomFile
        ]

        for command in self.commands:
            print(f"{command.__name__}  {command.__doc__.strip()}")
