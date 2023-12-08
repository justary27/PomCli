class Repository:
    """
    Model class for a GitHub repository, only the useful propoerties 
    from the API are stored.
    """
    def __init__(self, name:str, desc:str, url:str) -> None:
        self.name = name
        self.description = desc if len(desc) <= 24 else desc[:24]+"..."
        self.url = url
