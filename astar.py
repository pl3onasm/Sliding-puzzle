#  ╓────────────────────────────────────────────────────────────────────────────╖
#  ║  File name: astar.py                                                       ║ 
#  ║  Author: David De Potter, pl3onasm@gmail.com                               ║
#  ║  License: refer to the license file in this repository                     ║
#  ║  Description: implementation of A* algorithms                              ║
#  ║  - AStarTile is used to compute the shortest path from the blank           ║
#  ║  square to a given tile's neighbour (adjacent tile)                        ║
#  ║  - AStar computes the shortest node path for a 2x3 puzzle, where each      ║
#  ║  node contains a new puzzle that is one swap further away from its parent  ║
#  ╙────────────────────────────────────────────────────────────────────────────╜

from queue import PriorityQueue

  ## <<:::::::::::::::::::::::: A* Tile Path Search ::::::::::::::::::::::::>> ##

def AStarTile (puzzle, blank, destination, tileValue) :
    '''A* algorithm to find shortest path of blank square to destination'''
    #takes the blank square to destination which is right next to tileValue
    #a dictionary is used for explored so as to keep track of previous steps
    #the tileValue is kept fixed while searching for the shortest path
    frontier, tilePath = PriorityQueue(), []
    frontier.put((0,blank))                     #blank is a tuple
    explored = {blank: (("blank",blank),None)}  

    while not frontier.empty():
      _, curTile = frontier.get()  
      if curTile == destination: 
        while curTile in explored:
          tilePath.insert(0,explored[curTile][0])
          curTile = explored[curTile][1]
        return tilePath

      for step, x, y in puzzle.getTileSteps(curTile):
        nextTile = (x,y)   
        if nextTile not in explored and puzzle.getTileValue(nextTile) != tileValue\
        and puzzle.isActive(x,y):
          frontier.put((puzzle.getTileDistance(nextTile,destination),nextTile))
          explored[nextTile] = ((step,nextTile), curTile)
    
    return
    
  ## <<:::::::::::::::::::::::: A* Node Path Search ::::::::::::::::::::::::>> ##

def AStar (root) :
  '''A* algorithm to find shortest node path in the remaining 2x3 puzzle'''
  #a dictionary is used for explored so as to keep track of the parent nodes
  frontier,g = PriorityQueue(),0
  frontier.put((0,str(root),root))
  explored = {str(root): (('','',''),None)}

  while not frontier.empty():
    _, _, curPuzzle = frontier.get()         
    if curPuzzle.solved():  
      path = []                        
      while str(curPuzzle) in explored:  
        path.insert(0,explored[str(curPuzzle)][0])
        curPuzzle = explored[str(curPuzzle)][1]
      return path

    g += 1  # the next generated nodes are one step further away from the root
    for step,tileValue,newPuzzle in curPuzzle.getNeighbours():
      if str(newPuzzle) not in explored:
        frontier.put((g+newPuzzle.h(),str(newPuzzle),newPuzzle))
        explored[str(newPuzzle)] = ((step,tileValue,newPuzzle.draw()), curPuzzle)

  return 
