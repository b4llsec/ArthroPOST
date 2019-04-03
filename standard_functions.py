import sys
import os

ERASE_LINE = '\x1b[2K'

def read_config_file():
    config = {}
    with open('config') as f:
        for line in f:
            config[line.strip("\n").split(" ")[0].strip(":")] = line.strip("\n").split(" ")[1]
        return config

def clear_line():
    # Clears the current Terminal line
    sys.stdout.write(ERASE_LINE)
    sys.stdout.flush()

def dynamic_print(string):
    # Prints to the same Terminal line.
    clear_line()
    sys.stdout.write( "\r" + string)
    sys.stdout.flush()

def check_string_length(string):
    if len(string) >70:
        string = string[:70] + "..."
    return string
