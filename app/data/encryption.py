# Simple encryption function

def encode(data):
    string = ""
    for char in data:
        new_char = chr(ord(char) + 3)
        string+=new_char
    return string

def decode(data):
    string = ""
    for char in data:
        new_char = chr(ord(char) - 3)
        string+=new_char
    return string