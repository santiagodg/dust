from parser import Parser

class Compiler:
    def __init__(self, parser: Parser):
        self.__parser = parser
    
    def test(self, data):
        return self.__parser.test(data)
