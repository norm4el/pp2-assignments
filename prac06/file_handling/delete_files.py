import os
import shutil

source_file = "sample.txt"
backup_file = "sample_backup.txt"

with open(source_file, "a") as file:
    file.write("aaaaaa\n")
    file.write("bbbb\n")

with open(source_file, "r") as file:
    print(file.read())

shutil.copy(source_file, backup_file)

file_to_delete = "temp.txt"

if os.path.exists(source_file):
    os.remove(source_file)
    print("deleted safely")
else:
    print("does not exist.")