class POST_handler:

    def __init__(self, POST_url_dict):
        self.POST_url_dict = POST_url_dict
        #print("one is " + str(self.POST_url_dict[0]))
        self.print_POST_url_list()
        while True:
            string = self.user_interaction()
            if isinstance(input, int):
                print_POST_request(input)

    def print_POST_url_list(self):
        print("\nResults:")
        row_format = "| {:^3}|  {:^3}  | {:<70} |"
        print("| {:^3}| {:^3} | {:<70} |".format("NR.", "POSTS", "URL"))
        print("="*87)
        count = 1
        for x in self.POST_url_dict:
            if len(x) > 70:
                print(row_format.format(str(count), str(len(self.POST_url_dict[x])), str(x[:67]) + "..."))
            else:
                print(row_format.format(str(count), str(len(self.POST_url_dict[x])), str(x)))
            count+=1
        print("\n")

    def user_interaction(self):
        string = input("ArthroPOST -> ")
        if string == "help":
             self.show_help_handler()
        return string

    def find_login_forms(self, POST_list):
        possible_login_list = []
        for form in POST_list:
            login_found = re.match(r'pa?s?s?wo?r?d?', str(POST_list[form]))
            if login_found is not None:
                possible_login_list.append(form)
        return possible_login_list

    def show_help_handler(self):
        print('''ArthroPOST lets you handle and edit POST requests.
        Options:
        - view      Lets you view the request(s).
        - edit      Lets you edit the request(s).

        Example: {NR.} + {option}

        Other commands:
        - flogin    Let ArthroPOST search for possible login forms.''')
