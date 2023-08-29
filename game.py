import random
import pygame
from collections import OrderedDict
from sys import exit

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

class CardPile:
    def __init__(self, color, owner):
        self.color = color
        self.owner = owner
        self.pile = []
        self.score = 0

    def calculate_score(self):
        if not len(self.pile):
            return 0
        self.score = 0
        multiplier = 1
        for card in self.pile:
            if card.value == 1:
                multiplier += 1
            else:
                self.score += card.value
        self.score -= 20
        self.score *= multiplier
        if len(self.pile) >= 8:
            self.score += 20
        return self.score

    def is_empty(self):
        if self.pile:
            return False
        else:
            return True
            
    def remove_card(self):
        return self.pile.pop()

    def add_card(self, card):
        self.pile.append(card)

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.score = 0
        self.is_draw_phase = False

    def calculate_score(self, piles):
        self.score = 0
        for pile in piles:
            self.score += pile.calculate_score()
        return self.score

    def remove_card(self, card_index):
        return self.hand.pop(card_index)

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, card, pile):
        if (card in self.hand)\
                and (pile.is_empty() or pile.pile[-1].value < card.value or 1 == pile.pile[-1].value == card.value)\
                and (pile.color == card.color)\
                and (self.name == pile.owner):
            pile.add_card(self.remove_card(self.hand.index(card)))
            return True
        else:
            return False
        
    def discard_card(self, card, pile):
        if (card in self.hand)\
                and (pile.color == card.color)\
                and (pile.owner == "board"):
            pile.add_card(self.remove_card(self.hand.index(card)))
            return True
        else:
            return False
        
    def play_or_discard_multiplier_card(self, pile, is_play):
        for card in self.hand:
            if card.color == pile.color and card.value == 1:
                if is_play:
                    return self.play_card(card, pile)
                else:
                    return self.discard_card(card, pile)
        return False

    def play_or_discard_lowest_or_highest_value_card(self, pile, is_play, is_lowest):
        card_list = []
        card_value_list = []
        for card in self.hand:
            if card.color == pile.color and card.value > 1:
                card_list.append(card)
                card_value_list.append(card.value)
        if len(card_list):
            if is_play and is_lowest:
                return self.play_card(card_list[card_value_list.index(min(card_value_list))], pile)
            elif is_play and not is_lowest:
                return self.play_card(card_list[card_value_list.index(max(card_value_list))], pile)
            elif not is_play and is_lowest:
                return self.discard_card(card_list[card_value_list.index(min(card_value_list))], pile)
            else:
                return self.discard_card(card_list[card_value_list.index(max(card_value_list))], pile)
        return False
    
    # AI Actions
    def play_multiplier_card(self, player_pile):
        return self.play_or_discard_multiplier_card(player_pile, is_play=True)
    
    def play_lowest_value_card(self, player_pile):
        return self.play_or_discard_lowest_or_highest_value_card(player_pile, is_play=True, is_lowest=True)
    
    def play_highest_value_card(self, player_pile):
        return self.play_or_discard_lowest_or_highest_value_card(player_pile, is_play=True, is_lowest=False)

    def discard_multiplier_card(self, board_pile):
        return self.play_or_discard_multiplier_card(board_pile, is_play=False)
    
    def discard_lowest_value_card(self, board_pile):
        return self.play_or_discard_lowest_or_highest_value_card(board_pile, is_play=False, is_lowest=True)

    def discard_highest_value_card(self, board_pile):
        return self.play_or_discard_lowest_or_highest_value_card(board_pile, is_play=False, is_lowest=False)

    def draw_card_from_pile(self, board_pile):
        if board_pile.is_empty():
            return False
        else:
            self.add_card(board_pile.remove_card())
            return True
    
    def draw_card_from_deck(self, deck):
        self.add_card(deck.pop())
        return True

