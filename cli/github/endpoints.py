from enum import Enum

class ApiEndpoints(Enum):
    """
    Enumeration class to store the enpoints accessed by the CLI.
    """

    DEVICE_CODE = "https://github.com/login/device/code"
    ACCESS_TOKEN = "https://github.com/login/oauth/access_token"
    USER_REPOS = "https://api.github.com/user/repos"

    # def REPO_SEARCH(owner:str, repo_name:str, path:str=""):
    #     return f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
