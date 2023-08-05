import spacy
import json
from .baseParser import BaseParser
from spacy.matcher import Matcher


class PriceParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.matcher = Matcher(self.nlp.vocab)
        pattern = [{"LIKE_NUM": True}]
        self.matcher.add("Price", None, pattern)

    def parse_text(self, text, tps, sl):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        prices = []
        if self.debug:
            self.print_result()
        for _, start, end in self.matches:
            span = self.doc[start:end]  # The matched span
            prices.append(span.text)
            for price in tps:
                if price in prices:
                    prices.remove(price)
                if sl in prices:
                    prices.remove(sl)
        prices = list(filter(lambda tmp: not tmp.isdigit() or int(tmp) > 20, prices))
        if len(prices) == 0:
            return ""
        return prices[0]
