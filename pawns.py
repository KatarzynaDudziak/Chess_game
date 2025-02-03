class Pawn:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"

    def can_move(self, pawn_x, pawn_y, x, y):
        return move_forward_one_square(self.color, pawn_x, pawn_y, x, y) or move_forward_two_squares(self.color, pawn_x, pawn_y, x, y)

    def can_capture(self, pawn_x, pawn_y, x, y):
        if self.color == "white":
            if (x == pawn_x + 1 and y == pawn_y + 1) or (x == pawn_x + 1 and y == pawn_y - 1) and 0 <= x <= 7 and 0 <= y <= 7:
                return True
        elif self.color == "black":
            if (x == pawn_x - 1 and y == pawn_y + 1) or (x == pawn_x - 1 and y == pawn_y - 1) and 0 <= x <= 7 and 0 <= y <= 7:
                return True
        return False
    

class Bishop(Pawn):
    def __init__(self, color):
        super().__init__(color)
    
    def can_move(self, bishop_x, bishop_y, x, y):
        return move_diagonally(bishop_x, bishop_y, x, y)

    def can_capture(self, bishop_x, bishop_y, x, y):
        return move_diagonally(bishop_x, bishop_y, x, y)
    

class Rook(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, rook_x, rook_y, x, y):
        pass

    def can_capture(self, rook_x, rook_y, x, y):
        pass


class Knight(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, knight_x, knight_y, x, y):
        pass

    def can_capture(self, knight_x, knight_y, x, y):
        pass


class Queen(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, queen_x, queen_y, x, y):
        pass

    def can_capture(self, queen_x, queen_y, x, y):
        pass


class King(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, king_x, king_y, x, y):
        pass

    def can_capture(self, king_x, king_y, x, y):
        pass


def move_diagonally(bishop_x, bishop_y, x, y):
    if abs(x - bishop_x) == abs(y - bishop_y) and 0 <= x <= 7 and 0 <= y <= 7:
        return True
    return False

def move_forward_one_square(color, pawn_x, pawn_y, x, y):
    if color == "white":
        if x == pawn_x + 1 and y == pawn_y and 0 <= x <= 7 and 0 <= y <= 7:
            return True
    elif color == "black":
        if x == pawn_x - 1 and y == pawn_y and 0 <= x <= 7 and 0 <= y <= 7:
            return True
    return False
    
def move_forward_two_squares(color, pawn_x, pawn_y, x, y):
    if color == "white":
        if pawn_x == 1 and x == pawn_x + 2 and y == pawn_y and 0 <= x <= 7 and 0 <= y <= 7:
            return True
    elif color == "black":
        if pawn_x == 6 and x == pawn_x - 2 and y == pawn_y and 0 <= x <= 7 and 0 <= y <= 7:
            return True
    return False
