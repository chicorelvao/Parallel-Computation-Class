import random

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
        
        temparray = [Stat[pos].get(i) for i in range(1,len(Stat[pos])+1)]
        a = max(temparray)
        temparray.remove(max(temparray))
        if a in temparray:
            #print("Ambiguous value at pos ", pos, "randomizing")
            temparray = list(Stat[pos].items())
            temparray= [temparray[i][0] for i in range(len(Stat[pos]))]
            if len(Stat[pos]) != 1:    
                temparray.remove(min(Stat[pos], key=Stat[pos].get))
            move = random.choice(temparray)
            moves[player][pos] = move
            pos -= move
            
        else:
            move = max(Stat[pos], key=Stat[pos].get)
            moves[player][pos] = move
            pos -= move
        
        step += 1
        
      for pos in moves[player]:
        Stat[pos][moves[player][pos]]+= 1
      player = 2 if player == 1 else 1
      for pos in moves[player]:
        Stat[pos][moves[player][pos]] -= 1


    for i in range(maxpos, 0, -1):
      best = max(Stat[i], key=Stat[i].get)
      v = Stat[i][best]
      if v<0:
        best = '-'
        v = ''
      print (f"{i:>3}: {best} {v:>5}    {Stat[i]}")
      
    print ("Total number of steps:",step)
      
#      return Stat

#NIM(20,100)
#NIM(1000,10)
NIM()
