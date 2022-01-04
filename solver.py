#  ╓──────────────────────────────────────────────────────────────────╖
#  ║  File name: solver.py                                            ║ 
#  ║  Author: David De Potter, pl3onasm@gmail.com                     ║
#  ║  License: refer to the license file in this repository           ║
#  ║  Description: solves a given sliding puzzle by applying a        ║
#  ║  combination of A*-algorithms and a divide and conquer strategy  ║
#  ╙──────────────────────────────────────────────────────────────────╜

import os
import sys  
from puzzle import *
from divide import *
from astar import *
  
def solve (board):
  '''main solver'''

  def prettyPrint (solutionPath):
    # formats the output
    output = ""
    for step,value,puzzle in solutionPath:
      if step == "Initial board":
        output += "\n{}\n\n".format(step) + puzzle
      else:
        output += "Tile {} {}\n\n".format(value, step) + puzzle
    return output

  puzzle = Puzzle(board)
  if not puzzle.isSolvable():
    return "\nThe puzzle is unsolvable.\n"
  
  path1 = [("Initial board","",puzzle.draw())]
  reduceTo2x3(puzzle, len(board[0]), path1)
  path2 = AStar(puzzle)  #solves the remaining 2x3 puzzle 

  if not path1 or not path2:
    return "\nThe puzzle is unsolvable.\n"
  return prettyPrint(path1+path2[1:])

  ## <<::::::::::::::::::::::::::::::: Main :::::::::::::::::::::::::::::::>> ##

def main(inFile):
  with open(inFile, 'r') as f:
    puzzle = [[int(char.strip()) for char in line.strip().split(',')] \
              for line in f.readlines()]

  output = solve(puzzle)
  print(output)
  path = os.getcwd() + "/output"
  if not os.path.exists(path): 
    os.makedirs(path)
	
  outFile = path+"/{}.out".format(inFile[6:-3])
	
  with open(outFile, 'w', encoding = "utf-8") as f:
    f.write(output)

if __name__ == "__main__":
  main(sys.argv[1])