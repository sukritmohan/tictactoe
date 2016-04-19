# Tic Tac Toe Game

To run: python TicTacToeGame.py

Future Improvements:
* During training mode, both player-bots can simultaneously update the same QPolicy, since for a given gameplay both players
  see distinct states (mirror opposites of one another), so these states can be updated in parallel.
  We could initialize one QLearningPolicy and pass it to 2 RLBotPlayers, so that they can simultaneously update the Q-values
  based on what they've learnt. We know that in any given game, both players will see completely distinct game
  states (no overlap of states), so we can update Q-values from both Agents every game, without any risk of state collisions