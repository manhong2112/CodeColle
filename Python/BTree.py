null = None
class BTree(object):
  def __init__(self, val):
    self.val = val
    self.left = null
    self.right = null

  def insert(self, elem):
    if self.val == null:
      self.val = elem
    if self.val == elem:
      pass
    else:
      if self.val < elem:
        if self.right == null:
          self.right = BTree(elem)
        else:
          self.right.insert(elem)
      else:
        if self.left == null:
          self.left = BTree(elem)
        else:
          self.left.insert(elem)

def tree(arr):
  t = BTree(null)
  for i in arr:
    t.insert(i)
  return t

def postorder(p, indent=0):
    if p != None:
        if p.left:
            postorder(p.left, indent+4)
        if p.right:
            postorder(p.right, indent+4)
        x = "{:>" + str(indent) + "}"
        print("{} {}".format(x.format(""), p.val))
