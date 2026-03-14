import os
import shutil

os.mkdir("folder1")
os.mkdir("folder1/folder2")
os.mkdir("folder1/folder2/folder3")

print("All items:")
for item in os.listdir():
    print(item)