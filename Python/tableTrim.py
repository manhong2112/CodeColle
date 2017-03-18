# encoding: utf-8
import re

file = open("table.txt", encoding = 'utf8')
f = open("table-trim.txt",'w',encoding = 'utf8')
i = 0
while 1:
  line = file.readline()
  if not line:
    break
  arg = line.split(',')
  if(arg[0] != arg[1].split('\n')[0]):
    f.write(line.split(',')[0] + ',' + line.split(',')[1])

#print(result)