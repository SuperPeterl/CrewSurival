import json 
import os
def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def write_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

def remove_file(file_name):
    os.remove(file_name)
