import os

for i in os.scandir():
     i = str(i)
     i = i.replace('<', '')
     i = i.replace('>', '')
     i = i.replace("DirEntry ", '')
     i = i.replace("'", "")
     print(i)