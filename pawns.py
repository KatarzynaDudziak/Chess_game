class Pawn:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} at {self.x}{self.y}"

    def move(self, x, y):
        pass

    def capture(self, x, y):
        pass


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


pawn = Pawn("white", "H", 1)
bishop = Bishop("black", "A", 1)
rook = Rook("white", "D", 1)
knight = Knight("black", "F", 1)
queen = Queen("white", "D", 1)
king = King("black", "A", 1)

print(pawn)
print(bishop)
print(rook)
print(knight)
print(queen)
print(king)
