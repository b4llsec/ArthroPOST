from bs4 import BeautifulSoup, Comment
import urllib.request
import ssl
import re

class Spider:

    def __init__(self, start_url, depth):
        self.start_url = start_url
        self.depth = depth
        self.POST_url_list = []
        soup = self.make_soup(self.start_url)
        url_list = self.find_urls(self.start_url, soup)
        all_url_list = url_list.copy()
        for cycle in range(depth):
            print(cycle)
            new_url_list = []
            for url in url_list:
                try:
                    soup = self.make_soup(url)
                    sub_url_list = self.find_urls(url, soup)
                    self.find_POST_requests(url, soup)
                    for url in sub_url_list:
                        if self.already_seen_url(url, all_url_list) == False:
                            new_url_list.append(url)
                            all_url_list.append(url)
                except:
                    print(url + " Can't be reached. continuing...")
                    continue
            url_list = list(set(new_url_list))

    def make_soup(self, url):
        #returns soup object of given url.
        #clears for any ssl certificate errors and adds header
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        ctx = ssl.SSLContext()
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(req, context=ctx).read()
        soup = BeautifulSoup(html, features='lxml')
        return soup

    def find_urls(self, base_url, soup):
        #returns list of urls in given url
        #returns set (only unique values)
        links = soup.find_all('a')
        url_list = [base_url]
        only_subdomains = "False"
        for tag in links:
            url = tag.get('href', None)
            if url is not None:
                url = self.normalize_url(url, base_url)
                if self.already_seen_url(url, url_list) == False:
                    if only_subdomains == "True":
                        if self.check_if_subdomain(url, base_url) == True:
                            url_list.append(url)
                    if only_subdomains == "False":
                        match = re.search(r'https?://', url)
                        if match is not None:
                            url_list.append(url)
        return list(set(url_list))

        #TODO make http/https interchangable

    def normalize_url(self, url, base_url):
        #takes a (found) url and parses it to a working url (if necessary).
        if url.startswith("/") or url.startswith("../"):
            if base_url.endswith("/"):
                base_url = base_url[:-1]
                url = base_url + url
            else:
                url = base_url + url
        return url

    def check_if_subdomain(self, url, start_url):
        match = re.match(start_url, url)
        if match is not None:
            return True
        return False


    def already_seen_url(self, url, url_list):
        if url in url_list:
            return True
        return False

    def find_POST_requests(self, url, soup):
        print("searching through "+ str(url))
        forms = soup.find_all(name='form')
        for form in forms:
            method = form.get('method')
            if method is not None:
                if method.lower() == 'post':
                    print("Found POST request in: " + url)
                    self.POST_url_list.append(url)

    def find_js(self, soup):
        scripts = soup.find_all(name='script')
        for script in scripts:
            source = script.get('src')
