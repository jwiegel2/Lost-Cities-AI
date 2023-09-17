import pygame
from sys import exit
from game import Game
from gui import Gui
from dqn_torch import Agent
from lostcitiesenv import LostCitiesEnv
from stable_baselines3.common.env_checker import check_env
import numpy as np

env = LostCitiesEnv()
env.observation_space.sample()
env.reset()
# check_env(env, warn=True)
agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=36, eps_end=0.01, input_dims=[122], lr=0.0001)
scores, eps_history = [], []
n_games = 500

for i in range(n_games):
    score = 0
    done = False
    observation = env.reset()[0]
    while not done:
        action_map = agent.choose_action(observation)
        observation_, action, reward, done, info = env.step(action_map)
        env.render()
        score += reward
        agent.store_transition(observation, action, reward, observation_, done)
        agent.learn()
        observation = observation_
    scores.append(score)
    eps_history.append(agent.epsilon)

    avg_score = np.mean(scores[-100:])

    print("episode", i, "score %.2f" % score,
            "average score %.2f" % avg_score,
            "epsilon %.3f" % agent.epsilon)

# game = Game()
# gui = Gui()
# is_human_player = False
# card_to_play = None
# pile_to_play = None

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         if event.type == pygame.MOUSEBUTTONUP:
#             card_to_play, pile_to_play = gui.get_clicked_card(event.pos, game, card_to_play)

#     if game.deck:
#         if game.is_p1_turn:
#             if is_human_player:
#                 card_to_play, pile_to_play = game.human_player_turn(game, card_to_play, pile_to_play)
#             else:
#                 game.player_turn(game.p1)
#         else:
#             game.player_turn(game.p2)
            
#     gui.screen.blit(gui.BOARD_SURF,gui.BOARD_RECT)
#     gui.draw_game(game)

#     pygame.display.update()
#     gui.clock.tick(60)
