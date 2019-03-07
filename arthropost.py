from spider import *
import argparse

header = """    _       _   _            ___  ___  ___ _____
   /_\  _ _| |_| |_  _ _ ___| _ \/ _ \/ __|_   _|
  / _ \| '_|  _| ' \| '_/ _ \  _/ (_) \__ \ | |
 /_/ \_\_|  \__|_||_|_| \___/_|  \___/|___/ |_|
"""

if __name__ == "__main__":
    print(header)
    url = "http://www.bible.ca"
    spider = Spider(url, 5)

    #parser = argparse.Argumentparser(description='ArthroPOST spiders webpages and returns pages with POST request forms.')
    #parser.add_argument()
