import pygame
from sys import exit
from game import Game
from gui import Gui

game = Game()
gui = Gui()
is_human_player = False
card_to_play = None
pile_to_play = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            card_to_play, pile_to_play = gui.get_clicked_card(event.pos, game, card_to_play)

    if game.deck:
        if game.is_p1_turn:
            if is_human_player:
                card_to_play, pile_to_play = gui.human_player_turn(game, card_to_play, pile_to_play)
            else:
                game.player_turn(game.p1)
        else:
            game.player_turn(game.p2)
            
    gui.screen.blit(gui.BOARD_SURF,gui.BOARD_RECT)
    gui.draw_game(game)

    pygame.display.update()
    gui.clock.tick(60)
