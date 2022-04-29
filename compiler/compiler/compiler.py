from .parser import Parser
from .dir_func import DirFunc

class Compiler:
    def __init__(self, parser: Parser):
        self.__parser = parser
        self.__dir_func = DirFunc()
    
    def test(self, data):
        return self.__parser.test(data)
