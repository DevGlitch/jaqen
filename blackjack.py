import pandas as pd
import numpy as np

# Rules
# dealer hits soft 17
# double after split allowed
# no surrender
# no insurance


# initialize
decks_n = 2
bankroll = 2500


class Game:
    def __init__(self, decks_n):
        self.decks_n = decks_n
        self.count = 0
        self.min_bet = 10

    def update(self, card):
        if 2 <= card <= 6:
            self.count -= 1
        elif card >= 10:
            self.count += 1

    def bet_size(self):
        if self.count <= 0:
            return self.min_bet
        return self.min_bet*(self.count+1)


# debug
game1 = Game(2)
game1.update(10)
game1.update(10)
bet = game1.bet_size()
print(bet)