from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
import os
from game import Game

class LostCitiesEnv(Env):

    def __init__(self):
        self.game = Game()
        self.action_space = Discrete(36)
        self.observation_space = Box(0, 10, shape=(122,), dtype=np.int8)
        self.state = self.game.update_state()

    def step(self, action_map):
        _score = self.game.p1.calculate_score(list(self.game.piles["p1"].values()))
        action = self.play_action(action_map)
        self.state = self.game.update_state()
        reward = self.game.p1.calculate_score(list(self.game.piles["p1"].values())) - _score
        info = {}
        if self.game.deck:
            done = False
        else:
            done = True
            return self.state, action, reward, done, info
        if not self.game.is_p1_turn:
            self.game.player_turn(self.game.p2)
        return self.state, action, reward, done, info

    def render(self):
        # self.game.print_game()
        pass

    def reset(self, **kwargs):
        self.game.__init__()
        self.state = self.game.update_state()
        info = {}
        return self.state, info

    def play_action(self, action_map):
        for action in action_map:
            match action:
                case 0:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_multiplier_card(self.game.piles["p1"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 1:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_lowest_value_card(self.game.piles["p1"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 2:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_highest_value_card(self.game.piles["p1"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 3:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_multiplier_card(self.game.piles["board"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 4:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_lowest_value_card(self.game.piles["board"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 5:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_highest_value_card(self.game.piles["board"]["red"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 6:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_multiplier_card(self.game.piles["p1"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 7:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_lowest_value_card(self.game.piles["p1"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 8:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_highest_value_card(self.game.piles["p1"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 9:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_multiplier_card(self.game.piles["board"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 10:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_lowest_value_card(self.game.piles["board"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 11:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_highest_value_card(self.game.piles["board"]["green"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 12:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_multiplier_card(self.game.piles["p1"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 13:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_lowest_value_card(self.game.piles["p1"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 14:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_highest_value_card(self.game.piles["p1"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 15:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_multiplier_card(self.game.piles["board"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 16:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_lowest_value_card(self.game.piles["board"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 17:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_highest_value_card(self.game.piles["board"]["blue"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 18:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_multiplier_card(self.game.piles["p1"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 19:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_lowest_value_card(self.game.piles["p1"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 20:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_highest_value_card(self.game.piles["p1"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 21:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_multiplier_card(self.game.piles["board"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 22:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_lowest_value_card(self.game.piles["board"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 23:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_highest_value_card(self.game.piles["board"]["white"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 24:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_multiplier_card(self.game.piles["p1"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 25:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_lowest_value_card(self.game.piles["p1"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 26:
                    if not self.game.p1.is_draw_phase and self.game.p1.play_highest_value_card(self.game.piles["p1"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 27:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_multiplier_card(self.game.piles["board"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 28:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_lowest_value_card(self.game.piles["board"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 29:
                    if not self.game.p1.is_draw_phase and self.game.p1.discard_highest_value_card(self.game.piles["board"]["yellow"]):
                        self.game.p1.is_draw_phase = True
                        return action
                case 30:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_pile(self.game.piles["board"]["red"]):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
                case 31:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_pile(self.game.piles["board"]["green"]):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
                case 32:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_pile(self.game.piles["board"]["blue"]):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
                case 33:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_pile(self.game.piles["board"]["white"]):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
                case 34:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_pile(self.game.piles["board"]["yellow"]):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
                case _:
                    if self.game.p1.is_draw_phase and self.game.p1.draw_card_from_deck(self.game.deck):
                        self.game.p1.is_draw_phase = False
                        self.game.is_p1_turn = False
                        return action
