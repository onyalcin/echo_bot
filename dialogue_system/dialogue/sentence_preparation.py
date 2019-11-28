import re
from nltk import TweetTokenizer


class SentenceParser:
    def __init__(self):
        self.tokenizer = TweetTokenizer()

    def parse_sent(self, str_response, expressiveness=0.3):
        response_list = []
        d = {"word_list": [], "expressiveness": expressiveness}
        for sent in re.split('[?.!]', str_response):
            for word in self.tokenizer.tokenize(sent):
                d["word_list"].append(word)
            d["word_list"].append(' . ')
        if d["word_list"]:
            response_list.append(d)
        return response_list