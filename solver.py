#  ╓──────────────────────────────────────────────────────────────────╖
#  ║  File name: solver.py                                            ║ 
#  ║  Author: David De Potter, pl3onasm@gmail.com                     ║
#  ║  License: refer to the license file in this repository           ║
#  ║  Description: solves a given sliding puzzle by applying a        ║
#  ║  combination of A*-algorithms and a divide and conquer strategy  ║
#  ╙──────────────────────────────────────────────────────────────────╜

import os, sys
from time import perf_counter  
from puzzle import *
from divide import *
from astar import *
  
def solve (board):
  '''main solver'''

  def prettyPrint (solutionPath):
    # formats the output
    output,num = "",0
    for step,value,puzzle in solutionPath:
      if step == "INITIAL BOARD":
        output += f"\n\t= {step} =\n\n" + puzzle
      else:
        num +=1
        output += f"STEP {num}: Move tile {value} {step}\n\n" + puzzle
    return output, num

  puzzle = Puzzle(board)
  if not puzzle.isSolvable():
    return "\nThe puzzle is unsolvable.\n", 0
  
  path1 = [("INITIAL BOARD","",puzzle.draw())]
  reduceTo2x3(puzzle, len(board[0]), path1)
  path2 = AStar(puzzle)  #solves the remaining 2x3 puzzle 

  if not path1 or not path2:
    return "\nThe puzzle is unsolvable.\n", 0
  return prettyPrint(path1+path2[1:])

  ## <<::::::::::::::::::::::::::::::: Main :::::::::::::::::::::::::::::::>> ##

def main(inFile):
  with open(inFile, 'r') as f:
    puzzle = [[int(char.strip()) for char in line.strip().split(',')] \
              for line in f.readlines()]

  start = perf_counter()
  output, num = solve(puzzle)
  end = perf_counter()
  info = f'\n====<  Solved in {end-start:.3f} s, and in {num} steps  >====\n\n'
  path = os.getcwd() + "/output"
  if not os.path.exists(path): 
    os.makedirs(path)
	
  outFile = path+f"/{inFile[6:-3]}.out"
	
  with open(outFile, 'w', encoding = "utf-8") as f:
    f.write(info + output)

if __name__ == "__main__":
  main(sys.argv[1])