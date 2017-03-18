import re

file = open("from.txt", encoding='utf8').read()
output = open("to.txt", "w")

fromList = re.findall(r"[a-zA-z]+", file)
fromList.sort()
output.write("\n".join(fromList))
