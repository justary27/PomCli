from abc import ABC, abstractmethod

from cli.github.client import GitHubClient

class Cli(ABC):
    NAME:str
    VERSION:str

    prev_stage:list
    stage:str

    github_client:GitHubClient
    authenticated:bool

    @abstractmethod
    def save_stage(self):
        raise NotImplementedError

    @abstractmethod
    def reset_stage(self):
        raise NotImplementedError