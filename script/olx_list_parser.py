from typing import List


import sys
sys.path.append("..")
from connection.connection import SeleniumConnector
import const
import readwrite
import script.utils as utils


class OlxListParser(SeleniumConnector):
    
    def __init__(self) -> None:
        super().__init__(const.LINK_OLX_LIST)
    
    @SeleniumConnector.with_selenium()
    def get_list_of_links(self, browser) -> List[str]:
        self.browser = browser
        self.get_number_of_pages()
        print(f'Found {self.number_of_pages} pages with results')
        for page in range(1, self.number_of_pages + 1):
            self.get_list_from_page(page)

    def get_number_of_pages(self) -> int:
        selector = 'ul.pagination-list > li:last-of-type'
        item = utils.get_soup_by_css_selector(self.browser, selector)[0]
        try: self.number_of_pages = int(item.text)
        except: self.number_of_pages = None
    
    def get_list_from_page(self, page) -> List[str]:
        url = const.LINK_OLX_LIST + f'&page={page}'
        self.browser.get(url)
        selector = '.listing-grid-container > div > div:has(a)'
        items = utils.get_soup_by_css_selector(self.browser, selector)
        for i in items:
            for a in i.find_all('a', href=True):
                link = a['href']
                if link.startswith('/d/oferta'):
                    link = 'https://www.olx.pl' + link
                readwrite.save_link(link)
                break
        print(f'Found {len(items)} items on {page}th page')
