import random
import pygame
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
            return
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

    def calculate_score(self, piles):
        for pile in piles:
            self.score += pile.calculate_score()
        return self.score

    def remove_card(self, card_index):
        return self.hand.pop(card_index)

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, card, pile):
        if (card in self.hand)\
                and (pile.is_empty() or pile.pile[-1].value < card.value)\
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
        self.piles["board"] = {}
        self.piles["board"]["red"] = CardPile("red", "board")
        self.piles["board"]["green"] = CardPile("green", "board")
        self.piles["board"]["blue"] = CardPile("blue", "board")
        self.piles["board"]["white"] = CardPile("white", "board")
        self.piles["board"]["yellow"] = CardPile("yellow", "board")
        self.piles["p1"] = {}
        self.piles["p1"]["red"] = CardPile("red", "p1")
        self.piles["p1"]["green"] = CardPile("green", "p1")
        self.piles["p1"]["blue"] = CardPile("blue", "p1")
        self.piles["p1"]["white"] = CardPile("white", "p1")
        self.piles["p1"]["yellow"] = CardPile("yellow", "p1")
        self.piles["p2"] = {}
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
            if i < len(self.piles[p]["red"].pile):
                p_piles[0].append(str(self.piles[p]["red"].pile[i].value))
            else:
                p_piles[0].append(" ")
            if i < len(self.piles[p]["green"].pile):
                p_piles[1].append(str(self.piles[p]["green"].pile[i].value))
            else:
                p_piles[1].append(" ")
            if i < len(self.piles[p]["blue"].pile):
                p_piles[2].append(str(self.piles[p]["blue"].pile[i].value))
            else:
                p_piles[2].append(" ")
            if i < len(self.piles[p]["white"].pile):
                p_piles[3].append(str(self.piles[p]["white"].pile[i].value))
            else:
                p_piles[3].append(" ")
            if i < len(self.piles[p]["yellow"].pile):
                p_piles[4].append(str(self.piles[p]["yellow"].pile[i].value))
            else:
                p_piles[4].append(" ")
        return p_piles

    def print_game(self):
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        WHITE = "\033[37m"

        p2_hand_values = []
        p2_hand_colors = []
        p2_piles = self.create_2d_array_of_piles("p2")
        board = []
        p1_piles = self.create_2d_array_of_piles("p1")
        p1_hand_values = []
        p1_hand_colors = []

        for i in range(len(self.p1.hand)):
            p2_hand_values.append(str(self.p2.hand[i].value))
            if self.p2.hand[i].color == "red":
                p2_hand_colors.append(RED)
            elif self.p2.hand[i].color == "green":
                p2_hand_colors.append(GREEN)
            elif self.p2.hand[i].color == "blue":
                p2_hand_colors.append(BLUE)
            elif self.p2.hand[i].color == "white":
                p2_hand_colors.append(WHITE)
            elif self.p2.hand[i].color == "yellow":
                p2_hand_colors.append(YELLOW)
            p1_hand_values.append(str(self.p1.hand[i].value))
            if self.p1.hand[i].color == "red":
                p1_hand_colors.append(RED)
            elif self.p1.hand[i].color == "green":
                p1_hand_colors.append(GREEN)
            elif self.p1.hand[i].color == "blue":
                p1_hand_colors.append(BLUE)
            elif self.p1.hand[i].color == "white":
                p1_hand_colors.append(WHITE)
            elif self.p1.hand[i].color == "yellow":
                p1_hand_colors.append(YELLOW)
        
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
    
    if bool(random.getrandbits(1)):
        for pile in game.piles["board"]:
            if p.draw_card_from_pile(game.piles["board"][pile]):
                if game.is_p1_turn:
                    game.is_p1_turn = False
                else:
                    game.is_p1_turn = True
                return
    p.draw_card_from_deck(game.deck)
    if game.is_p1_turn:        
        game.is_p1_turn = False
    else:
        game.is_p1_turn = True

pygame.init()
screen = pygame.display.set_mode((800,1200))
screen.fill("green4")
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
CARD_SURF = {"red": RED_CARD_SURF, "green": GREEN_CARD_SURF, "blue": BLUE_CARD_SURF, \
             "white": WHITE_CARD_SURF, "yellow": YELLOW_CARD_SURF}