class Game:
    def __init__(self):
        self.init_deck()
        self.init_players()
        self.init_piles()

    def init_deck(self):
        self.deck = []
        for i in range(2,11):
            self.deck.append(Card("red", i))
            self.deck.append(Card("green", i))
            self.deck.append(Card("blue", i))
            self.deck.append(Card("white", i))
            self.deck.append(Card("yellow", i))
        for _ in range(3):
            self.deck.append(Card("red", 1))
            self.deck.append(Card("green", 1))
            self.deck.append(Card("blue", 1))
            self.deck.append(Card("white", 1))
            self.deck.append(Card("yellow", 1))
        random.Random(1).shuffle(self.deck)

    def init_players(self):
        p1_hand = []
        p2_hand = []
        for _ in range(8):
            p1_hand.append(self.deck.pop())
            p2_hand.append(self.deck.pop())
        self.p1 = Player("p1", p1_hand)
        self.p2 = Player("p2", p2_hand)
        self.is_p1_turn = True

    def init_piles(self):
        self.piles = {}
        self.piles["board"] = OrderedDict()
        self.piles["board"]["red"] = CardPile("red", "board")
        self.piles["board"]["green"] = CardPile("green", "board")
        self.piles["board"]["blue"] = CardPile("blue", "board")
        self.piles["board"]["white"] = CardPile("white", "board")
        self.piles["board"]["yellow"] = CardPile("yellow", "board")
        self.piles["p1"] = OrderedDict()
        self.piles["p1"]["red"] = CardPile("red", "p1")
        self.piles["p1"]["green"] = CardPile("green", "p1")
        self.piles["p1"]["blue"] = CardPile("blue", "p1")
        self.piles["p1"]["white"] = CardPile("white", "p1")
        self.piles["p1"]["yellow"] = CardPile("yellow", "p1")
        self.piles["p2"] = OrderedDict()
        self.piles["p2"]["red"] = CardPile("red", "p2")
        self.piles["p2"]["green"] = CardPile("green", "p2")
        self.piles["p2"]["blue"] = CardPile("blue", "p2")
        self.piles["p2"]["white"] = CardPile("white", "p2")
        self.piles["p2"]["yellow"] = CardPile("yellow", "p2")

    def print_hand(self, values, colors):
        print("\n[" + colors[0] + values[0] + ", "\
                    + colors[1] + values[1] + ", "\
                    + colors[2] + values[2] + ", "\
                    + colors[3] + values[3] + ", "\
                    + colors[4] + values[4] + ", "\
                    + colors[5] + values[5] + ", "\
                    + colors[6] + values[6] + ", "\
                    + colors[7] + values[7] + "\033[37m]\n")
        
    def print_board(self, values):
        print("\n[\033[31m" + values[0] + ", " +\
                "\033[32m" + values[1] + ", " +\
                "\033[34m" + values[2] + ", " +\
                "\033[37m" + values[3] + ", " +\
                "\033[33m" + values[4] + "\033[37m]      [" + \
                str(len(self.deck)) + "]\n")
        
    def print_piles(self, values2d):
        for i in range(len(values2d[0])):
            print("[\033[31m" + values2d[0][i] + ", " +\
                    "\033[32m" + values2d[1][i] + ", " +\
                    "\033[34m" + values2d[2][i] + ", " +\
                    "\033[37m" + values2d[3][i] + ", " +\
                    "\033[33m" + values2d[4][i] + "\033[37m]")
            
    def create_2d_array_of_piles(self, p):
        p_piles = [[],[],[],[],[]]
        longest = max([len(self.piles[p]["red"].pile),\
                    len(self.piles[p]["green"].pile),\
                    len(self.piles[p]["blue"].pile),\
                    len(self.piles[p]["white"].pile),\
                    len(self.piles[p]["yellow"].pile)])
        for i in range(longest):
            for j in range(len(self.piles[p])):
                if i < len(list(self.piles[p].values())[j].pile):
                    p_piles[j].append(str(list(self.piles[p].values())[j].pile[i].value))
                else:
                    p_piles[j].append(" ")
        return p_piles

    def print_game(self):
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        WHITE = "\033[37m"
        COLORS = OrderedDict([("red", RED), ("green", GREEN), ("blue", BLUE), \
                              ("white", WHITE), ("yellow", YELLOW)])

        p2_hand_values = []
        p2_hand_colors = []
        p2_piles = self.create_2d_array_of_piles("p2")
        board = []
        p1_piles = self.create_2d_array_of_piles("p1")
        p1_hand_values = []
        p1_hand_colors = []

        for i in range(8):
            if i < len(self.p2.hand):
                p2_hand_values.append(str(self.p2.hand[i].value))
                p2_hand_colors.append(COLORS[self.p2.hand[i].color])
            else:
                p2_hand_values.append(" ")
                p2_hand_colors.append(WHITE)
            if i < len(self.p1.hand):
                p1_hand_values.append(str(self.p1.hand[i].value))
                p1_hand_colors.append(COLORS[self.p1.hand[i].color])
            else:
                p1_hand_values.append(" ")
                p1_hand_colors.append(WHITE)

        for pile in self.piles["board"]:
            if self.piles["board"][pile].is_empty():
                board.append("x")
            else:
                board.append(str(self.piles["board"][pile].pile[-1].value))

        self.print_hand(p2_hand_values, p2_hand_colors)
        if len(p2_piles):
            self.print_piles(p2_piles)
        self.print_board(board)
        if len(p1_piles):
            self.print_piles(p1_piles)
        self.print_hand(p1_hand_values, p1_hand_colors)
        print("")

