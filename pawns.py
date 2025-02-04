class Pawn:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"

    def can_move(self, current_pos, new_pos):
        return is_moving_forward_one_square(self.color, current_pos, new_pos) or is_moving_forward_two_squares(self.color, current_pos, new_pos)

    def can_capture(self, current_pos, new_pos):
        if self.color == "white":
            if (new_pos.x == current_pos.x + 1 and new_pos.y == current_pos.y + 1) or (new_pos.x == current_pos.x - 1 and new_pos.y == current_pos.y + 1):
                return True
        elif self.color == "black":
            if (new_pos.x == current_pos.x - 1 and new_pos.y == current_pos.y - 1) or (new_pos.x == current_pos.x + 1 and new_pos.y == current_pos.y - 1):
                return True
        return False
    

class Bishop(Pawn):
    def __init__(self, color):
        super().__init__(color)
    
    def can_move(self, current_pos, new_pos):
        return is_moving_diagonally(current_pos, new_pos)

    def can_capture(self, current_pos, new_pos):
        return is_moving_diagonally(current_pos, new_pos)
    

class Rook(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, current_pos, new_pos):
        return is_moving_sideways(current_pos, new_pos)

    def can_capture(self, current_pos, new_pos):
        pass


class Knight(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, current_pos, new_pos):
        if (abs(new_pos.x - current_pos.x) == 2 and abs(new_pos.y - current_pos.y) == 1) or (abs(new_pos.x - current_pos.x) == 1 and abs(new_pos.y - current_pos.y) == 2):
            return True
        return False

    def can_capture(self, current_pos, new_pos):
        pass


class Queen(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, current_pos, new_pos):
        return is_moving_diagonally(current_pos, new_pos) or is_moving_forward(current_pos, new_pos) or is_moving_sideways(current_pos, new_pos)

    def can_capture(self, current_pos, new_pos):
        pass


class King(Pawn):
    def __init__(self, color):
        super().__init__(color)

    def can_move(self, current_pos, new_pos):
        if abs(new_pos.x - current_pos.x) <= 1 and abs(new_pos.y - current_pos.y) <= 1:
            return True
        return False

    def can_capture(self, current_pos, new_pos):
        pass


def is_moving_diagonally(current_pos, new_pos):
    if abs(new_pos.x - current_pos.x) == abs(new_pos.y - current_pos.y):
        return True
    return False


def is_moving_forward_one_square(color, current_pos, new_pos):
    if color == "white":
        if new_pos.y == current_pos.y + 1 and new_pos.x == current_pos.x:
            return True
    elif color == "black":
        if new_pos.y == current_pos.y - 1 and new_pos.x == current_pos.x:
            return True
    return False


def is_moving_forward_two_squares(color, current_pos, new_pos):
    if color == "white":
        if current_pos.y == 1 and new_pos.y == current_pos.y + 2 and new_pos.x == current_pos.x:
            return True
    elif color == "black":
        if current_pos.y == 6 and new_pos.y == current_pos.y - 2 and new_pos.x == current_pos.x:
            return True
    return False


def is_moving_forward(color, current_pos, new_pos):
    if color == "white":
        if new_pos.y > current_pos.y and new_pos.x == current_pos.x:
            return True
    elif color == "black":
        if new_pos.y < current_pos.y and new_pos.x == current_pos.x:
            return True
    return False


def is_moving_sideways(current_pos, new_pos):
    if new_pos.y == current_pos.y and new_pos.x != current_pos.x:
        return True
    return False
