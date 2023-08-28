import os

directory = './files/inputs/'  # replace 'path_to_directory' with your folder path
file_contents = []

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            file_contents.append(file.read())

print(file_contents)