PLAYER1_HAND_RECT = [CARDBACK_SURF.get_rect(center = (screen.get_width()*(1/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(3/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(5/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(7/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(9/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(11/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(13/16), screen.get_height()*(15/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(15/16), screen.get_height()*(15/16)))]
PLAYER2_HAND_RECT = [CARDBACK_SURF.get_rect(center = (screen.get_width()*(1/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(3/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(5/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(7/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(9/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(11/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(13/16), screen.get_height()*(1/16))), \
                    CARDBACK_SURF.get_rect(center = (screen.get_width()*(15/16), screen.get_height()*(1/16)))]
DECK_RECT = CARDBACK_SURF.get_rect(midleft = (BOARD_RECT.right + 15, screen.get_height()/2))
RED_BOARD_RECT = pygame.Rect(BOARD_RECT.left,BOARD_RECT.top,102,153)
GREEN_BOARD_RECT = pygame.Rect(BOARD_RECT.left+102,BOARD_RECT.top,98,153)
BLUE_BOARD_RECT = pygame.Rect(BOARD_RECT.left+200,BOARD_RECT.top,98,153)
WHITE_BOARD_RECT = pygame.Rect(BOARD_RECT.left+298,BOARD_RECT.top,98,153)
YELLOW_BOARD_RECT = pygame.Rect(BOARD_RECT.left+396,BOARD_RECT.top,102,153)
PLAYER1_PILES_RECT = [pygame.Rect(RED_BOARD_RECT.left,RED_BOARD_RECT.bottom+30,\
                    RED_BOARD_RECT.width,screen.get_height()*(15/16)-150-RED_BOARD_RECT.top), \
                    pygame.Rect(GREEN_BOARD_RECT.left,GREEN_BOARD_RECT.bottom+30,\
                    GREEN_BOARD_RECT.width,screen.get_height()*(15/16)-150-GREEN_BOARD_RECT.top), \
                    pygame.Rect(BLUE_BOARD_RECT.left,BLUE_BOARD_RECT.bottom+30,\
                    BLUE_BOARD_RECT.width,screen.get_height()*(15/16)-150-BLUE_BOARD_RECT.top), \
                    pygame.Rect(WHITE_BOARD_RECT.left,WHITE_BOARD_RECT.bottom+30,\
                    WHITE_BOARD_RECT.width,screen.get_height()*(15/16)-150-WHITE_BOARD_RECT.top), \
                    pygame.Rect(YELLOW_BOARD_RECT.left,YELLOW_BOARD_RECT.bottom+30,\
                    YELLOW_BOARD_RECT.width,screen.get_height()*(15/16)-150-YELLOW_BOARD_RECT.top)]
PLAYER2_PILES_RECT = [pygame.Rect(RED_BOARD_RECT.left,screen.get_height()*(1/16)+150,\
                    RED_BOARD_RECT.width,RED_BOARD_RECT.top-(screen.get_height()*(1/16)+180)), \
                    pygame.Rect(GREEN_BOARD_RECT.left,screen.get_height()*(1/16)+150,\
                    GREEN_BOARD_RECT.width,GREEN_BOARD_RECT.top-(screen.get_height()*(1/16)+180)), \
                    pygame.Rect(BLUE_BOARD_RECT.left,screen.get_height()*(1/16)+150,\
                    BLUE_BOARD_RECT.width,BLUE_BOARD_RECT.top-(screen.get_height()*(1/16)+180)), \
                    pygame.Rect(WHITE_BOARD_RECT.left,screen.get_height()*(1/16)+150,\
                    WHITE_BOARD_RECT.width,WHITE_BOARD_RECT.top-(screen.get_height()*(1/16)+180)), \
                    pygame.Rect(WHITE_BOARD_RECT.left,screen.get_height()*(1/16)+150,\
                    YELLOW_BOARD_RECT.width,YELLOW_BOARD_RECT.top-(screen.get_height()*(1/16)+180))]

def draw_p1_piles(values2d):
    for i in range(len(values2d[0])):
        if values2d[0][i] != " ":
            screen.blit(RED_CARD_SURF[int(values2d[0][i])-1],(PLAYER1_PILES_RECT[0].left+7,PLAYER1_PILES_RECT[0].top+(i*30)))
        if values2d[1][i] != " ":
            screen.blit(GREEN_CARD_SURF[int(values2d[1][i])-1],(PLAYER1_PILES_RECT[1].left+5,PLAYER1_PILES_RECT[1].top+(i*30)))
        if values2d[2][i] != " ":
            screen.blit(BLUE_CARD_SURF[int(values2d[2][i])-1],(PLAYER1_PILES_RECT[2].left+5,PLAYER1_PILES_RECT[2].top+(i*30)))
        if values2d[3][i] != " ":
            screen.blit(WHITE_CARD_SURF[int(values2d[3][i])-1],(PLAYER1_PILES_RECT[3].left+5,PLAYER1_PILES_RECT[3].top+(i*30)))
        if values2d[4][i] != " ":
            screen.blit(YELLOW_CARD_SURF[int(values2d[4][i])-1],(PLAYER1_PILES_RECT[4].left+5,PLAYER1_PILES_RECT[4].top+(i*30)))

def draw_p2_piles(values2d):
    for i in range(len(values2d[0])):
        if values2d[0][i] != " ":
            screen.blit(RED_CARD_SURF[int(values2d[0][i])-1],(PLAYER2_PILES_RECT[0].left+7,PLAYER2_PILES_RECT[0].bottom-CARDBACK_SURF.get_height()-(i*30)))
        if values2d[1][i] != " ":
            screen.blit(GREEN_CARD_SURF[int(values2d[1][i])-1],(PLAYER2_PILES_RECT[1].left+5,PLAYER2_PILES_RECT[1].bottom-CARDBACK_SURF.get_height()-(i*30)))
        if values2d[2][i] != " ":
            screen.blit(BLUE_CARD_SURF[int(values2d[2][i])-1],(PLAYER2_PILES_RECT[2].left+5,PLAYER2_PILES_RECT[2].bottom-CARDBACK_SURF.get_height()-(i*30)))
        if values2d[3][i] != " ":
            screen.blit(WHITE_CARD_SURF[int(values2d[3][i])-1],(PLAYER2_PILES_RECT[3].left+5,PLAYER2_PILES_RECT[3].bottom-CARDBACK_SURF.get_height()-(i*30)))
        if values2d[4][i] != " ":
            screen.blit(YELLOW_CARD_SURF[int(values2d[4][i])-1],(PLAYER2_PILES_RECT[4].left+5,PLAYER2_PILES_RECT[4].bottom-CARDBACK_SURF.get_height()-(i*30)))

def draw_p1_hand(values, colors):
    for i in range(len(values)):
        screen.blit(CARD_SURF[colors[i]][values[i]-1],PLAYER1_HAND_RECT[i])

def draw_p2_hand():
    for i in range(8):
        screen.blit(CARDBACK_SURF,PLAYER2_HAND_RECT[i])

def draw_board(values):
    #TODO: this is wrong
    if values[0] > 0:
        screen.blit(RED_CARD_SURF[values[0]-1],(RED_BOARD_RECT.left+7,RED_BOARD_RECT.top+10))
        screen.blit(BLUE_CARD_SURF[values[1]-1],(BLUE_BOARD_RECT.left+5,BLUE_BOARD_RECT.top+10))
        screen.blit(GREEN_CARD_SURF[values[2]-1],(GREEN_BOARD_RECT.left+5,GREEN_BOARD_RECT.top+10))
        screen.blit(WHITE_CARD_SURF[values[3]-1],(WHITE_BOARD_RECT.left+5,WHITE_BOARD_RECT.top+10))
        screen.blit(YELLOW_CARD_SURF[values[4]-1],(YELLOW_BOARD_RECT.left+5,YELLOW_BOARD_RECT.top+10))

def draw_deck():
    screen.blit(CARDBACK_SURF,DECK_RECT)

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
    draw_p2_piles(p2_piles)
    draw_board(board_values)
    draw_deck()
    draw_p1_piles(p1_piles)
    draw_p1_hand(p1_hand_values, p1_hand_colors)

game = Game()
game.print_game()
screen.blit(BOARD_SURF,BOARD_RECT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    while len(game.deck) > 0:
        if game.is_p1_turn:
            player_turn(game, game.p1)
        else:
            player_turn(game, game.p2)

        game.print_game()
        draw_game(game)

        pygame.display.update()
        clock.tick(60)

print("P1: " + str(game.p1.calculate_score(game.piles["p1"].values())))
print("P2: " + str(game.p2.calculate_score(game.piles["p2"].values())))
