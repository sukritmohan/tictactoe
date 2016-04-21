# Tic Tac Toe Game

To play:
---------

### 1 player game::
    python TicTacToeGame.py
        --sarsa : to play against a SARSA bot
        --qlearning : to play against a Q-Learning bot (default)
        --policy_file <filepath> : to pass your own model file to read and persist state. Defaults to
                                                    previously saved bot if argument isn't passed

### 2 player game::
    python TicTacToeGame.py --2p

### Training mode::
    python TicTacToeGame.py --2p --sarsa --policy_file <loc>
        (to train SARSA bot and save to location <loc>)

To see changing Q-values after every episode, please uncomment lines 37,70,71 of QLearningPolicy.py
and lines 25,54,55 of SARSAPolicy.py and play game using command:

    python TicTacToeGame.py --qlearning --policy_file ./test_ql.dmp
        or
    python TicTacToeGame.py --sarsa --policy_file ./test_sarsa.dmp


On extended simulations, SARSA bot wins about 5 times as many games as a random bot, whereas QLearningBot wins about 6-7 times as 
many games as a random bot.

    python TicTacToeGame.py --sarsa --training


SARSA episode/reward : ./models/sarsa_training.png

Q-Learning episode/reward : ./models/qlearning_training.png

Haven't done too much tweaking of learning rate and discount rate to optimize model. Tuning these parameters
will likely result in a better trained player. Learning rate would also benefit from some sort of simulated
annealing treatment as the model starts to learn and get better.

TODO:
--------------------
* [DONE] Unit tests for TicTacToe [tictactoe/TicTacToe_Tests.py]
* Unit tests for QPolicy
* [DONE] During training mode, both player-bots can simultaneously update the same QPolicy, since for a given gameplay both players
  see distinct states (mirror opposites of one another), so these states can be updated in parallel.
  We could initialize one QLearningPolicy and pass it to 2 RLBotPlayers, so that they can simultaneously update the Q-values
  based on what they've learnt. We know that in any given game, both players will see completely distinct game
  states (no overlap of states), so we can update Q-values from both Agents every game, without any risk of state collisions
  [sarsamodel_agent_v_agent.dmp was trained using the same sarsa model playing as both players]
* Games can be run parallelly, but Q-value policy needs to be shared between the threads.

