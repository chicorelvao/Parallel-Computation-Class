# Simulation of NIM game with one heap of maxpos peaces
# Rule: at each position, take 1, 2 or 3 pieces.
# Winner: the player that takes the last piece.
#
# https://en.wikipedia.org/wiki/Nim
#
# Machine learning:
#   Play nr_games times against yourself and collect
#   statistics for winning and loosing positions,
#   in order to obtain best move for any position.
#

"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #9.2 06-12-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

import json, sys
import numpy as np


# if present, use arguments in call: python nim.py {maxpos} {nr_games} 
if len(sys.argv) > 1:
  maxpos   = sys.argv[1]
  nr_games = sys.argv[2]
else:
  maxpos   = input('Number of inicial peaces: ')
  nr_games = input('Number of games to play: ')
maxpos   = int(maxpos)
nr_games = int(nr_games)


"""
    Chapter 1 - Functions
    ------------------------------------------------------------
"""
# This function randomizes the move to be picked, when the Stats
# are all the same for a board state (position) and moves.

def randomMove(dictMoves):
  allDif = True

  bestMove = 1

  for key in dictMoves:
    for keyCheck in dictMoves:
      if key != keyCheck:
        if dictMoves[key] == dictMoves[keyCheck]:
          allDif = False
          break
    
    if not allDif:
      break


  if allDif:
    bestMove = max(dictMoves, key=dictMoves.get)
  else:
    bestMove = np.random.randint(1, len(dictMoves) + 1)

  return bestMove

  
# Since it's necessary to check until what position the algortithm
# already found the winning strategy, this functions does exactly that
# but the winning strategy has to be known before hand.
# This function doesn't find the winning strategy
def checkWinningStrat(bestMoves):
  
  winningStrat = [1, 2, 3, "-"]

  counterStrat = 0
  highestPos = 0

  counter = 0
  for move in bestMoves:

    if counterStrat > 3:
      counterStrat = 0

    if move != winningStrat[counterStrat]:
      highestPos = counter
      break

    counterStrat += 1      
    counter += 1

    if counter == len(bestMoves):
      highestPos = counter 

  return highestPos



"""
    Chapter 2 - Main Procedure
    ------------------------------------------------------------
"""
# Stat:
# two-dimensional dictionary holding the statistical analysis of each move
# Stat[position][move], initialized with 0
Stat={}
for i in range(1,maxpos+1):
  Stat[i] = {}
  for j in range(1,min(i,3)+1):
    Stat[i][j] = 0

for g in range(nr_games):
  # moves[player][pos]:
  #   for player 1 and 2:
  #     for each position this player went through:
  #        number of peaces taken at position
  moves = {}
  moves[1] = {}
  moves[2] = {}
  # start position, player 1 is starting
  pos = maxpos
  player = 0
  # perform one game:
  while pos:
    # switch to other player
    player = 2 if player == 1 else 1

    # get best move for this position so far:
    #   key of highest value in Stat[pos])
    move = randomMove(Stat[pos]) #max(Stat[pos], key=Stat[pos].get)
    moves[player][pos] = move
    pos -= move

  # last player wins, collect statistics:  
  for pos in moves[player]:
    Stat[pos][moves[player][pos]]+= 1
  # switch to other player that lost:
  player = 2 if player == 1 else 1
  for pos in moves[player]:
    Stat[pos][moves[player][pos]] -= 1





# For each simulated game:
# - gains one point if move at position ended in winning the game
# - looses one point if move at position ended in loosing the game

winningStratArrChreck = []


# Detect best move for all positions and print statistics:
for i in range(maxpos, 0, -1):
  # get best move (key of highest value in Stat[i])
  best = max(Stat[i], key=Stat[i].get)
  v = Stat[i][best]
  if v<0:
    best = '-'
    v = ''

  
  print ("%3d: %s %5s     %s" % (i, str(best), str(v), str(Stat[i])))
  
  winningStratArrChreck.append(best)

winningStratArrChreck.reverse()

highestPos = checkWinningStrat(winningStratArrChreck)

    
print(f"Position Up Until Winning Strategy is found: \n {highestPos}")



# Save Stat in json file:
f = open('nim.json', 'w')
json.dump(Stat, f, sort_keys=True, indent=4, separators=(',', ': '))
f.close()




"""
    Chapter 2 - Final Comment
    ------------------------------------------------------------

    
    The efficiency of the learning procedure is increased, 
    since, the bias introduced by the older algorithm is removed.

    Running this code, one can see that the position up until the 
    winning strategy is known, is actually lower than the first code.
    Naturally, a random algorithm, is usually less efficient and if
    efficiency is defined as winning position over number of pieces,
    then it's not different in this case.
    
    But from a neural network point of view, even though this game
    is a somewhat kind of learning environment, the rules are clear and 
    bad moves can be found quickly, it's better if the neural network
    is presented with different statistics dictionaries and games, like
    the ones given by this code. 
    This removes other types of biases and overtraining of the same games, 
    having a net increase in the learning process. Providing a quality
    database to a neural network is an art in it self and very important.

    This is actually a very difficult topic to discuss without seeing the setup
    of neural network in question. Blocking neurons, parameters obtained from the database,
    type of gradient descent algorithm to affect the neuron weights, etc...
    All these affect the efficiency of the learning process.

"""

