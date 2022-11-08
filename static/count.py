import os

c = 0
for i in os.scandir():
     i = str(i)
     i = i.replace('<', '')
     i = i.replace('>', '')
     i = i.replace("DirEntry ", '')
     i = i.replace("'", "")
     f = open(i, 'r')
     try:
          for j in f.read():
               c+=1
     except:
          print(i + " not counted")

print(c - 14)