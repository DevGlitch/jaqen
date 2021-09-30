import pandas as pd
import numpy as np
import math


# Rules
# dealer hits soft 17
# double after split allowed
# no surrender
# no insurance


# initialize
decks = 2
bankroll = 500


class Game:
    """
    cards: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    """

    def __init__(self, decks_n):
        self.decks_n = decks_n
        self.count = 0
        self.min_bet = 10

    def update(self, card):
        """
        counting rules

        :param card: int - seen card
        :return: none
        """
        if 2 <= card <= 6:
            self.count -= 1/self.decks_n
        elif card == 10 or card == 1:
            self.count += 1/self.decks_n

    def bet_size(self):
        """
        Determines how much to bet

        :return: int - betting amount
        """
        if self.count < 0:
            return self.min_bet
        return self.min_bet*(math.floor(self.count)+1)


class Hand:
    """
    Class for hand
    """
    def __init__(self, cards):
        """
        :param cards: list - list of cards in hand
        """
        self.hand = cards
        self.htype = self.hand_type()
        self.total = self.hand_sum()
        # self.status = 1

    def hand_type(self):
        """
        determine hand type to apply different rules

        :return: str - "pair" or "soft" or "hard" or "none"
        """
        hand_size = len(self.hand)
        if hand_size <= 1:
            return None

        if hand_size == 2:
            if self.hand[0] == self.hand[1]:
                return "pair"
            else:
                if 1 in self.hand:
                    return "soft"
                else:
                    return "hard"
        elif hand_size > 2:
            if 1 in self.hand:
                if sum(self.hand) > 12:
                    return "hard"
                else:
                    return "soft"
            else:
                return "hard"

    def hand_sum(self):
        """
        calculates max sum of hand

        :return points: int - max sum
        """
        points = sum(self.hand)
        if 1 in self.hand and points + 10 <= 21:
            points += 10
        return points

    def hit(self, card):
        """
        Hit/Double action
        :param card: int - added new card
        :return: None
        """
        self.hand.append(card)
        self.htype = self.hand_type()
        self.total = self.hand_sum()

    def split(self, card):
        """
        Split action
        :param card: int -  added new card
        :return pop: int - split card
        """
        pop = self.hand.pop()
        self.hand.append(card)
        self.htype = self.hand_type()
        self.total = self.hand_sum()
        return pop


# debug Class Game
game1 = Game(2)
game1.update(10)
game1.update(10)
bet = game1.bet_size()
print(bet)

# debug Class Hand
hand1 = Hand([5, 6, 10])
print(hand1.htype)
print(hand1.total)
