from spider import *
from standard_functions import *

header = """    _       _   _            ___  ___  ___ _____
   /_\  _ _| |_| |_  _ _ ___| _ \/ _ \/ __|_   _|
  / _ \| '_|  _| ' \| '_/ _ \  _/ (_) \__ \ | |
 /_/ \_\_|  \__|_||_|_| \___/_|  \___/|___/ |_|
"""


if __name__ == "__main__":
    url = sys.argv[1]
    print("\nThis is ArthroPOST, a webcrawler that looks for POST requests.")
    print(header)
    print("URL: {0}".format(url))
    config = read_config_file()
    only_subdomains = config["only_spider_subdomains"]
    depth = int(config["max_spider_depth"])
    spider = Spider(url, only_subdomains, depth)