def player_turn(game, p):
    color = p.hand[0].color
    value = p.hand[0].value
    if value > 1:
        if not p.play_lowest_value_card(game.piles[p.name][color]):
            p.discard_lowest_value_card(game.piles["board"][color])
    else:
        if not p.play_multiplier_card(game.piles[p.name][color]):
            p.discard_multiplier_card(game.piles["board"][color])
    p.is_draw_phase = True
    
    if bool(random.getrandbits(1)):
        for pile in game.piles["board"]:
            if p.draw_card_from_pile(game.piles["board"][pile]):
                if game.is_p1_turn:
                    game.is_p1_turn = False
                else:
                    game.is_p1_turn = True
                return
    p.draw_card_from_deck(game.deck)
    p.is_draw_phase = False
    if game.is_p1_turn:        
        game.is_p1_turn = False
    else:
        game.is_p1_turn = True

pygame.init()
screen = pygame.display.set_mode((800,1200))
screen.fill("green4")
font = pygame.font.Font(None, 64)
pygame.display.set_caption("Lost Cities")
clock = pygame.time.Clock()

BOARD_SURF = pygame.image.load("images/gameboard.png")
BOARD_RECT = BOARD_SURF.get_rect(center = ((screen.get_width()/2)-50,screen.get_height()/2))
CARDBACK_SURF = pygame.image.load("images/cardback.png")
RED_CARD_SURF    = [pygame.image.load("images/red1.png"), pygame.image.load("images/red2.png"), \
                    pygame.image.load("images/red3.png"), pygame.image.load("images/red4.png"), \
                    pygame.image.load("images/red5.png"), pygame.image.load("images/red6.png"), \
                    pygame.image.load("images/red7.png"), pygame.image.load("images/red8.png"), \
                    pygame.image.load("images/red9.png"), pygame.image.load("images/red10.png")]
GREEN_CARD_SURF  = [pygame.image.load("images/green1.png"), pygame.image.load("images/green2.png"), \
                    pygame.image.load("images/green3.png"), pygame.image.load("images/green4.png"), \
                    pygame.image.load("images/green5.png"), pygame.image.load("images/green6.png"), \
                    pygame.image.load("images/green7.png"), pygame.image.load("images/green8.png"), \
                    pygame.image.load("images/green9.png"), pygame.image.load("images/green10.png")]
BLUE_CARD_SURF   = [pygame.image.load("images/blue1.png"), pygame.image.load("images/blue2.png"), \
                    pygame.image.load("images/blue3.png"), pygame.image.load("images/blue4.png"), \
                    pygame.image.load("images/blue5.png"), pygame.image.load("images/blue6.png"), \
                    pygame.image.load("images/blue7.png"), pygame.image.load("images/blue8.png"), \
                    pygame.image.load("images/blue9.png"), pygame.image.load("images/blue10.png")]
WHITE_CARD_SURF  = [pygame.image.load("images/white1.png"), pygame.image.load("images/white2.png"), \
                    pygame.image.load("images/white3.png"), pygame.image.load("images/white4.png"), \
                    pygame.image.load("images/white5.png"), pygame.image.load("images/white6.png"), \
                    pygame.image.load("images/white7.png"), pygame.image.load("images/white8.png"), \
                    pygame.image.load("images/white9.png"), pygame.image.load("images/white10.png")]
YELLOW_CARD_SURF = [pygame.image.load("images/yellow1.png"), pygame.image.load("images/yellow2.png"), \
                    pygame.image.load("images/yellow3.png"), pygame.image.load("images/yellow4.png"), \
                    pygame.image.load("images/yellow5.png"), pygame.image.load("images/yellow6.png"), \
                    pygame.image.load("images/yellow7.png"), pygame.image.load("images/yellow8.png"), \
                    pygame.image.load("images/yellow9.png"), pygame.image.load("images/yellow10.png")]
