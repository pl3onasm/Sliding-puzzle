#  ┌────────────────────────────────────────────────────────────┐
#  |  File name: puzzle.py                                      | 
#  |  Author: David De Potter, pl3onasm@gmail.com               |
#  |  License: refer to the license file in this repository     |
#  |  Description: implementation of the puzzle class           |
#  └────────────────────────────────────────────────────────────┘

import copy

  ## <<:::::::::::::::::::::::::::: Puzzle Class ::::::::::::::::::::::::::::>> ##  
  
class Puzzle:

  def __init__ (self, board, active=None):
    self.board = board
    self.width = len(board[0])
    g = [d for d in range(1,self.width**2)]+[0]
    self.goal = [g[i:i+self.width] for i in range(0,len(g),self.width)]
    self.active = active if active else [self.width*[1] for _ in range(self.width)]
                  # tiles can only be moved if active

  def getWidth (self):
    return self.width

  def getSolution (self, stype):
    '''depending on the parameter, the row or column solution is returned'''
    def transpose(grid):
      return [list(x) for x in zip(*grid)]

    if stype == 'c': 
      return transpose(self.goal)
    return self.goal

  def solved (self):
    '''verifies if a puzzle is solved or not'''
    return self.board == self.goal

  def h (self):
    '''heuristic for 2x3 A*-search'''
    return self.hammingDistance() + self.manhattanDistance()
  
  def hammingDistance (self):
    '''computes the hamming distance between two puzzles'''
    hamming = 0
    for i in range(3):
      for j in range(3):
        if self.board[i][j] and self.board[i][j] != self.goal[i][j]:
          hamming += 1
    return hamming

  def manhattanDistance (self):
    '''computes the manhattan or taxi-cab distance between two puzzles'''
    manhattan = 0; copy1D = sum(self.board,[])
    for i,val in enumerate(copy1D):
      if copy1D[i]:
        pos = i//3 + i%3
        goal = val//3 + val%3
        manhattan += abs(pos-goal)
    return manhattan
  
  def getNeighbours (self):
    neighbours, (x,y) = [], self.getTileCoords(0)
    for step,r,c in self.getTileSteps((x,y)):
      newPuzzle = self.getNewBoard(x,y,r,c)
      neighbours += [(step, self.board[r][c], newPuzzle)]
    return neighbours

  def getNewBoard (self, x0, y0, x1, y1):
    '''generates a new puzzle in which the given coordinates have been swapped'''
    newBoard = copy.deepcopy(self.board)
    val = newBoard[x0][y0] 
    newBoard[x0][y0], newBoard[x1][y1] = newBoard[x1][y1], val
    return Puzzle(newBoard,self.active)

  def __str__ (self):
    '''returns a string representation of the puzzle board'''
    return "".join(map(str,sum(self.board,[])))

  def getBoard(self):
    '''returns the board's present state'''
    return self.board

  def draw (self):
    '''ouputs a representation of the puzzle board'''
    output = ""
    w = self.width*5 if self.width < 10 else self.width*6
    for i in range(self.width):
      output += '\t'+'-'*(w+1)+'\n'
      output += '\t'
      for j in range(self.width):
        d = self.board[i][j]
        if self.width <10:
          if d:
            output += "| {0:2d} ".format(d)
          else:
            output += "|    "
        elif self.width >= 10:
          if d:
            output += "| {0:3d} ".format(d)
          else:
            output += "|     "
      output += "|"+'\n'
    output += '\t'+'-'*(w+1)+'\n\n'
    return output

  def swap (self,x1,y1,x2,y2):
    '''executes a tile swap in the puzzle board'''
    val = self.board[x1][y1] 
    self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], val

  def isSolvable (self):
    '''verifies whether a given puzzle is solvable or not'''
    def inversions (arr):
      inversions, l = 0, len(arr)
      for i in range(l):
        for j in range(i + 1, l):
          if (arr[i] > arr[j]):
            inversions += 1
      return inversions      
    
    copy1D = sum(self.board,[])
    copy1D.remove(0)
    if self.width & 1: #odd
      return 0 if (inversions(copy1D) & 1) else 1
    return 1 if ((inversions(copy1D) + self.getTileCoords(0)[0]) & 1) else 0

  ## <<::::::::::::::::::::::: Tile Specific Methods ::::::::::::::::::::::::>> ##

  def getTileCoords (self, value):
    for x in range(self.width):
      for y in range(self.width):
        if self.board[x][y] == value: 
          return x,y
  
  def getTileValue (self, coords):
    (x,y) = coords
    return self.board[x][y]

  def getTileDistance (self, coords1, coords2):
    (x1,y1), (x2,y2) = coords1, coords2
    return abs(x1-x2) + abs(y1-y2)

  def getTileSteps (self, coords):
    '''returns all valid adjactent tiles along with the corresponding step'''
    valid, (x,y) = [], coords
    steps = [("Up \u2B9D",x+1,y), ("Down \u2B9F",x-1, y), 
            ("Left \u2B9C",x,y+1), ("Right \u2B9E",x,y-1)]
    for step,r,c in steps:
      if (0 <= r < self.width and 0 <= c < self.width) \
      and self.isActive(r,c):
        valid += [(step,r,c)]
    return valid

  def deactivate (self, x ,y) :
    '''fixes a tile to its spot, so it cannot be moved anymore'''
    self.active[x][y] = 0

  def activate (self, x, y) :
    '''reactivates a tile, so that it may be moved again'''
    self.active[x][y] = 1

  def isActive (self, x, y):
    '''checks if a tile is active or not'''
    return self.active[x][y]

  def getStep (self, w, x, y , z) :
    '''returns the step between to adjacent tiles'''
    steps = [("Up \u2B9D",1,0), ("Down \u2B9F",-1,0), 
            ("Left \u2B9C",0,1), ("Right \u2B9E",0,-1)]
    for step,r,c in steps:
      if w + r == y and x + c == z:
        return step
