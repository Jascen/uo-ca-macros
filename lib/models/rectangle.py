from Assistant import Engine


class Rectangle:
    def __init__(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        # Top of screen - X and Y are smaller
        # Note: X increases when you head East. 
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y

        # Bottom of screen - X and Y are larger
        # Note: Y increases when you head South
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y


    @staticmethod
    def FromLocation(top_left_location, bottom_right_location):
        return Rectangle(top_left_location.x, top_left_location.y, bottom_right_location.x, bottom_right_location.y)


    def IsInside(self):
        player = Engine.Player
        if player.X < self.top_left_x: return False
        if player.Y < self.top_left_y: return False
        if self.bottom_right_x < player.X: return False
        if self.bottom_right_y < player.Y: return False

        return True