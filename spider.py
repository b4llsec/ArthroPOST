from bs4 import BeautifulSoup, Comment
import requests
import re
import sys
from standard_functions import *
from POST_handler import *



class Spider:

    def __init__(self, start_url, only_spider_subdomains, depth):
        self.start_url = start_url
        self.depth = depth
        self.total_POSTS = 0
        self.POST_url_dict = {}
        soup = self.make_soup(self.start_url)
        url_list = self.find_urls(self.start_url, soup, only_spider_subdomains)
        all_url_list = url_list.copy()
        for cycle in range(depth):
            dynamic_print("Searching... Cycle {0}/{1}\n".format(cycle+1, depth))
            new_url_list = []
            for url in url_list:
                try:
                    soup = self.make_soup(url)
                    updated_url = check_string_length(url)
                    dynamic_print("{0} POST requests found. searching through: {1}".format(self.total_POSTS, updated_url))
                    if cycle+1 is not depth:
                        sub_url_list = self.find_urls(url, soup, only_spider_subdomains)
                        for url in sub_url_list:
                            if self.already_seen_url(url, all_url_list) == False:
                                new_url_list.append(url)
                                all_url_list.append(url)
                    self.find_POST_requests(url, soup)

                except Exception as e:
                #    print("\n" + str(e) + "\n")
                    continue
            url_list = list(set(new_url_list))
            if len(url_list) == 0:
                dynamic_print("Found {0} POST requests on {1} pages. No more links to follow! Exiting...\n".format(self.total_POSTS, len(all_url_list)))
                post_handler = POST_handler(self.POST_url_dict)
                sys.exit()
        print("\n")
        dynamic_print("Found {0} POST requests on {1} pages. Exiting...\n".format(self.total_POSTS, len(all_url_list)))
        post_handler = POST_handler(self.POST_url_dict)

    def make_soup(self, url):
        #returns soup object of given url.
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        req = requests.get(url, headers=headers, allow_redirects=True )
        #print(req.status_code)
        req = self.handle_http_status(req)
        html = req.text
        soup = BeautifulSoup(html, features='lxml')
        return soup

    def find_urls(self, base_url, soup, only_subdomains):
        #returns list of urls in given url
        #returns set (only unique values)
        links = soup.find_all('a')
        url_list = [base_url]
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
        if start_url in url:
            return True
        return False


    def already_seen_url(self, url, url_list):
        if url in url_list:
            return True
        return False

    def find_POST_requests(self, url, soup):
        forms = soup.find_all(name='form')
        for form in forms:
            method = form.get('method')
            if method is not None:
                if method.lower() == 'post':
                    self.POST_url_dict.setdefault(url, []).append(form)
                    self.total_POSTS += 1
                #    print("this is dict now: " + str(self.POST_url_dict) + "\n \n")
                    self.check_POST_request(form)

    def check_POST_request(self, form):
        password_match = re.match(r'pa?s?s?w?o?r?d?', str(form))
        if password_match is not None:
            print("PASSWORD MATCH IN: {0}\n".format(str(form)))
            print("possible login field with password input")
            print(str(form))

    def find_js(self, soup):
        scripts = soup.find_all(name='script')
        for script in scripts:
            source = script.get('src')

            #TODO make this so that it checks for http code and stops if not neccesary
    def handle_http_status(self,request):
        if request.status_code == 200:
            return request
        elif 300 <= request.status_code <= 399:
            if request.status_code == 305:
                dynamic_print("{0} POST requests found. URL returns {1}. Proxy needed.".format(self.total_POSTS,request.status_code))
            return request
        else:
            dynamic_print("{0} POST requests found. Page can't be reached! HTTP STATUS CODE: {1}".format(self.total_POSTS, request.status_code))
