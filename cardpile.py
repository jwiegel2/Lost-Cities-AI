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
