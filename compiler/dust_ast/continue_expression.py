class ContinueExpression:
    def __init__(self):
        pass

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        return 'ContinueExpression'

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
