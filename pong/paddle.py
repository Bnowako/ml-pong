import arcade

from game_params import PADDLE_HEIGHT, PADDLE_WIDTH


class Paddle:
    VEL = 4
    move_up = False
    move_down = False

    def __init__(self,color, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.color = color

    def move(self, up=True):
        if up:
            self.y += self.VEL
        else:
            self.y -= self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
    
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT, self.color)
        self.velocity_y = 0