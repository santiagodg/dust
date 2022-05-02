from .parser import Parser
from .dir_func import DirFunc
from .semantic_cube import SemanticCube

class Compiler:
    def __init__(self, parser: Parser, dir_func: DirFunc, semantic_cube: SemanticCube):
        self.__parser = parser
        self.__dir_func = dir_func
        self.__semantic_cube = semantic_cube
    
    def test(self, data):
        return self.__parser.test(data)
