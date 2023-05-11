# Blackjack
Blackjack game with both manual and AI play options. AI player implemented with 3 different reinforcement learning algorithms: Monte Carlo policy evaluation, temporal difference policy evaluation and Q-learning.

## Files
**main.py**: Blackjack Game UI  
**game.py**: Game engine  
**ai.py**: AI simulator  
**test.py**: Automated testing suites  
**test_state_1, test_state_2, test_state_3, test_convergence**: test cases  

## Usage
To run the program:  
```
python main.py
```

To run deterministic tester for MC algorithm:
```
python main.py -t 1 -a 1
```

To run convergence tester for all algorithms:
```
python main.py -t 2
```

## in-game keyboard options
* 'h': hit
* 's': stand
* 'm': toggle MC learning
* 't': toggle TD learning
* 'q': toggle Q-learning
* 'a': toggle autoplay
* '1': save the AI state (not the game state)
* '2': load from saved AI state

## Game Rules
**Goal of the player**: Get a bigger sum than the dealer’s sum, without going over 21 (bust). 

### Cards’ values:
- Ace counts as either 1 or 11 based on need. 
- Jack, Queen and King counts as 10. 
- Other cards count as their numerical values.

### Terms:
- Bust: the sum of cards is greater than 21.

### Game’s procedure: 
1. The player and dealer are both given two cards, with one of the dealer’s card revealed to the player. 
2. The player can keep asking for new cards before going bust. 
3. When the player stands, the dealer takes over until termination. 

### Player’s actions: 
1. Hit: player takes a card from card deck
2. Stand: player stops taking cards, and dealer plays with its policy (see below)

### Dealer’s policy:
1. Dealer starts taking cards until the sum get greater than or equal to 17, or greater than or equal to the player’s sum
2. If dealer has A’s in its hand, then the A only counts as 1 when otherwise the dealer bursts. See below for examples
    1. If dealer has {“Ace”, 6}. then the ace counts as 11 and dealer stops taking cards since the sum equals 17.
    2. If dealer has {8, 6, “Ace”}, then the ace counts as 1 (since counting A as 11 would make the dealer burst), and dealer keeps taking cards since the sum equals 15.

### Termination conditions:
1. Player stands
2. Player gets over 21 (bust)
3. Player gets exactly 21

### Game results:
1. If player and dealer has the same sum values, the player LOSES
2. If player busts, player LOSES
3. If dealer busts, player WINS
4. If neither busts, the player WINS if player has a sum bigger than dealer. That means if player and dealer has the same sum value, player LOSES

### Custom rules:
1. Cards are drawn with replacement, so assume that you are playing with infinitely many decks of cards and the drawn cards do not affect the probability of the next cards. 
2. When user has 5 cards without busting, it is NOT considered as WIN in our game engine. 
3. We don’t have DRAW state. If after stand, user and dealer has the same sum values, the player LOSEs.
4. If player gets 21 at the first hand, player WINs if dealer doesn’t have 21; otherwise player LOSEs. 
5. If player gets 21 after a hit, the player automatically stands, meaning dealer starts to play, and check results afterwards.
6. We don’t differentiate between Blackjack (A + 10) and 21, meaning if user and player both has a sum of 21 when the scores are checked, the player is considered as LOSE.
