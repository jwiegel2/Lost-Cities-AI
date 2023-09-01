import pygame
from collections import OrderedDict

class Gui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,1200))
        self.screen.fill("green4")
        self.font = pygame.font.Font(None, 64)
        pygame.display.set_caption("Lost Cities")
        self.clock = pygame.time.Clock()

        self.BOARD_SURF = pygame.image.load("images/gameboard.png")
        self.BOARD_RECT = self.BOARD_SURF.get_rect(center = ((self.screen.get_width()/2)-50,self.screen.get_height()/2))
        self.CARDBACK_SURF = pygame.image.load("images/cardback.png")
        self.RED_CARD_SURF    = [pygame.image.load("images/red1.png"), pygame.image.load("images/red2.png"), \
                            pygame.image.load("images/red3.png"), pygame.image.load("images/red4.png"), \
                            pygame.image.load("images/red5.png"), pygame.image.load("images/red6.png"), \
                            pygame.image.load("images/red7.png"), pygame.image.load("images/red8.png"), \
                            pygame.image.load("images/red9.png"), pygame.image.load("images/red10.png")]
        self.GREEN_CARD_SURF  = [pygame.image.load("images/green1.png"), pygame.image.load("images/green2.png"), \
                            pygame.image.load("images/green3.png"), pygame.image.load("images/green4.png"), \
                            pygame.image.load("images/green5.png"), pygame.image.load("images/green6.png"), \
                            pygame.image.load("images/green7.png"), pygame.image.load("images/green8.png"), \
                            pygame.image.load("images/green9.png"), pygame.image.load("images/green10.png")]
        self.BLUE_CARD_SURF   = [pygame.image.load("images/blue1.png"), pygame.image.load("images/blue2.png"), \
                            pygame.image.load("images/blue3.png"), pygame.image.load("images/blue4.png"), \
                            pygame.image.load("images/blue5.png"), pygame.image.load("images/blue6.png"), \
                            pygame.image.load("images/blue7.png"), pygame.image.load("images/blue8.png"), \
                            pygame.image.load("images/blue9.png"), pygame.image.load("images/blue10.png")]
        self.WHITE_CARD_SURF  = [pygame.image.load("images/white1.png"), pygame.image.load("images/white2.png"), \
                            pygame.image.load("images/white3.png"), pygame.image.load("images/white4.png"), \
                            pygame.image.load("images/white5.png"), pygame.image.load("images/white6.png"), \
                            pygame.image.load("images/white7.png"), pygame.image.load("images/white8.png"), \
                            pygame.image.load("images/white9.png"), pygame.image.load("images/white10.png")]
        self.YELLOW_CARD_SURF = [pygame.image.load("images/yellow1.png"), pygame.image.load("images/yellow2.png"), \
                            pygame.image.load("images/yellow3.png"), pygame.image.load("images/yellow4.png"), \
                            pygame.image.load("images/yellow5.png"), pygame.image.load("images/yellow6.png"), \
                            pygame.image.load("images/yellow7.png"), pygame.image.load("images/yellow8.png"), \
                            pygame.image.load("images/yellow9.png"), pygame.image.load("images/yellow10.png")]
        self.COLOR_CARD_SURF = OrderedDict([("red", self.RED_CARD_SURF), ("green", self.GREEN_CARD_SURF), ("blue", self.BLUE_CARD_SURF),\
                            ("white", self.WHITE_CARD_SURF), ("yellow", self.YELLOW_CARD_SURF)])
        self.BG_SURF = pygame.Surface((self.CARDBACK_SURF.get_size()))
        self.BG_SURF.fill("green4")
        self.PLAYER1_HAND_RECT = [self.CARDBACK_SURF.get_rect(center = (self.screen.get_width()*(((i*2)+1)/16), self.screen.get_height()*(15/16)))\
                            for i in range(8)]
        self.PLAYER2_HAND_RECT = [self.CARDBACK_SURF.get_rect(center = (self.screen.get_width()*(((i*2)+1)/16), self.screen.get_height()*(1/16)))\
                            for i in range(8)]
        self.DECK_RECT = self.CARDBACK_SURF.get_rect(midleft = (self.BOARD_RECT.right + 15, self.screen.get_height()/2))
        self.RED_BOARD_RECT = pygame.Rect(self.BOARD_RECT.left+4,self.BOARD_RECT.top,98,153)
        self.GREEN_BOARD_RECT = pygame.Rect(self.BOARD_RECT.left+102,self.BOARD_RECT.top,98,153)
        self.BLUE_BOARD_RECT = pygame.Rect(self.BOARD_RECT.left+200,self.BOARD_RECT.top,98,153)
        self.WHITE_BOARD_RECT = pygame.Rect(self.BOARD_RECT.left+298,self.BOARD_RECT.top,98,153)
        self.YELLOW_BOARD_RECT = pygame.Rect(self.BOARD_RECT.left+396,self.BOARD_RECT.top,98,153)
        self.COLOR_BOARD_RECT = OrderedDict([("red", self.RED_BOARD_RECT), ("green", self.GREEN_BOARD_RECT), ("blue", self.BLUE_BOARD_RECT),\
                            ("white", self.WHITE_BOARD_RECT), ("yellow", self.YELLOW_BOARD_RECT)])
        self.PLAYER1_PILES_RECT = [pygame.Rect(c_board_rect.left,c_board_rect.bottom+30,\
                            c_board_rect.width,self.screen.get_height()*(15/16)-180-c_board_rect.bottom)\
                            for c_board_rect in list(self.COLOR_BOARD_RECT.values())]
        self.PLAYER2_PILES_RECT = [pygame.Rect(c_board_rect.left,self.screen.get_height()*(1/16)+150,\
                            c_board_rect.width,c_board_rect.top-(self.screen.get_height()*(1/16)+180))\
                            for c_board_rect in list(self.COLOR_BOARD_RECT.values())]

    def draw_p_piles(self, values2d, p):
        for i in range(len(list(zip(*values2d)))):
            for j, c_card_surf in enumerate(list(self.COLOR_CARD_SURF.values())):
                if values2d[j][i] != " ":
                    if p == "p1":
                        self.screen.blit(c_card_surf[int(values2d[j][i])-1],\
                                (self.PLAYER1_PILES_RECT[j].left+5,self.PLAYER1_PILES_RECT[j].top+(i*30)))
                    elif p == "p2":
                        self.screen.blit(c_card_surf[int(values2d[j][i])-1],\
                                (self.PLAYER2_PILES_RECT[j].left+5,self.PLAYER2_PILES_RECT[j].bottom-self.CARDBACK_SURF.get_height()-(i*30)))

    def draw_p1_hand(self, values, colors):
        self.screen.blit(self.BG_SURF,self.PLAYER1_HAND_RECT[7].topleft)
        for i, (value, color) in enumerate(zip(values, colors)):
            self.screen.blit(self.COLOR_CARD_SURF[color][value-1],self.PLAYER1_HAND_RECT[i])

    def draw_p2_hand(self):
        for i in range(8):
            self.screen.blit(self.CARDBACK_SURF,self.PLAYER2_HAND_RECT[i])

    def draw_board(self, values):
        for j, (c_card_surf, c_board_rect) in enumerate(zip(list(self.COLOR_CARD_SURF.values()), list(self.COLOR_BOARD_RECT.values()))):
            if values[j] > 0:
                self.screen.blit(c_card_surf[values[j]-1],(c_board_rect.left+5,c_board_rect.top+10))

    def draw_deck(self, deck_length):
        self.screen.blit(self.CARDBACK_SURF,self.DECK_RECT)
        text = self.font.render(str(deck_length), True, "white")
        textRect = text.get_rect()
        textRect.center = self.DECK_RECT.center
        self.screen.blit(text, textRect)

    def draw_game(self, game):
        p2_piles = game.create_2d_array_of_piles("p2")
        board_values = [game.piles["board"][pile].pile[-1].value if not game.piles["board"][pile].is_empty() else 0 for pile in game.piles["board"]]
        p1_piles = game.create_2d_array_of_piles("p1")
        p1_hand_values = [card.value for card in game.p1.hand]
        p1_hand_colors = [card.color for card in game.p1.hand]

        self.draw_p2_hand()
        self.draw_p_piles(p2_piles, "p2")
        self.draw_board(board_values)
        self.draw_deck(len(game.deck))
        self.draw_p_piles(p1_piles, "p1")
        self.draw_p1_hand(p1_hand_values, p1_hand_colors)
        if not game.deck:
            self.game_over(game)

    def get_clicked_card(self, mouse_pos, game, card_to_play):
        if not game.p1.is_draw_phase:
            for i, p1_hand_rect in enumerate(self.PLAYER1_HAND_RECT):
                if p1_hand_rect.collidepoint(mouse_pos):
                    return game.p1.hand[i], None
            if card_to_play is not None:
                for i, p1_piles_rect in enumerate(self.PLAYER1_PILES_RECT):
                    if p1_piles_rect.collidepoint(mouse_pos):
                        return card_to_play, list(game.piles["p1"].values())[i]
                for j, c_board_rect in enumerate(list(self.COLOR_BOARD_RECT.values())):
                    if c_board_rect.collidepoint(mouse_pos):
                        return card_to_play, list(game.piles["board"].values())[j]
        else:
            for j, c_board_rect in enumerate(list(self.COLOR_BOARD_RECT.values())):
                if c_board_rect.collidepoint(mouse_pos):
                    return card_to_play, list(game.piles["board"].values())[j]
            if self.DECK_RECT.collidepoint(mouse_pos):
                return card_to_play, "deck"
        return card_to_play, None

    def game_over(self, game):
        p1_score = game.p1.calculate_score(game.piles["p1"].values())
        p2_score = game.p2.calculate_score(game.piles["p2"].values())
        message = ""
        if p1_score > p2_score:
            message = "YOU WIN!"
        elif p1_score < p2_score:
            message = "P2 WINS"
        else:
            message = "TIE"
        p1_text = self.font.render(str(p1_score), True, "white")
        p2_text = self.font.render(str(p2_score), True, "white")
        message_text = self.font.render(message, True, "white")
        p1_text_rect = p1_text.get_rect()
        p2_text_rect = p2_text.get_rect()
        message_rect = message_text.get_rect()
        p1_text_rect.center = self.PLAYER1_PILES_RECT[2].center
        p2_text_rect.center = self.PLAYER2_PILES_RECT[2].center
        message_rect.center = self.BOARD_RECT.center
        self.screen.blit(p1_text, p1_text_rect)
        self.screen.blit(p2_text, p2_text_rect)
        self.screen.blit(message_text, message_rect)