COLOR_CARD_SURF = OrderedDict([("red", RED_CARD_SURF), ("green", GREEN_CARD_SURF), ("blue", BLUE_CARD_SURF),\
                    ("white", WHITE_CARD_SURF), ("yellow", YELLOW_CARD_SURF)])
BG_SURF = pygame.Surface((CARDBACK_SURF.get_size()))
BG_SURF.fill("green4")
PLAYER1_HAND_RECT = []
PLAYER2_HAND_RECT = []
for i in range(8):
    PLAYER1_HAND_RECT.append(CARDBACK_SURF.get_rect(center = (screen.get_width()*(((i*2)+1)/16), screen.get_height()*(15/16))))
    PLAYER2_HAND_RECT.append(CARDBACK_SURF.get_rect(center = (screen.get_width()*(((i*2)+1)/16), screen.get_height()*(1/16))))
DECK_RECT = CARDBACK_SURF.get_rect(midleft = (BOARD_RECT.right + 15, screen.get_height()/2))
RED_BOARD_RECT = pygame.Rect(BOARD_RECT.left+4,BOARD_RECT.top,98,153)
GREEN_BOARD_RECT = pygame.Rect(BOARD_RECT.left+102,BOARD_RECT.top,98,153)
BLUE_BOARD_RECT = pygame.Rect(BOARD_RECT.left+200,BOARD_RECT.top,98,153)
WHITE_BOARD_RECT = pygame.Rect(BOARD_RECT.left+298,BOARD_RECT.top,98,153)
YELLOW_BOARD_RECT = pygame.Rect(BOARD_RECT.left+396,BOARD_RECT.top,98,153)
COLOR_BOARD_RECT = OrderedDict([("red", RED_BOARD_RECT), ("green", GREEN_BOARD_RECT), ("blue", BLUE_BOARD_RECT),\
                    ("white", WHITE_BOARD_RECT), ("yellow", YELLOW_BOARD_RECT)])
PLAYER1_PILES_RECT = []
PLAYER2_PILES_RECT = []
for j in range(len(COLOR_BOARD_RECT)):
    PLAYER1_PILES_RECT.append(pygame.Rect(list(COLOR_BOARD_RECT.values())[j].left,list(COLOR_BOARD_RECT.values())[j].bottom+30,\
                    list(COLOR_BOARD_RECT.values())[j].width,screen.get_height()*(15/16)-180-list(COLOR_BOARD_RECT.values())[j].bottom))
    PLAYER2_PILES_RECT.append(pygame.Rect(list(COLOR_BOARD_RECT.values())[j].left,screen.get_height()*(1/16)+150,\
                    list(COLOR_BOARD_RECT.values())[j].width,list(COLOR_BOARD_RECT.values())[j].top-(screen.get_height()*(1/16)+180)))

def draw_p_piles(values2d, p):
    for i in range(len(values2d[0])):
        for j in range(len(COLOR_CARD_SURF)):
            if values2d[j][i] != " ":
                if p == "p1":
                    screen.blit(list(COLOR_CARD_SURF.values())[j][int(values2d[j][i])-1],\
                            (PLAYER1_PILES_RECT[j].left+5,PLAYER1_PILES_RECT[j].top+(i*30)))
                elif p == "p2":
                    screen.blit(list(COLOR_CARD_SURF.values())[j][int(values2d[j][i])-1],\
                            (PLAYER2_PILES_RECT[j].left+7,PLAYER2_PILES_RECT[j].bottom-CARDBACK_SURF.get_height()-(i*30)))

def draw_p1_hand(values, colors):
    screen.blit(BG_SURF,PLAYER1_HAND_RECT[7].topleft)
    for i in range(len(values)):
        screen.blit(COLOR_CARD_SURF[colors[i]][values[i]-1],PLAYER1_HAND_RECT[i])

def draw_p2_hand():
    for i in range(8):
        screen.blit(CARDBACK_SURF,PLAYER2_HAND_RECT[i])

def draw_board(values):
    for j in range(len(COLOR_CARD_SURF)):
        if values[j] > 0:
            screen.blit(list(COLOR_CARD_SURF.values())[j][values[j]-1],\
                    (list(COLOR_BOARD_RECT.values())[j].left+5,list(COLOR_BOARD_RECT.values())[j].top+10))

def draw_deck(deck_length):
    screen.blit(CARDBACK_SURF,DECK_RECT)
    text = font.render(str(deck_length), True, "white")
    textRect = text.get_rect()
    textRect.center = DECK_RECT.center
    screen.blit(text, textRect)

