import shutil
import os

os.mkdir("source")
os.mkdir("destination")

with open("source/test.txt", "w") as f:
    f.write("Hello")

shutil.copy("source/test.txt", "destination/test_copy.txt")
print("File copied")

shutil.move("source/test.txt", "destination/test.txt")
print("File moved")