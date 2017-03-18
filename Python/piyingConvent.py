# encoding: utf-8
import os
import sys
if len(sys.argv) == 3:
  sys.exit("py piyingConvent.py <input>")
file = sys.argv[2]
input = open(file,encoding = 'utf8')
output = open(file.split(".")[0] + ".o.txt",'w',encoding = 'utf8')
i = 0
table = {"ā":"a","á":"a","ǎ":"a","à":"a","ō":"o","ó":"o","ǒ":"o","ò":"o","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"}
while 1:
  i = 0
  line = input.readline()
  if not line:
    break
  charArray = list(line)
  oline = ""
  for eachChar in charArray:
    if eachChar in table:
      charArray[i] = table[eachChar]
    i += 1
  output.write("".join(charArray))