def draw_game(game):
    p2_piles = game.create_2d_array_of_piles("p2")
    board_values = []
    p1_piles = game.create_2d_array_of_piles("p1")
    p1_hand_values = []
    p1_hand_colors = []

    for i in range(len(game.p1.hand)):
        p1_hand_values.append(game.p1.hand[i].value)
        p1_hand_colors.append(game.p1.hand[i].color)

    for pile in game.piles["board"]:
        if game.piles["board"][pile].is_empty():
            board_values.append(0)
        else:
            board_values.append(game.piles["board"][pile].pile[-1].value)

    draw_p2_hand()
    draw_p_piles(p2_piles, "p2")
    draw_board(board_values)
    draw_deck(len(game.deck))
    draw_p_piles(p1_piles, "p1")
    draw_p1_hand(p1_hand_values, p1_hand_colors)
    if len(game.deck) <= 0:
        game_over(game)

def human_player_turn(game, card_to_play, pile_to_play):
    if not game.p1.is_draw_phase:
        if card_to_play is None or pile_to_play is None:
            return card_to_play, pile_to_play
        if pile_to_play.owner == "p1":
            if not game.p1.play_card(card_to_play, pile_to_play):
                return None, None
        else:
            if not game.p1.discard_card(card_to_play, pile_to_play):
                return None, None
        game.p1.is_draw_phase = True
        return None, None
    else:
        if pile_to_play is None:
            return card_to_play, pile_to_play
        if pile_to_play == "deck":
            game.p1.draw_card_from_deck(game.deck)
        else:
            if not game.p1.draw_card_from_pile(pile_to_play):
                return None, None
        game.p1.is_draw_phase = False
        game.is_p1_turn = False
        return None, None

def get_clicked_card(mouse_pos, game, card_to_play):
    if not game.p1.is_draw_phase:
        if card_to_play is None:
            for i in range(len(PLAYER1_HAND_RECT)):
                if PLAYER1_HAND_RECT[i].collidepoint(mouse_pos):
                    return game.p1.hand[i], None
        else:
            for i in range(len(PLAYER1_PILES_RECT)):
                if PLAYER1_PILES_RECT[i].collidepoint(mouse_pos):
                    return card_to_play, list(game.piles["p1"].values())[i]
            for j in range(len(COLOR_BOARD_RECT)):
                if list(COLOR_BOARD_RECT.values())[j].collidepoint(mouse_pos):
                    return card_to_play, list(game.piles["board"].values())[j]
    else:
        for j in range(len(COLOR_BOARD_RECT)):
            if list(COLOR_BOARD_RECT.values())[j].collidepoint(mouse_pos):
                return card_to_play, list(game.piles["board"].values())[j]
        if DECK_RECT.collidepoint(mouse_pos):
            return card_to_play, "deck"
    return None, None

def game_over(game):
    p1_score = game.p1.calculate_score(game.piles["p1"].values())
    p2_score = game.p2.calculate_score(game.piles["p2"].values())
    message = ""
    if p1_score > p2_score:
        message = "YOU WIN!"
    elif p1_score < p2_score:
        message = "P2 WINS"
    else:
        message = "TIE"
    p1_text = font.render(str(p1_score), True, "white")
    p2_text = font.render(str(p2_score), True, "white")
    message_text = font.render(message, True, "white")
    p1_text_rect = p1_text.get_rect()
    p2_text_rect = p2_text.get_rect()
    message_rect = message_text.get_rect()
    p1_text_rect.center = PLAYER1_PILES_RECT[2].center
    p2_text_rect.center = PLAYER2_PILES_RECT[2].center
    message_rect.center = BOARD_RECT.center
    screen.blit(p1_text, p1_text_rect)
    screen.blit(p2_text, p2_text_rect)
    screen.blit(message_text, message_rect)

game = Game()
is_human_player = False
card_to_play = None
pile_to_play = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            card_to_play, pile_to_play = get_clicked_card(event.pos, game, card_to_play)

    if len(game.deck) > 0:
        if game.is_p1_turn:
            if is_human_player:
                card_to_play, pile_to_play = human_player_turn(game, card_to_play, pile_to_play)
            else:
                player_turn(game, game.p1)
        else:
            player_turn(game, game.p2)
            
    screen.blit(BOARD_SURF,BOARD_RECT)
    draw_game(game)

    pygame.display.update()
    clock.tick(60)
