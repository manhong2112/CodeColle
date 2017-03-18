# -*- coding:utf8 -*-
poem = "\
静夜思 李白\n\
床前明月光，\n\
疑似地上霜。\n\
举头望明月，\n\
低头思故乡。".split('\n')

poem = poem[::-1]

poemLength = 0
for i in poem:
    poemLength = len(i) if poemLength < len(i) else poemLength
poemWidth = len(poem)

for i in range(0, poemLength):
    for j in range(0, poemWidth):
        try:
            print(poem[j][i] if poem[j][i] != " " else "  ", end="|")
        except IndexError:
            print(end="  |")
    print()
