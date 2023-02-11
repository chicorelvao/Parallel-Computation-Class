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
    Exercise Sheet #9.3 06-12-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

import sys 
import numpy as np


"""
    Chapter 1 - Functions
    ------------------------------------------------------------
"""

# To build the Stat dictionary, it's necessary for create the keys,
# which represent a state of the game and the values which represent
# moves, found by a winning strategy.

# This functions builds the moves associated to a key, or a game state
def movesBuilder(row0,row1,row2, row3):
    outDict = {}
    pos = [row0, row1, row2, row3]

    for i in range(0,4):
        for j in range(1, pos[i] + 1):
            outDict[i,j] = 0

    return outDict


# This functions randomizes the move to be picked, when the Stats
# are all the same for a board state (position) and moves.
def randomMove(dictMoves):
  allDif = True

  bestMove = (0, 1)

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
    bestMove = np.random.randint(0, len(dictMoves))
    bestMove = list(dictMoves.keys())[bestMove]

  return bestMove


"""
    Chapter 2 - Initializions and Allocations
    ------------------------------------------------------------
"""

# The strategy of this program or algorithm is the same as the professor provived
# Only now, there is a fixed set of pieces and colummns.

if len(sys.argv) > 1:
  nr_games = sys.argv[1]
else:

  nr_games = input('Number of games to play: ')
nr_games = int(nr_games)


# The Stat dictionary, very similar to the given example code
Stat = {}
for row0 in range(0,2):
    for row1 in range(0,4):
        for row2 in range(0,6):
            for row3 in range(0,8):
                Stat[row0, row1, row2, row3] = movesBuilder(row0, row1, row2, row3)




"""
    Chapter 3 - Main Procedure
    ------------------------------------------------------------
"""
for g in range(nr_games):

  moves = {}
  moves[1] = {}
  moves[2] = {}
  
  # This array represent the initial game state
  pos = [1, 3, 5, 7]
  player = 0 


  # Game Cycle
  while sum(pos):

    # Switch players
    if player == 1:
        player = 2
    else:
        player = 1

    
    posTuple = tuple(pos) 
    # Movements and Positions are now tuples so that access 
    # to the Stat dict is possible.
    move = randomMove(Stat[posTuple])

    
    moves[player][posTuple] = move
    pos[move[0]] -= move[1]



  # last player wins, collect statistics:
  for pos in moves[player]:
    posTuple = tuple(pos)
    Stat[posTuple][moves[player][posTuple]] += 1


  # switch to other player that lost:
  player = 2 if player == 1 else 1

  for pos in moves[player]:
    posTuple = tuple(pos)
    Stat[posTuple][moves[player][posTuple]] -= 1


# Detect best move for all positions and print statistics:
# (Pretty much the same)

for row0 in range(1,-1,-1): 
    for row1 in range(3,-1,-1):
        for row2 in range(5,-1,-1):
            for row3 in range(7,-1,-1):
                if (row0, row1, row2, row3) != (0,0,0,0):
                    pos = (row0, row1, row2, row3)
                
                best = max(Stat[pos], key=Stat[pos].get)
                v = Stat[pos][best]

                if v<0:
                    best = '-'
                    v = ''

                print ("%s: %s %5s" % (pos, str(best), str(v)))


"""
    Chapter 4 - Final Comment
    ------------------------------------------------------------

    As it's possible to see from this program output, it's not 
    possible to find a winning strategy, per say. 
    It's definitely possible to find moves that are associated 
    with moves that eventually lead to a game win, since this
    are the moves with the highest frequencies.

    Maybe the neural network can exploit these high frequency
    moves to find possible winning strategies.
"""

