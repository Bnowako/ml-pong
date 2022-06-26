from tkinter import W
from tkinter.tix import WINDOW
from turtle import window_height
import arcade
from pong.paddle import Paddle
from pong.ball import Ball
from game_params import *
import time
class MyGame(arcade.Window):

    def __init__(self, width, height, fps=30, on_update_external = None):
        super().__init__(width, height, 'ArcadePong!')
        self.set_update_rate(1/fps)

        arcade.set_background_color(arcade.color.ALMOND)
        self.on_update_external = on_update_external
        self.ball_list = []
        self.paddle_list = []
        self.object_list = []
        self.computer_opponent = None
        self.human_player = None
        self.ball_init_speed = 0
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.draw_count = 0
        self.update_count = 0
        
    def setup(self):
        self.right_paddle = Paddle(color=arcade.color.BLUE, x=SCREEN_WIDTH-PADDLE_WIDTH//2-PADDLE_MARGIN, y=SCREEN_HEIGHT/2)
        self.left_paddle = Paddle(color=arcade.color.RED, x=PADDLE_WIDTH//2+PADDLE_MARGIN, y=SCREEN_HEIGHT/2)
        self.ball_init_speed = INITIAL_BALL_SPEED
        
        self.paddle_list = [self.left_paddle, self.right_paddle]
        self.ball = Ball(x= SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, color=arcade.color.ALLOY_ORANGE, paddles = self.paddle_list)
        self.object_list = self.paddle_list + [self.ball]
    

    def resetAll(self):
        self.ball_list = []
        self.paddle_list = []
        self.object_list = []
        self.computer_opponent = None
        self.human_player = None
        self.ball_init_speed = 0
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.right_paddle = Paddle(color=arcade.color.BLUE, x=SCREEN_WIDTH-PADDLE_WIDTH//2-PADDLE_MARGIN, y=SCREEN_HEIGHT/2)
        self.left_paddle = Paddle(color=arcade.color.RED, x=PADDLE_WIDTH//2+PADDLE_MARGIN, y=SCREEN_HEIGHT/2)
        self.ball_init_speed = INITIAL_BALL_SPEED
        self.draw_count = 0
        self.update_count = 0
        
        self.paddle_list = [self.left_paddle, self.right_paddle]
        self.ball = Ball(x= SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, color=arcade.color.ALLOY_ORANGE, paddles = self.paddle_list)
        self.object_list = self.paddle_list + [self.ball]

    def on_draw(self):
        # start = time.time()
        self.draw_count += 1
        arcade.Window.clear(self)
        for obj in self.object_list:
            obj.draw()
            self._draw_score()

        if DEBUG:
            self.debug_output()

        # end = time.time()
        # print(f'time to draw {end-start}')

        

    def update(self, delta_time):
        start = time.time()
        self.update_count += 1
        if(self.on_update_external != None):
            self.on_update_external()

        self.ball.move()
        self._handle_collision()
        self.move_paddle_ifKey(True, self.left_paddle)
        self.move_paddle_ifKey(False, self.right_paddle)

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > SCREEN_WIDTH:
            self.ball.reset()
            self.left_score += 1
        end = time.time()
        # print(f'time to update {end-start}')
    
    def debug_output(self):
        pass


    def _draw_score(self):
        arcade.draw_text(f'{self.left_score}', SCREEN_WIDTH-POINTS_DISPLAY_X_MARGIN, POINTS_DISPLAY_Y, arcade.color.WHITE, 28)
        arcade.draw_text(f'{self.right_score}', POINTS_DISPLAY_X_MARGIN, POINTS_DISPLAY_Y, arcade.color.WHITE, 28)

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + BALL_SIZE >= SCREEN_HEIGHT:
            ball.y_vel *= -1
        elif ball.y - BALL_SIZE <= 0:
            ball.y_vel *= -1
        
        if ball.x_vel < 0:

            
            if abs(left_paddle.y - ball.y) < PADDLE_HEIGHT / 2:
                if ball.x - BALL_SIZE <= left_paddle.x + PADDLE_WIDTH / 2:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + PADDLE_WIDTH / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (PADDLE_HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.left_hits += 1

        else:
            if abs(right_paddle.y - ball.y) < PADDLE_HEIGHT / 2:
                if ball.x + BALL_SIZE >= right_paddle.x - PADDLE_WIDTH / 2:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + PADDLE_HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (PADDLE_HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1


    def on_key_press(self, key, key_modifiers):
        # W = 119
        # S = 115
        # down = 65364
        # up = 65362
        if(key == 65307):
            self.ball.reset()
        
        if(key == 65362):
            self.right_paddle.move_up = True
        if(key == 65364):
            self.right_paddle.move_down = True

        if(key == 119):
            self.left_paddle.move_up = True
        if(key == 115):
            self.left_paddle.move_down = True

    def on_key_release(self, key, key_modifiers):
        if(key == 119):
            self.left_paddle.move_up = False
        if(key == 115):
            self.left_paddle.move_down = False
        if(key == 65362):
            self.right_paddle.move_up = False
        if(key == 65364):
            self.right_paddle.move_down = False


    def move_paddle_ifKey(self, left, paddle):
        if(paddle.move_up):
            self.move_paddle(left,up=True)
        if(paddle.move_down):
            self.move_paddle(left,up=False)


    def move_paddle(self, left=True, up=True):
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        """
        if left:
            if not up and (self.left_paddle.y - PADDLE_HEIGHT / 2) - Paddle.VEL < 0:
                return False
            if up and self.left_paddle.y + PADDLE_HEIGHT / 2 > SCREEN_HEIGHT:
                return False
            self.left_paddle.move(up)
        else:
            if not up and (self.right_paddle.y - PADDLE_HEIGHT / 2) - Paddle.VEL < 0:
                return False
            if up and self.right_paddle.y + PADDLE_HEIGHT / 2 > SCREEN_HEIGHT:
                return False
            self.right_paddle.move(up)

        return True

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
    
