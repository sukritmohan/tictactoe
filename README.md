# Tic Tac Toe Game

To play:
---------

### 1 player game::
    python TicTacToeGame.py
        --qlearning : to play against a Q-Learning bot [default]
        --sarsa : to play against a SARSA bot
        --policy_file <filepath> : to pass your own model file to read and persist state. Defaults to
                                                    previously saved bot if argument isn't passed

### 2 player game::
    python TicTacToeGame.py --2p

### Training mode::
    python TicTacToeGame.py --training --sarsa --policy_file <loc>
        (to train SARSA bot and save to location <loc>)

To see changing Q-values after every episode, please uncomment lines 70,83,84 of QLearningPolicy.py 
and play game using command:

    python TicTacToeGame.py --qlearning --policy_file ./test_ql.dmp
        or
    python TicTacToeGame.py --sarsa --policy_file ./test_sarsa.dmp



Reward/episode : ./models/reward_per_episode.png

Haven't done too much tweaking of learning rate and discount rate to optimize model. Tuning these parameters
will likely result in a better trained player. Learning rate could also benefit from some sort of simulated
annealing treatment as the model starts to learn and get better.

TODO:
--------------------
* [DONE] Unit tests for TicTacToe [tictactoe/TicTacToe_Tests.py]
* Unit tests for QPolicy
* During training mode, both player-bots can simultaneously update the same QPolicy, since for a given gameplay both players
  see distinct states (mirror opposites of one another), so these states can be updated in parallel.
  We could initialize one QLearningPolicy and pass it to 2 RLBotPlayers, so that they can simultaneously update the Q-values
  based on what they've learnt. We know that in any given game, both players will see completely distinct game
  states (no overlap of states), so we can update Q-values from both Agents every game, without any risk of state collisions
  [sarsamodel_agent_v_agent.dmp was trained using the same sarsa model playing as both players]
* Games can be run parallelly, but Q-value policy needs to be shared between the threads.
* Could use the other player's moves to update Q-values using the opponent's perspective (count it as exploration ?)

