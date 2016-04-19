# Tic Tac Toe Game

To play:
---------

1 player game:: python TicTacToeGame.py
                        --sarsa : to play against a SARSA bot
                        --qlearning : to play against a Q-Learning bot
                        --policy_file <filepath> : to pass your own model file to read and persist state. Defaults to
                                                    previously saved bot if argument isn't passed

2 player game:: python TicTacToeGame.py --2p

Training mode:: python TicTacToeGame.py --2p --sarsa --policy_file <loc>
                            (to train SARSA bot and save to location <loc>)




Future Improvements:
* [DONE] During training mode, both player-bots can simultaneously update the same QPolicy, since for a given gameplay both players
  see distinct states (mirror opposites of one another), so these states can be updated in parallel.
  We could initialize one QLearningPolicy and pass it to 2 RLBotPlayers, so that they can simultaneously update the Q-values
  based on what they've learnt. We know that in any given game, both players will see completely distinct game
  states (no overlap of states), so we can update Q-values from both Agents every game, without any risk of state collisions



TODO:
* Unit Tests