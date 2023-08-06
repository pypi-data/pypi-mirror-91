class Config:

    def __init__(
        self,
        containerInitFunction: callable,
        rootModuleName: str,
        allowedEnvironments: list,
    ):
        self.__containerInitFunction = containerInitFunction
        self.__rootModuleName = rootModuleName
        self.__allowedEnvironments = allowedEnvironments

    @property
    def containerInitFunction(self):
        return self.__containerInitFunction

    @property
    def rootModuleName(self):
        return self.__rootModuleName

    @property
    def allowedEnvironments(self):
        return self.__allowedEnvironments
