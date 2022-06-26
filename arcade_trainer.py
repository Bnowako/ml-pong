from distutils.sysconfig import get_makefile_filename
from game_params import SCREEN_HEIGHT, SCREEN_WIDTH
import neat
import time
import arcade
from arcade_snake import MyGame
import time


class ArcadeTrainer:
    # def __init__(self):
        # self.game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 10000, self.on_update)
        # self.game.setup()
        # self.left_paddle = self.game.paddle_list[0]
        # self.right_paddle = self.game.paddle_list[1]
        # self.ball = self.game.ball

    
    def train_ai(self, genome1, genome2, config):
        self.net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        self.net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        self.game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 120, self.on_update)
        self.game.setup()
        self.left_paddle = self.game.paddle_list[0]
        self.right_paddle = self.game.paddle_list[1]
        self.ball = self.game.ball
        arcade.run()
        
        genome1.fitness += self.game.left_hits
        genome2.fitness += self.game.right_hits

    def on_update(self):
        # input neurons `paddle positoon` `ball position` `ball paddle distanse`
        output1 = self.net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
        decision1= output1.index(max(output1))
        if decision1 == 0:
            pass
        elif decision1 == 1:
            self.game.move_paddle(left=True, up=True)
        else:
            self.game.move_paddle(left=True, up=False)
        start = time.time()
        output2 = self.net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
        end = time.time()
        # print(f'time to predict {end-start}')
        decision2= output2.index(max(output2))
        if decision2 == 0:
            pass
        elif decision2 == 1:
            self.game.move_paddle(left=False, up=True)
        else:
            self.game.move_paddle(left=False, up=False)

        if(self.game.left_score >= 1 or self.game.right_score >= 1 or self.game.left_hits > 50):
            # arcade.close_window()
            arcade.exit()
            arcade.close_window()
            # gc.collect()
            print(self.game.draw_count)
            print(self.game.update_count)
        