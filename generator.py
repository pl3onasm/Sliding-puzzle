#  ╓──────────────────────────────────────────────────────────────────────╖
#  ║  File name: generator.py                                             ║ 
#  ║  Author: David De Potter, pl3onasm@gmail.com                         ║
#  ║  License: refer to the license file in this repository               ║
#  ║  Description: generates a random puzzle of the given width and type  ║
#  ║  (both passed as command line arguments) and outputs a .in file in   ║  
#  ║  the input directory (which will be created if it does not exist)    ║
#  ╙──────────────────────────────────────────────────────────────────────╜

import random, sys, os

def generator(width):
  p = list(range(0,width**2))
  random.shuffle(p)
  return p

def getBlankX (board, width):
  for x in board:
    if board[x] == 0: return x//width

def solvable (board, width):
  '''verifies whether a given puzzle is solvable or not'''
  def inversions (arr):
    inversions, l = 0, len(arr)
    for i in range(l):
      for j in range(i + 1, l):
        if (arr[i] > arr[j]): inversions += 1
    return inversions      
  
  copy = board.copy()
  copy.remove(0)
  if width & 1: #odd
    return 0 if (inversions(copy) & 1) else 1
  return 1 if ((inversions(copy) + getBlankX(board, width)) & 1) else 0

def getFileNumber(path):
  files = os.listdir(path)
  if files:
    for idx,file in enumerate(files):
      files[idx] = int(file[:-3])
    files.sort()
    return 1 + files.pop()
  return 1

def stringify (arr, width):
  string = ""
  for row in range(width):
    for i, d in enumerate(range (width)):
      string += str(arr.pop())
      if i < width-1: string += ", "
    string += '\n'
  return string

def main():
  if len(sys.argv) == 1 :
    print("\nPlease provide the width and the type of puzzle\n"
    "you want to generate.\n")
    return
  elif len(sys.argv) == 2:
    print("\nPlease provide the type of puzzle you want to\n"
    "generate: r for random, or s for solvable.\n")
    return
  elif len(sys.argv) > 3:
    print("\nMore than two parameters were passed.\n")
    return
  else:
    width = int(sys.argv[1])
    ptype = sys.argv[2]

  path = os.getcwd() + "/input"
  if not os.path.exists(path): os.makedirs(path)
	
  fileNum = getFileNumber(path)
  file = path + f"/{fileNum}.in"

  if ptype == 's':
    d = "solvable "
    while 1:
      p = generator(width)
      if solvable(p, width): break
  elif ptype == 'r':
    d = "(solvable or unsolvable) "
    p = generator(width)
  else:
    print("\nPlease provide a valid parameter for the puzzle\n"
    "you want to generate: r for random, or s for solvable\n")
    return

  with open(file, 'w', encoding = "utf-8") as f:
    f.write(stringify(p, width))

  print("\nA random {} x {} {}sliding puzzle\nhas been added "
  "as file \"{}.in\" to the \input\nsubdirectory of the current "
  "working directory.\n".format(width,width,d,fileNum))

if __name__ == "__main__":
   main()
