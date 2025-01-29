class Pawn:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x   # The row: from 0 to 7
        self.y = y   # The column: from 0 to 7

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} at {self.x}{self.y}"

    def move(self, x, y):
        if self.color == "white":
            if (x == self.x + 1 and y == self.y) or (self.x == 1 and y == self.y and x == self.x + 2):
                return True     # The pawn is moving one or two squares
        elif self.color == "black":
            if (x == self.x - 1 and y == self.y) or (self.x == 6 and y == self.y and x == self.x - 2):
                return True     # The pawn is moving one or two squares
        return  False    # The pawn is not moving, moving more than two squares or moving in the wrong direction

    def capture(self, x, y):
        if self.color == "white":
            if (x == self.x + 1 and y == self.y + 1) or (x == self.x + 1 and y == self.y - 1):
                return True     # The pawn is capturing another pawn
        elif self.color == "black":
            if (x == self.x - 1 and y == self.y + 1) or (x == self.x - 1 and y == self.y - 1):
                return True     # The pawn is capturing another pawn
        return False    # The pawn is not capturing or capturing in the wrong direction


class Bishop(Pawn):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


class Rook(Pawn):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


class Knight(Pawn):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


class Queen(Pawn):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


class King(Pawn):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


pawn = Pawn("white", 0, 1)
bishop = Bishop("black", 2, 1)
rook = Rook("white", 2, 1)
knight = Knight("black", 5, 1)
queen = Queen("white", 3, 1)
king = King("black", 6, 1)

print(pawn)
print(bishop)
print(rook)
print(knight)
print(queen)
print(king)
