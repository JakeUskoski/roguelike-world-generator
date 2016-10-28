import math

class StaticCamera(object):
    def __init__(self, screen_size):
        self.x = 0
        self.y = 0
        self.x_size = screen_size[0]
        self.y_size = screen_size[1]
        self.x_min = -50
        self.y_min = -50
        self.x_limit = self.x_size + 50
        self.y_limit = self.y_size + 50

    def set_room_size(self, x_size, y_size):
        self.x_limit = x_size + 50
        self.y_limit = y_size + 50

    def position_camera(self, x, y):
        self.x = x
        self.y = y

    def center_camera(self, x, y):
        self.x = x - int(self.x_size / 2)
        self.y = y - int(self.y_size / 2)

        if self.x + self.x_size > self.x_limit:
            self.x = self.x_limit - self.x_size
        elif self.x < self.x_min:
            self.x = self.x_min

        if self.y + self.y_size > self.y_limit:
            self.y = self.y_limit - self.y_size
        elif self.y < self.y_min:
            self.y = self.y_min

    def move_camera(self, x, y):
        if x > 0:
            # positive
            if self.x + self.x_size + x > self.x_limit:
                self.x = self.x_limit - self.x_size
            else:
                self.x += x
        elif x < 0:
            # negative
            if self.x + x < self.x_min:
                self.x = self.x_min
            else:
                self.x += x

        if y > 0:
            # positive
            if self.y + self.y_size + y > self.y_limit:
                self.y = self.y_limit - self.y_size
            else:
                self.y += y
        elif y < 0:
            # negative
            if self.y + y < self.y_min:
                self.y = self.y_min
            else:
                self.y += y

    def x_offset(self, x):
        return x - self.x

    def y_offset(self, y):
        return y - self.y

class DragCamera(object):
    def __init__(self, screen_size):
        self.x = 0
        self.y = 0
        self.x_size = screen_size[0]
        self.y_size = screen_size[1]
        self.x_min = -50
        self.y_min = -50
        self.x_limit = self.x_size + 50
        self.y_limit = self.y_size + 50

    def position_camera(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        x_diff = self.x + int(self.x_size / 2) - x
        y_diff = self.y + int(self.y_size / 2) - y

        x_move = math.ceil(x_diff / 4)
        y_move = math.ceil(y_diff / 4)

        if x_move > 0:
            # positive
            if self.x + self.x_size + x_move > self.x_limit:
                self.x = self.x_limit - self.x_size
            else:
                self.x += x_move
        elif x_move < 0:
            # negative
            if self.x + x_move < self.x_min:
                self.x = self.x_min
            else:
                self.x += x_move

        if y_move > 0:
            # positive
            if self.y + self.y_size + y_move > self.y_limit:
                self.y = self.y_limit - self.y_size
            else:
                self.y += y_move
        elif y_move < 0:
            # negative
            if self.y + y_move < self.y_min:
                self.y = self.y_min
            else:
                self.y += y_move

    def x_offset(self, x):
        return x - self.x


    def y_offset(self, y):
        return y - self.y
