from collections import namedtuple
Node = namedtuple("Node", "hash key value next")

def forEachNode(node: Node, func):
   while node:
      func(node)
      node = node.next

class HashMap():
   def __init__(self, size=16):
      self.bucket = [None] * size
      self.size = 16
      while self.size < size:
         self.size <<= 1
      self.threshold = size >> 1
      self.len = 0
   
   def put(self, key, value):
      h = hash(key)
      index = h & (self.size - 1)
      self.bucket[index] = Node(h, key, value, self.bucket[index])
      self.len += 1
      if self.len >= self.threshold:
         self.resize()

   def get(self, key):
      h = hash(key)
      index = h & (self.size - 1)
      return self.search(self.bucket[index], key)
   
   def resize(self):
      print("resize!")
      size = self.size << 1
      threshold = size >> 1

      new_bucket = [None] * size
      def put(node: Node):
         h = node.hash
         index = h & (size - 1)
         new_bucket[index] = Node(node.hash, node.key, node.value, new_bucket[index])
      
      for i in self.bucket:
         # i : Node
         forEachNode(i, lambda node: put(node))
      
      self.bucket = new_bucket
      self.size = size
      self.threshold = threshold
   
   def search(self, node: Node, key):
      while node:
         if node.hash == hash(key) and node.key == key:
            return node.value
         else:
            node = node.next
      assert False
   

import random
h = HashMap(128)
for k in range(0, 100):
   v = random.randint(1, 100)
   h.put(str(k), v)
   print(v == h.get(str(k)))
