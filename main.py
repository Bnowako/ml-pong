from re import T
from tkinter import W

from arcade_trainer import ArcadeTrainer
import neat
import os
import gc



# window = pygame.display.set_mode((WIDTH, HEIGHT))


def eval_genomes(genomes, config):
    width = 700
    height = 500
    # window = pygame.display.set_mode((width, height))
    # game = ArcadeTrainer(width, height)

    for i, (genome_id, genome1) in enumerate (genomes):
        print(f'Alll genomes: {len(genomes)}')
        if i == len(genomes) - 1: 
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            print(f'Training genome {i} against {genome_id2}.')
            game = ArcadeTrainer()
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            force_quit = game.train_ai(genome1, genome2, config)



def run_neat(config):
    p = neat.Population(config)
    # logs to std output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_neat(config)