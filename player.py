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
        if card_list:
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
