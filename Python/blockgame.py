vector = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Node(object):
    def __init__(self):
        self.linkedNode = [None] * 4
        pass

    def link(self, node, v):
        assert v in vector
        self.linkedNode[vector.index(v)] = node
        node.linkedNode[(vector.index(v) + 2) % 4] = self

    def getLinkedNode(self, v):
        return self.linkedNode[vector.index(v)]


class Game(object):
    def __init__(self, size):
        self.gameBroad = [[Node() for x in range(size)] for y in range(size)]
        self.size = size
        self.turn = "A"
        pass

    def linkNode(self, x, y, v):
        n = self.gameBroad[x][y]
        x2, y2 = x + v[0], y + v[1]
        assert x2 >= 0 and y2 >= 0
        n2 = self.gameBroad[x2][y2]
        n.link(n2, v)
        return self.checkIfFromBlock(n2, v)

    def checkIfFromBlock(self, n, lastV):
        x = vector.index(lastV) + 1
        y = vector[x:]
        y.extend(vector[:x])
        for i in y:
            n = n.getLinkedNode(i)
            if n is None:
                return False
        return True
        pass

g = Game(3)


def p(x):
    print(x, end="")

g.linkNode(0, 0, vector[0])
g.linkNode(1, 0, vector[1])
g.linkNode(1, 1, vector[2])
g.linkNode(0, 1, vector[3])

p(".")
p(" " if g.gameBroad[0][0].getLinkedNode(vector[0]) is None else "-")
p(".")
p(" " if g.gameBroad[1][0].getLinkedNode(vector[0]) is None else "-")
p(".")
print()
p(" " if g.gameBroad[0][0].getLinkedNode(vector[1]) is None else "|")
p(" ")
p(" " if g.gameBroad[1][0].getLinkedNode(vector[1]) is None else "|")
p(" ")
p(" " if g.gameBroad[2][0].getLinkedNode(vector[1]) is None else "|")
print()
p(".")
p(" " if g.gameBroad[0][1].getLinkedNode(vector[0]) is None else "-")
p(".")
p(" " if g.gameBroad[1][1].getLinkedNode(vector[0]) is None else "-")
p(".")
print()
p(" " if g.gameBroad[0][1].getLinkedNode(vector[1]) is None else "|")
p(" ")
p(" " if g.gameBroad[1][1].getLinkedNode(vector[1]) is None else "|")
p(" ")
p(" " if g.gameBroad[2][1].getLinkedNode(vector[1]) is None else "|")
print()
p(".")
p(" " if g.gameBroad[0][2].getLinkedNode(vector[0]) is None else "-")
p(".")
p(" " if g.gameBroad[1][2].getLinkedNode(vector[0]) is None else "-")
p(".")
print()
