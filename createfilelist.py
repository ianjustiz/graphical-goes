import glob

path = r"./static/assets/images-cool/*.png"
files = glob.glob(path)

print(files)

with open("./static/assets/images-cool/images.txt", "w") as file:
    for line in files:
        file.write(f"{line}\n")