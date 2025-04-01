
class GameOverException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
    
    def __repr__(self) -> str:
        return self.message
