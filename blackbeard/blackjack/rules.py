import pandas as pd


### 1,2,4+ Deck Basic Strategy

# 1 = hit, 2 = stand, 3 = double, 4 = split
# basic_strat df - basic blackjack for 1,2,4+ decks


# data
hard_4 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 5, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 6, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 7, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 8, 4],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1, "hard", 9, 4],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "hard", 10, 4],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, "hard", 11, 4],
    [1, 1, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 12, 4],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 13, 4],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 14, 4],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 15, 4],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 16, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 17, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 18, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 19, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 20, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 21, 4],
]

soft_4 = [
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1, "soft", 13, 4],
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1, "soft", 14, 4],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 15, 4],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 16, 4],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 17, 4],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, "soft", 18, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 19, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 20, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 21, 4],
]

pair_4 = [
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 4, 4],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 6, 4],
    [1, 1, 1, 4, 4, 1, 1, 1, 1, 1, "pair", 8, 4],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "pair", 10, 4],
    [4, 4, 4, 4, 4, 1, 1, 1, 1, 1, "pair", 12, 4],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 14, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 16, 4],
    [4, 4, 4, 4, 4, 4, 2, 4, 2, 2, "pair", 18, 4],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "pair", 20, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 12, 4],
]

hard_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 5, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 6, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 7, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 8, 2],
    [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, "hard", 9, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "hard", 10, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, "hard", 11, 2],
    [1, 1, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 12, 2],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 13, 2],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 14, 2],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 15, 2],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 16, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 17, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 18, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 19, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 20, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 21, 2],
]

soft_2 = [
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1, "soft", 13, 2],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 14, 2],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 15, 2],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 16, 2],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 17, 2],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, "soft", 18, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 19, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 20, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 21, 2],
]

pair_2 = [
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 4, 2],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 6, 2],
    [1, 1, 1, 4, 4, 1, 1, 1, 1, 1, "pair", 8, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "pair", 10, 2],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 12, 2],
    [4, 4, 4, 4, 4, 4, 4, 1, 1, 1, "pair", 14, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 16, 2],
    [4, 4, 4, 4, 4, 2, 4, 4, 2, 2, "pair", 18, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "pair", 20, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 12, 2],
]

hard_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 6, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "hard", 7, 1],
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1, "hard", 8, 1],
    [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, "hard", 9, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "hard", 10, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, "hard", 11, 1],
    [1, 1, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 12, 1],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 13, 1],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 14, 1],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 15, 1],
    [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, "hard", 16, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 17, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 18, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 19, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 20, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "hard", 21, 1],
]

soft_1 = [
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 13, 1],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 14, 1],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 15, 1],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 16, 1],
    [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, "soft", 17, 1],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, "soft", 18, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 19, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 20, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "soft", 21, 1],
]

pair_1 = [
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 4, 1],
    [4, 4, 4, 4, 4, 4, 4, 1, 1, 1, "pair", 6, 1],
    [1, 1, 4, 4, 4, 1, 1, 1, 1, 1, "pair", 8, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, "pair", 10, 1],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, "pair", 12, 1],
    [4, 4, 4, 4, 4, 4, 4, 1, 2, 1, "pair", 14, 1],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 16, 1],
    [4, 4, 4, 4, 4, 2, 4, 4, 2, 4, "pair", 18, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "pair", 20, 1],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "pair", 12, 1],
]


# construct blackjack df
rules = [hard_4, soft_4, pair_4, hard_2, soft_2, pair_2, hard_1, soft_1, pair_1]
cols = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1, "type", "sum", "deck"]
basic_strat = pd.DataFrame(columns=cols)

for rule in rules:
    temp_rule = pd.DataFrame(rule, columns=cols)
    basic_strat = pd.concat([basic_strat, temp_rule], ignore_index=True)


# raw value: [num, count]
cards = {
    "AS": [1, 1],
    "AH": [1, 1],
    "AD": [1, 1],
    "AC": [1, 1],
    "2S": [2, 1],
    "2H": [2, 1],
    "2D": [2, 1],
    "2C": [2, 1],
    "3S": [3, 1],
    "3H": [3, 1],
    "3D": [3, 1],
    "3C": [3, 1],
    "4S": [4, 1],
    "4H": [4, 1],
    "4D": [4, 1],
    "4C": [4, 1],
    "5S": [5, 1],
    "5H": [5, 1],
    "5D": [5, 1],
    "5C": [5, 1],
    "6S": [6, 1],
    "6H": [6, 1],
    "6D": [6, 1],
    "6C": [6, 1],
    "7S": [7, 1],
    "7H": [7, 1],
    "7D": [7, 1],
    "7C": [7, 1],
    "8S": [8, 1],
    "8H": [8, 1],
    "8D": [8, 1],
    "8C": [8, 1],
    "9S": [9, 1],
    "9H": [9, 1],
    "9D": [9, 1],
    "9C": [9, 1],
    "10S": [10, 1],
    "10H": [10, 1],
    "10D": [10, 1],
    "10C": [10, 1],
    "JS": [10, 1],
    "JH": [10, 1],
    "JD": [10, 1],
    "JC": [10, 1],
    "QS": [10, 1],
    "QH": [10, 1],
    "QD": [10, 1],
    "QC": [10, 1],
    "KS": [10, 1],
    "KH": [10, 1],
    "KD": [10, 1],
    "KC": [10, 1],
}


# debug
# df_test = basic_strat.groupby("deck")
# print(df_test.get_group(2))
