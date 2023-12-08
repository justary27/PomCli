import os
import time
from datetime import datetime

from dotenv import load_dotenv

from cli.github.pomfile import PomFile
from cli.github.api_client import ApiClient
from cli.github.repository import Repository

class GitHubClient:
    """
    The GitHub client class, uses the ApiClient class to 
    return modeled responses.
    """

    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.user_token = os.getenv("USER_TOKEN")
        self.user_token_creation_time = os.getenv("TOKEN_CREATION_TIME")

        self.authenticated = True if self.user_token else False

        self.repositories:list = []
        self.current_repo:Repository = None

        self.pom_files:list = []
        self.current_pomfile:PomFile = None

    def login(self):
        deviceResponse = None
        try:
            deviceResponse = ApiClient.request_device_code(self.client_id)

            if deviceResponse is not None:
                device_code = deviceResponse["device_code"]
                interval = deviceResponse["interval"]
                user_code = deviceResponse["user_code"]
                verification_url = deviceResponse["verification_url"]

                print(f"\nPlease visit: \033[96m{verification_url}\033[0m")
                print(f"And enter code \033[96m{user_code}\033[0m\n")

                return self.poll_for_token(self.client_id, device_code, interval)

        except Exception as e:
            print(e)
        pass

    def getAllRepositories(self) -> list:
        if len(self.repositories) > 0:
            return self.repositories
        else:
            reposResponse = None

            try:
                reposResponse = ApiClient.get_all_user_repositories(self.user_token)

                if reposResponse is not None:
                    self.repositories = reposResponse
                    return reposResponse
                
            except Exception as e:
                print(e)

    def getRepository(self, repo_index:int):
        self.current_repo = self.repositories[repo_index]
        print(f"\033[92mYou've entered the repository: {self.repositories[repo_index].name}\033[0m")

    def getAllRepoPomFiles(self) -> list:
        if len(self.pom_files) > 0:
            return self.pom_files
        else:
            fileResponse = None

            try:
                fileResponse = ApiClient.get_all_repo_pomfiles(self.user_token, self.current_repo.url+"/contents")
                
                if fileResponse is not None:
                    self.pom_files = fileResponse
                    return fileResponse
                
            except Exception as e:
                print(e)

    def getPomFile(self, file_index:int) -> list:
        self.current_pomfile = self.pom_files[file_index]
        print(f"\033[92mYou've entered the file: {self.pom_files[file_index].path}\033[0m")

        return self.current_pomfile.get_dependencies(ApiClient.get_pomfile_contents(self.user_token, self.current_pomfile.url))

    def logout(self) -> bool:
        if self.authenticated:

            with open(os.path.dirname(os.path.realpath(__file__)) + "/.env","r+") as envfile:
                lines = envfile.readlines()
                envfile.seek(0)

                for line in lines:
                    if "USER_TOKEN" in line:
                        pass
                    elif "TOKEN_CREATION_TIME" in line:
                        pass
                    else:
                        envfile.write(line)
                envfile.truncate()

            return True
        else:
            return False

    def poll_for_token(self, client_id, device_code, interval):
        poll = True

        while poll:
            tokenResonse = ApiClient.request_user_token(
                client_id, 
                device_code
            )

            error = tokenResonse["error"]

            if error:
                match error:
                    case "authorization_pending":
                        time.sleep(2*interval)

                    case "slow_down":
                        time.sleep(2*interval + 5)

                    case "expired_token":
                        poll = False
                        print("\033[91mThe device code has expired. Please run login again.\033[0m")
                        return False

                    case "access_denied":
                        poll = False
                        print("\033[91mLogin cancelled by user\033[0m")
                        return False

            else:
                user_token = tokenResonse["user_token"]
                self.authenticated = True
                poll = False

                with open(os.path.dirname(os.path.realpath(__file__)) + "/.env", "a") as envfile:
                    envfile.write(
                        f"\nUSER_TOKEN={user_token}\nTOKEN_CREATION_TIME={datetime.now().isoformat()}\n"
                    )

                print("\033[92mLogged in successfully!\033[0m")
                return True

    def check_token_validity(self) -> bool:
        if self.user_token and self.user_token_creation_time:
            pass
        else:
            return False
