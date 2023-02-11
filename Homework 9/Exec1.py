def NIM(maxpos=0,nr_games=0):
    if maxpos == 0 and nr_games == 0:
        maxpos   = int(input('Number of inicial peaces: '))
        nr_games = int(input('Number of games to play: ')) 
        
    Stat={}
    for i in range(1,maxpos+1):
      Stat[i] = {}
      for j in range(1,min(i,3)+1):
        Stat[i][j] = 0
    step = 0
    
    for g in range(nr_games):
      
      moves = {}
      moves[1] = {}
      moves[2] = {}
    
      pos = maxpos
      player = 0
    
      while pos:
    
        player = 2 if player == 1 else 1
    
        move = max(Stat[pos], key=Stat[pos].get)
        moves[player][pos] = move
        pos -= move
        
        step += 1
    
      for pos in moves[player]:
        Stat[pos][moves[player][pos]]+= 1
      player = 2 if player == 1 else 1
      for pos in moves[player]:
        Stat[pos][moves[player][pos]] -= 1
    
        
    Sequence = []
    for i in range(maxpos, 0, -1):
      best = max(Stat[i], key=Stat[i].get)
      v = Stat[i][best]
      if v<0:
        best = '-'
        v = ''
      Sequence.append(best)  
      print (f"{i:>3}: {best} {v:>5}    {Stat[i]}")

    Sequence.reverse()
    BestSeq = [0 for i in range(maxpos)]
    for i in range(0,maxpos,4):
       try:
           BestSeq[i] = 1
           BestSeq[i+1] = 2
           BestSeq[i+2] = 3
           BestSeq[i+3] = '-'
       except IndexError:
           continue
    
    for i in range(maxpos):
        if BestSeq[i] != Sequence[i]:
            print("Last predicted move is", BestSeq[i], "at position,", i)
            break
        else:
            print("Up until position", i+1, "We are good")
            continue
    print ("Total number of steps:",step)
    return None

#NIM(20,100)
#NIM(1000,10)
#NIM(1000,100)
#NIM(1000,1000)
#NIM(1000,10000)
NIM()
