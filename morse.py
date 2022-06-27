#Morse Code Using a Binary Tree - adapted from www.101computing.net/morse-code-using-a-binary-tree/

#A class to implement a Node / Tree
class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right
    
#Convert Character (Find the character using a pre-order traversal of the Binary Tree
def getMorseCode(node, character, code):
  if node==None:
    return False
  elif node.value==character:
    return True
  else:  
    if getMorseCode(node.left,character,code)==True:
      code.insert(0,".")
      return True
    elif getMorseCode(node.right,character,code)==True:
      code.insert(0,"-")
      return True
      
#Let's initialise our binary tree:
tree = Node("START") #The root node of our binary tree

# 1st Level
tree.left = Node("E")
tree.right = Node("T")

# 2nd Level
tree.left.left = Node("I")
tree.left.right = Node("A")
tree.right.left = Node("N")
tree.right.right = Node("M")

# 3rd Level
tree.left.left.left = Node("S")
tree.left.left.right = Node("U")
tree.left.right.left = Node("R")
tree.left.right.right = Node("W")

tree.right.left.left = Node("D")
tree.right.left.right = Node("K")
tree.right.right.left = Node("G")
tree.right.right.right = Node("O")

# 4th Level
tree.left.left.left.left = Node("H")
tree.left.left.left.right = Node("V")
tree.left.left.right.left = Node("F")
tree.left.left.right.right = Node("")
tree.left.right.left.left = Node("L")
tree.left.right.left.right = Node("")
tree.left.right.right.left = Node("P")
tree.left.right.right.right = Node("J")

tree.right.left.left.left = Node("B")
tree.right.left.left.right = Node("X")
tree.right.left.right.left = Node("C")
tree.right.left.right.right = Node("Y")
tree.right.right.left.left = Node("Z")
tree.right.right.left.right = Node("Q")
tree.right.right.right.left = Node("")
tree.right.right.right.right = Node("")

# 5th Level
tree.left.left.left.left.left = Node("1")
tree.left.left.left.left.right = Node("")
tree.left.left.left.right.left = Node("")
tree.left.left.left.right.right = Node("")
tree.left.left.right.left.left = Node("")
tree.left.left.right.left.right = Node("")
tree.left.left.right.right.left = Node("2")
tree.left.left.right.right.right = Node("")
tree.left.right.left.left.left = Node("")
tree.left.right.left.left.right = Node("")
tree.left.right.left.right.left = Node("3")
tree.left.right.left.right.right = Node("")
tree.left.right.right.left.left = Node("4")
tree.left.right.right.left.right = Node("5")

tree.right.left.left.left.left = Node("0")
tree.right.left.left.left.right = Node("9")
tree.right.left.left.right.left = Node("")
tree.right.left.left.right.right = Node("8")
tree.right.left.right.left.left = Node("")
tree.right.left.right.left.right = Node("")
tree.right.left.right.right.left = Node("")
tree.right.left.right.right.right = Node("7")
tree.right.right.left.left.left = Node("")
tree.right.right.left.left.right = Node("")
tree.right.right.left.right.left = Node("")
tree.right.right.left.right.right = Node("")
tree.right.right.right.left.left = Node("")
tree.right.right.right.left.right = Node("")
tree.right.right.right.right.left = Node("6")
tree.right.right.right.right.right = Node("")

def encode(message):
  morseCode = ""
  for character in message:
    dotsdashes = []
    getMorseCode(tree,character,dotsdashes)
    code = "".join(dotsdashes)
    morseCode = morseCode + code + "/"
  return morseCode