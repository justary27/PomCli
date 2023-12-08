import json
import requests

from cli.github.pomfile import PomFile
from cli.github.repository import Repository
from cli.github.endpoints import ApiEndpoints


class ApiClient:
    """"""

    @staticmethod
    def request_device_code(client_id:str) -> dict:
        response = requests.post(
            ApiEndpoints.DEVICE_CODE.value,
            json={
              "client_id": client_id,  
            },
            headers= {"Accept": "application/json"}
        )
        if response.ok:
            parsed_reponse = json.loads(response.text)
            return {
                "device_code": parsed_reponse["device_code"],
                "user_code": parsed_reponse["user_code"],
                "verification_url": parsed_reponse["verification_uri"],
                "interval": parsed_reponse["interval"],
            }
        else:
            raise Exception("An exception occured")

    @staticmethod
    def request_user_token(client_id:str, device_code:str) -> dict:
        reponse = requests.post(
            ApiEndpoints.ACCESS_TOKEN.value, 
            json={
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
            headers= {"Accept": "application/json"}
        )

        if reponse.ok:
            parsed_response = json.loads(reponse.text)

            if "access_token" not in parsed_response:
                return {
                    "error": parsed_response["error"],
                }
            else:
                return {
                    "user_token": parsed_response["access_token"],
                    "error": None,
                }


        else:
            raise Exception("An exception occured")
    
    @staticmethod
    def refresh_user_token():
        pass

    @staticmethod
    def get_all_user_repositories(user_token) -> list:
        response = requests.get(
            ApiEndpoints.USER_REPOS.value,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {user_token}",
            }
        )

        if response.ok:
            parsed_response = json.loads(response.text)
            repo_response = []

            for jsonRepo in parsed_response:
                name = jsonRepo["name"]
                url = jsonRepo["url"]
                desc = str(jsonRepo["description"])

                if desc == "None":
                    desc = "Description Unavailable"

                repo_response.append(
                    Repository(name, desc, url)
                )

            return repo_response

        else:
            raise Exception("An exception occured")
        
    @staticmethod
    def get_all_repo_pomfiles(user_token, repo_url) -> list:
        file_response = []

        repo_url = "https://api.github.com/repos/Ekryd/sortpom/contents"


        # Sets the depth of the maximum recursive search 
        # across folders.
        MAX_RECURSE_LEVEL = 4

        def recursive_search(url, recurse_lvl):
            if recurse_lvl <= MAX_RECURSE_LEVEL:
                response = requests.get(
                    url,
                    headers= {
                        "Accept": "application/json",
                        "Authorization": f"Bearer {user_token}"
                    }
                )

                if response.ok:
                    parsed_response = json.loads(response.text)

                    for searchObj in parsed_response:
                        name = str(searchObj["name"])
                        path = str(searchObj["path"])
                        url = str(searchObj["url"])
                        obj_type = str(searchObj["type"])

                        if name.lower() == "pom.xml" and obj_type=="file":
                            file_response.append(
                                PomFile(name, path, url)
                            )

                        elif obj_type == "dir":
                            recursive_search(url, recurse_lvl+1)

                else:
                    raise Exception("An exception occured")
            
        recursive_search(repo_url, 1)

        return file_response
    
    @staticmethod
    def get_pomfile_contents(user_token, url):
        response = requests.get(
            url,
            headers= {
                "Accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        if response.ok:
            parsed_response = json.loads(response.text)
            content = str(parsed_response["content"])

            return content
        else:
            raise Exception("An exception occured")
            

