import re

import sys
sys.path.append("..")
import const
from connection.connection import SeleniumConnector


class ItemParser(SeleniumConnector):
    
    def __init__(self, url) -> None:
        super().__init__(url)
        self.item = { 'link': url }
