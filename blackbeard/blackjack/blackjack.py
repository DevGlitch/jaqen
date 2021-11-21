import math
from .rules import basic_strat

# Rules
# dealer hits soft 17
# double after split allowed
# no surrender
# no insurance


# initialize
decks = 1
bankroll = 500


class Hand:
    """
    Class for hand
    """

    def __init__(self):
        """ """
        self.hand = []
        self.dealer = []
        self.htype = self.hand_type()
        self.ptotal = self.hand_sum(player="player")
        self.dtotal = self.hand_sum(player="dealer")
        self.action = -1
        self.opt = self.optAction()

    def hand_type(self):
        """
        determine hand type to apply different rules

        :return: str - "pair" or "soft" or "hard" or "none"
        """
        hand_size = len(self.hand)
        if hand_size <= 1:
            return "none"

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

    def hand_sum(self, player="player"):
        """
        calculates max sum of hand

        :param player: str - player/dealer
        :return points: int - max sum
        """
        if player == "player":
            cur_hand = self.hand
        else:
            cur_hand = self.dealer
        points = sum(cur_hand)
        if 1 in cur_hand and points + 10 <= 21:
            points += 10
        return points

    def add(self, card, player="player"):
        """
        Dealing/Hit/Double action
        :param card: int - added new card
        :param player: str - player/dealer
        :return: None
        """
        # if dealer empty, 1st card goes to dealer
        if not self.dealer:
            player = "dealer"

        if player == "dealer":
            self.dealer.append(card)
            self.dtotal = self.hand_sum(player="dealer")
        else:
            self.hand.append(card)
            self.htype = self.hand_type()
            self.ptotal = self.hand_sum()
            self.action = -1

    # def split(self, card):
    #     """
    #     Split action
    #     :param card: int -  added new card
    #     :return pop: int - split card
    #     """
    #     pop = self.hand.pop()
    #     self.hand.append(card)
    #     self.htype = self.hand_type()
    #     self.ptotal = self.hand_sum()
    #     return pop

    def optAction(self, decks_n=1):
        """
        Optimal action

        :return: str - optimal action
        """
        if self.phase == 1:
            action_space = {1: "Hit", 2: "Stand", 3: "Double", 4: "Split"}
            basic_df = basic_strat.groupby("deck").get_group(decks_n)
            filtered = basic_df[
                (basic_df["sum"] == self.ptotal) & (basic_df["type"] == self.htype)
            ]
            return action_space[filtered[self.dealer[0]].values[0]]
        else:
            return "None"


class Round(Hand):
    """
    Round per hand
    """

    def __init__(self):
        self.new_round()

    def check_bet(self):
        """
        Betting phase + dealing initial cards
        """
        self.n_cards += 1
        if self.n_cards == 3:
            self.phase += 1

    def check_player(self):
        """
        Player's turn
        player actions: {1: "Hit", 2: 'Stand', 3: 'Double', 4: 'Split'}
        """
        if self.action == 1:
            self.add(self.last_seen)
        elif self.action == 2:
            print("stands")
            self.phase += 1
        if self.ptotal > 21:
            self.new_round()

    def check_dealer(self):
        if self.dtotal < 17:
            self.add(self.last_seen, player="dealer")
        if self.dtotal >= 17:
            # win/lose/bust
            self.new_round()

    def new_round(self):
        self.phase = 0  # 0: betting, 1: player, 2: dealer
        self.n_cards = 0
        super().__init__()

    def round_update(self, card):
        if self.phase == 0:
            if card > 0:
                self.add(card, player="player")
                self.check_bet()
        elif self.phase == 1:
            self.check_player()
        elif self.phase == 2:
            self.check_dealer()


class Game(Round):
    """
    Game per deck

    cards: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    """

    def __init__(self, cards, decks_n=1, debug=True):
        """
        new game
        """
        super().__init__()
        self.debug = debug
        self.decks_n = decks_n
        self.cards = cards
        self.reset()

    def counter(self, card):
        """
        counting rules

        :param card: str - seen unique card
        :return: none
        """
        num = self.cards[card][0]
        if 2 <= num <= 6:
            self.count -= 1 / self.decks_n
        elif num == 10 or num == 1:
            self.count += 1 / self.decks_n
        self.last_seen = num

    def game_update(self, card="", gest="None"):
        """
        check for unique cards. Moves blackjack logic along with unique cards
        updates available card list

        :param card: str - detected card
        :param gest: str - hit/stand/reset
        """
        if not card and gest == "None":
            return
        self.gest_assign(gest=gest)
        if card and self.cards[card][1] == 1:
            self.cards[card][1] = 0
            self.counter(card)
        self.round_update(self.last_seen)
        if self.debug:
            self.debug_print()

    def gest_assign(self, gest="None"):
        """
        :param gest: str - None/Hit/Stand/Reset
        """
        gest_key = {"Hit": 1, "Stand": 2, "Split": "3"}
        if gest == "Reset":
            self.reset()
        elif gest == "None":
            pass
        else:
            self.action = gest_key[gest]

    def bet_size(self):
        """
        Determines how much to bet

        :return: int - betting amount
        """
        if self.count < 2:
            return self.min_bet
        return self.min_bet * (math.floor(self.count) - 1)

    def reset(self):
        """
        shuffle/new table
        """
        self.count = 0
        self.min_bet = 10
        self.cards = {k: [v[0], 1] for k, v in self.cards.items()}
        self.last_seen = 0

    def debug_print(self):
        print(f"Game Phase: {self.phase}")
        print(f"Count: {self.count}")
        print(f"Game Last Card: {self.last_seen}")
        print(f"Player Action: {self.action}")
        print(f"Player Hand: {self.hand} | {self.ptotal}")
        print(f"Dealer Hand: {self.dealer} | {self.dtotal}")
