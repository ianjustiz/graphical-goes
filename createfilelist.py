import sys
import os

path = sys.argv[1]

files = os.listdir(path)

print(files)

with open("{}/images.txt".format(path), "wb") as file:
    incrementer = 0

    for line in sorted(files):
        if line.find(".png") != -1:
            incrementer += 1
            
            if len(sorted(files)) != incrementer:
                file.write("{}/{}\n".format(path, line).encode())
            else:
                file.write("{}/{}".format(path, line).encode())