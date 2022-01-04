#  ╓──────────────────────────────────────────────────────────────────────╖
#  ║  File name: divide.py                                                ║ 
#  ║  Author: David De Potter, pl3onasm@gmail.com                         ║
#  ║  License: refer to the license file in this repository               ║
#  ║  Description: implementation of a divide and conquer strategy for    ║
#  ║               reducing the original problem to a puzzle of 2x3       ║
#  ╙──────────────────────────────────────────────────────────────────────╜

from astar import *

  ## <<::::::::::::::::::::::::: Divide & Conquer :::::::::::::::::::::::::>> ## 

def placeTile (puzzle, solValue, goal, solutionPath):
  '''places a tile with given solValue on the desired goal spot of the puzzle'''

  def getBestNeighbour (puzzle, tile,goal):
    # best neighbour is the adjacent tile with the shortest distance to the goal
    neighbours = []
    for _,r,c in puzzle.getTileSteps(tile):
      dist = puzzle.getTileDistance((r,c),goal)
      neighbours += [(dist,(r,c))]
    neighbours.sort(key=lambda x:x[0])
    return neighbours[0][1]

  while (puzzle.getTileValue(goal) != solValue):
    #get present location of the solution value in the board
    tile = puzzle.getTileCoords(solValue)
    #find the adjacent location to tile with the shortest distance to the goal
    neighbour = getBestNeighbour(puzzle, tile, goal)
    #find present location of the blank square in the board
    blank = puzzle.getTileCoords(0)
    #find shortest path to get the blank square to the tile's best neighbour
    path = AStarTile(puzzle, blank, neighbour, solValue)
    
    for (_,(a,b)),(step,(c,d)) in zip(path,path[1:]):
      #repeatedly swaps the blank square with adjacent tile along the found path
      puzzle.swap(a,b,c,d)
      solutionPath += [(step,puzzle.board[a][b],puzzle.draw())]
     
    # processes final swap of the blank square with the tile that needs to be
    # moved towards the goal one step at the time
    _, (a,b) = path[-1]
    (c,d) = puzzle.getTileCoords(solValue)
    puzzle.swap(a,b,c,d)
    solutionPath += [(puzzle.getStep(a,b,c,d),puzzle.board[a][b],puzzle.draw())]
  
  puzzle.deactivate(*goal)
  return
    
def solveRowCol (puzzle, w, btype, solution, idx, spots, solutionPath):
  '''solves the top row or the left most column'''
  (px,py),(cx, cy),(ax,ay),(tx,ty) = spots   
  # px, py are coords of the penultimate spot in top row or left column
  # cx, cy are coords of the relevant corner
  # ax, ay are coords of the corner's neigbour below or to the right
  # tx, ty are coords of a temporary spot with minimal cost

  # solve the row or column except for the last two tiles
  for j in range(idx,w-2):
    value = solution[j]
    coord = (idx, j) if btype == 'r' else (j,idx)
    placeTile(puzzle, value, coord, solutionPath)
  
  board = puzzle.getBoard()
  if not (solution[-2] == board[px][py] and solution[-1] == board[cx][cy]):
    # move the tile with the last solution value to a temporary location
    placeTile(puzzle, solution[-1], (tx, ty), solutionPath)
    puzzle.activate(tx,ty)

    # move the tile with the penultimate solution value to the 
    # the top right or bottom left corner
    placeTile(puzzle, solution[-2], (cx, cy), solutionPath)

    # place the tile with the last solution value next to the penultimate one
    puzzle.activate(tx,ty)
    placeTile(puzzle, solution[-1], (ax, ay), solutionPath)

    # activate the corner tile and rotate it into its final position
    puzzle.activate(cx,cy)
    placeTile(puzzle, solution[-2], (px, py), solutionPath)
    
    # activate the adjacent tile and rotate it into its final position
    puzzle.activate(ax,ay)
    placeTile(puzzle, solution[-1], (cx, cy), solutionPath)

  puzzle.deactivate(cx,cy); puzzle.deactivate(px,py)
  return    

def reduceTo2x3 (puzzle, w, solutionPath):
  '''reduces the problem to a 2x3 puzzle by repeatedly solving the 
     top row and left most column'''
  
  rsolution = puzzle.getSolution('r')
  csolution = puzzle.getSolution('c')
  for i in range(w-3):
    spots = [(i,-2),(i,w-1),(i+1,w-1),(i+2,w-2)]  
    solveRowCol (puzzle, w, 'r', rsolution[i], i, spots, solutionPath) 
    spots = [(-2,i),(w-1,i),(w-1,i+1),(w-2,i+2)]  
    solveRowCol (puzzle, w, 'c', csolution[i], i, spots, solutionPath)

  spots = [(w-3,-2),(w-3,w-1),(w-2,w-1),(w-1,w-1)]  
  solveRowCol (puzzle, w, 'r', rsolution[w-3], w-3, spots, solutionPath) 
  return 