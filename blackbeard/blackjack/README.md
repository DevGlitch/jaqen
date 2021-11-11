# Blackjack Strategy and Strategy

Key Classes & methods:
- Game
  - update(): everytime seeing a new card
  - bet_size(): every new round
- Hand
  - action(): determines hit/stand based on current cards

How to use:
1. Instantiate Game Class every shuffle/reset
2. Instantiate Hand Class & Game.bet_size() every round
3. update Game instance for every card seen
4. update Hand instance based on action
5. Hand.action() for best action
