import random
import string

randstr = lambda n: ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=n))


class Node():
   def __init__(self, k, v, n, f=None):
      self.key = k
      self.value = v
      self.next: Node = n
      self.forward: Node = f
   def clone(self):
      return Node(self.key, self.value, self.next, self.forward)


def toSortedLinkedList(lst):
   lst = sorted(lst)
   n = Node(lst[-1][0], lst[-1][1], None)
   for i in lst[:-1][::-1]:
      n = Node(i[0], i[1], n)
   return n


def skiplist(node, factor=0.5):
   if not node:
      return None
   head = node.clone()
   head.forward = node
   tmp = head
   n = head
   while n.next:
      n = n.next
      if random.random() > factor:
         continue
      new = n.clone()
      new.forward = n
      tmp.next = new
      tmp = new
   return head


def search(node: Node, key):
   while node:
      if key == node.key:
         return node
      if node.next and node.next.key >key:
         node = node.forward
      else:
         node = node.next
