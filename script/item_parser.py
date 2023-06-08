import re

import sys
sys.path.append("..")
import const
from connection.connection import SeleniumConnector


class ItemParser(SeleniumConnector):
    
    def __init__(self, url) -> None:
        super().__init__(url)
        self.item = { 'link': url }

    def deduce_value(self, text, regex, index):
        if match := re.search(regex, text, re.IGNORECASE):
            return match.group(index)
    
    def deduce_bool(self, text, regex):
        return re.search(regex, text, re.IGNORECASE) is not None

    def deduce_surrounding_text(self, text, regex, padding):
        if match := re.search(regex, text, re.IGNORECASE):
            start, end = match.span(0)
            new_start = max(start - padding, 0)
            try: new_start = new_start + text[new_start:start + 1].rindex('\n') + 1
            except: pass
            new_end = min(end + padding, len(text))
            try: new_end = end + text[end:new_end + 1].index('\n')
            except: pass
            return text[new_start:new_end]

    def deduce_deposit(self, text):
        if t := self.deduce_surrounding_text(text, rf'depozyt[{const.REGEX_POLISH_AZ}]+', 20):
            return ', '.join(re.findall(r'[0-9.,]+', t))
        if t := self.deduce_surrounding_text(text, rf'kaucj[{const.REGEX_POLISH_AZ}]+', 20):
            return ', '.join(re.findall(r'[0-9]+[0-9.,]+', t))
