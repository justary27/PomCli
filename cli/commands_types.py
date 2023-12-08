from enum import Enum

class CliCommandsTypes(Enum):
    LOGIN = "login"
    LIST_REPOSITORIES = "listRepos"
    SELECT_REPOSITORY = "selectRepo"
    SEARCH_REPOSITORY_FOR_POMFILES = "searchPom"
    LIST_POM_DEPENDENCIES = "listPomDep"
    GOTO_PREV_STAGE = ".."
    HELP = "help"
    CLEAR = "clear"
    LOGOUT = "logout"
    EXIT = "exit"

    @classmethod
    def exists(cls, eValue):
        if eValue in cls._value2member_map_:
            return cls._value2member_map_[eValue]
        
        return None
