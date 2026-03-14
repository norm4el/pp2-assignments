file_name = "sample.txt"

with open(file_name, "r") as file:
    content = file.read()

print("File contents:")
print(content)