import random
from collections import OrderedDict
from card import Card
from cardpile import CardPile
from player import Player

class Game:
    def __init__(self):
        self.colors = ["red", "green", "blue", "white", "yellow"]
        self.init_deck()
        self.init_players()
        self.init_piles()

    def init_deck(self):
        self.deck = [Card(c, i) for c in self.colors for i in range(2,11)]
        multipliers = [Card(c, 1) for c in self.colors for _ in range(3)]
        self.deck.extend(multipliers)
        random.Random(1).shuffle(self.deck)

    def init_players(self):
        p1_hand = [self.deck.pop() for _ in range(8)]
        p2_hand = [self.deck.pop() for _ in range(8)]
        self.p1 = Player("p1", p1_hand)
        self.p2 = Player("p2", p2_hand)
        self.is_p1_turn = True

    def init_piles(self):
        self.piles = {}
        self.piles["board"] = OrderedDict([(c, CardPile(c, "board")) for c in self.colors])
        self.piles["p1"] = OrderedDict([(c, CardPile(c, "p1")) for c in self.colors])
        self.piles["p2"] = OrderedDict([(c, CardPile(c, "p2")) for c in self.colors])

    def print_hand(self, values, colors, color_map):
        color_value_pairs = ["".join(map(str, i)) for i in zip(colors, values)]
        print("\n[" + ", ".join(color_value_pairs) + color_map["white"] + "]\n")
        
    def print_board(self, values, color_map):
        color_value_pairs = ["".join(map(str, i)) for i in zip(list(color_map.values()), values)]
        print("\n[" + ", ".join(color_value_pairs) + color_map["white"] + \
                "]      [" + str(len(self.deck)) + "]\n")
        
    def print_piles(self, values2d, color_map):
        color_value_pairs = [[] for _ in range(len(list(zip(*values2d))))]
        for i, color_value_pair in enumerate(color_value_pairs):
            for j, color in enumerate(list(color_map.values())):
                color_value_pair.append("".join(map(str, (color, values2d[j][i]))))
            print("[" + ", ".join(color_value_pair) + color_map["white"] + "]")
            
    def create_2d_array_of_piles(self, p):
        p_piles = [[] for _ in self.colors]
        pile_lengths = [len(self.piles[p][c].pile) for c in self.colors]
        longest = max(pile_lengths)
        for i in range(longest):
            for j, color_pile in enumerate(list(self.piles[p].values())):
                if i < len(color_pile.pile):
                    p_piles[j].append(str(color_pile.pile[i].value))
                else:
                    p_piles[j].append(" ")
        return p_piles

    def print_game(self):
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        WHITE = "\033[37m"
        COLOR_MAP = OrderedDict([("red", RED), ("green", GREEN), ("blue", BLUE), \
                              ("white", WHITE), ("yellow", YELLOW)])

        p2_hand_values = [str(self.p2.hand[i].value) if i < len(self.p2.hand) else (" ") for i in range(8)]
        p2_hand_colors = [COLOR_MAP[self.p2.hand[i].color] if i < len(self.p2.hand) else WHITE for i in range(8)]
        p2_piles = self.create_2d_array_of_piles("p2")
        board = [str(self.piles["board"][pile].pile[-1].value) if not self.piles["board"][pile].is_empty() else "x" for pile in self.piles["board"]]
        p1_piles = self.create_2d_array_of_piles("p1")
        p1_hand_values = [str(self.p1.hand[i].value) if i < len(self.p1.hand) else " " for i in range(8)]
        p1_hand_colors = [COLOR_MAP[self.p1.hand[i].color] if i < len(self.p1.hand) else WHITE for i in range(8)]

        self.print_hand(p2_hand_values, p2_hand_colors, COLOR_MAP)
        if p2_piles:
            self.print_piles(p2_piles, COLOR_MAP)
        self.print_board(board, COLOR_MAP)
        if p1_piles:
            self.print_piles(p1_piles, COLOR_MAP)
        self.print_hand(p1_hand_values, p1_hand_colors, COLOR_MAP)
        print("")

    def player_turn(self, p):
        color = p.hand[0].color
        value = p.hand[0].value
        if value > 1:
            if not p.play_lowest_value_card(self.piles[p.name][color]):
                p.discard_lowest_value_card(self.piles["board"][color])
        else:
            if not p.play_multiplier_card(self.piles[p.name][color]):
                p.discard_multiplier_card(self.piles["board"][color])
        p.is_draw_phase = True
        
        if bool(random.getrandbits(1)):
            for pile in self.piles["board"]:
                if p.draw_card_from_pile(self.piles["board"][pile]):
                    if self.is_p1_turn:
                        self.is_p1_turn = False
                    else:
                        self.is_p1_turn = True
                    return
        p.draw_card_from_deck(self.deck)
        p.is_draw_phase = False
        if self.is_p1_turn:        
            self.is_p1_turn = False
        else:
            self.is_p1_turn = True

    def human_player_turn(self, card_to_play, pile_to_play):
        if not self.p1.is_draw_phase:
            if card_to_play is None or pile_to_play is None:
                return card_to_play, pile_to_play
            if pile_to_play.owner == "p1":
                if not self.p1.play_card(card_to_play, pile_to_play):
                    return card_to_play, None
            else:
                if not self.p1.discard_card(card_to_play, pile_to_play):
                    return card_to_play, None
            self.p1.is_draw_phase = True
            return None, None
        else:
            if pile_to_play is None:
                return card_to_play, pile_to_play
            if pile_to_play == "deck":
                self.p1.draw_card_from_deck(self.deck)
            else:
                if not self.p1.draw_card_from_pile(pile_to_play):
                    return None, None
            self.p1.is_draw_phase = False
            self.is_p1_turn = False
            return None, None

    def update_state(self):
        state = []
        # Player hand
        # (Color, Number) (Color, Number) ... 8 cards = 16 entries
        #  1    , 2        5    , 10
        hand_card_colors = [card.color for card in self.p1.hand]
        hand_card_values = [card.value for card in self.p1.hand]
        for i in range(8):
            if i < len(list(zip(hand_card_colors, hand_card_values))):
                state.extend([self.colors.index(hand_card_colors[i]) + 1, hand_card_values[i]])
            else:
                state.extend([0, 0])
        # Opponent piles
        # (Multiplier, 2, 3, 4, 5, ...) 10 values for 5 piles = 50 entries
        #  3         , 0, 1, 0, 1, ...
        for pile in self.piles["p2"]:
            multiplier = 1
            is_card_value = [0] * 9
            for card in self.piles["p2"][pile].pile:
                if card.value == 1:
                    multiplier += 1
                else:
                    is_card_value[card.value - 2] += 1
            state.append(multiplier)
            state.extend(is_card_value)
        # Board piles
        # (Top card of pile) 1 value for 5 piles = 5 entries
        board_values = [self.piles["board"][pile].pile[-1].value if not self.piles["board"][pile].is_empty() else 0 for pile in self.piles["board"]]
        state.extend(board_values)
        # Player piles
        # Same as opponent piles = 50 entries
        for pile in self.piles["p1"]:
            multiplier = 1
            is_card_value = [0] * 9
            for card in self.piles["p1"][pile].pile:
                if card.value == 1:
                    multiplier += 1
                else:
                    is_card_value[card.value - 2] += 1
            state.append(multiplier)
            state.extend(is_card_value)
        # Deck
        # Number of cards remaining <= 10
        cards_remaining = min(len(self.deck), 10)
        state.append(cards_remaining)
        return state
