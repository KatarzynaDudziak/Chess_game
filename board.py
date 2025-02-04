class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[" " for _ in range(width)] for _ in range(height)]

# 0 <= x <= 7 and 0 <= y <= 7

board = Board(8, 8)
print(board.board)
