import re
import datetime
from typing import List

import sys
sys.path.append("..")
import const
import readwrite
import script.utils as utils
from script.item_parser import ItemParser
from connection.connection import SeleniumConnector


class OtodomItemParser(ItemParser):
    
    def __init__(self, url) -> None:
        super().__init__(url)
        self.item = { 'link': url }
    
    @SeleniumConnector.with_selenium()
    def parse(self, browser) -> List[str]:
        self.browser = browser
        if 'from404' in self.browser.current_url:
            print(f'\tError: \t 404 redirection')
            return
        self.parse_price()
        self.parse_date()
        self.parse_location()
        self.parse_highlighted_options()
        self.parse_text()
        readwrite.save_item(self.item)
    
    def parse_price(self) -> None:
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/header/strong'
        price = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        price = float(price.replace('zł', '').replace(' ', '').replace(',', '.'))
        self.item['price_base'] = price
    
    def parse_date(self) -> None:
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/div[5]/div[4]'
        date = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        if s := re.search(r'Data aktualizacji: ([0-9]+) (dni|dzień) temu', date):
            date = datetime.datetime.now() - datetime.timedelta(days=int(s.group(1)))
            self.item['date'] = datetime.datetime.strftime(date, '%d.%m.%Y')
            return
        if s := re.search(rf'Data aktualizacji: ([0-9]+) godzin[{const.REGEX_POLISH_AZ}]* temu', date):
            date = datetime.datetime.now() - datetime.timedelta(hours=int(s.group(1)))
            self.item['date'] = datetime.datetime.strftime(date, '%d.%m.%Y')
            return
        else: print('Data aktualizacji nie w dniach !!!!!!!!!!!!!!')
    
    def parse_location(self) -> None:
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/header/div/a'
        location = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        self.item['location_approximation'] = location.split(',')[-1].strip()
    
    def parse_highlighted_options(self) -> None:
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/div[1]/div'
        options_div = utils.get_soup_by_xpath(self.browser, xpath)[0]
        options = {}
        for div in options_div.findChildren('div', recursive=False):
            divs = div.select('div > div')
            key = divs[0].text
            value = divs[-1].text
            options[key] = value if value != 'Zapytaj' else ''
        
        try: self.item['area'] = float(options['Powierzchnia'].replace('m²', '').replace(',', '.').strip())
        except: pass
        try: self.item['price_additional'] = float(options['Czynsz'].replace('zł', '').replace(',', '.').strip())
        except: pass
        try: self.item['rooms'] = int(options['Liczba pokoi'].strip())
        except: pass
        try: self.item['deposit'] = float(options['Kaucja'].replace('zł', '').replace(',', '.').strip())
        except: pass
        try: self.item['level'] = int(options['Piętro'].strip().split('/')[0])
        except: pass
        try: self.item['build_type'] = options['Rodzaj zabudowy'].strip()
        except: pass
        try: self.item['balcony'] = (options['Balkon / ogród / taras'].strip() != '')
        except: pass
        try: self.item['furniture'] = (options['Stan wykończenia'].strip() == 'do zamieszkania')
        except: pass

    def parse_text(self) -> None:
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/div[3]/div/div[3]/div[2]/div'
        appliances = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        xpath = '//*[@id="__next"]/main/div[3]/div[2]/section[2]/div/div/div'
        text = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        text += f'\nWypozażenie: {appliances}.'
        text_csv = text.replace('\n', ' ')
    
        self.item['whole_text'] = text_csv
        self.item['location'] = self.deduce_value(text, rf'(ul[{const.REGEX_POLISH_AZ}.]+) ([{const.REGEX_POLISH_AZ} ]+ [0-9]+)', 2)
        self.item['shower'] = self.deduce_bool(text, rf'przysznic[{const.REGEX_POLISH_AZ}]+')
        self.item['bath'] = self.deduce_bool(text, rf'wann[{const.REGEX_POLISH_AZ}]+')
        self.item['balcony'] = self.deduce_bool(text, rf'balkon[{const.REGEX_POLISH_AZ}]+')
        self.item['dishwasher'] = self.deduce_bool(text, rf'zmywark[{const.REGEX_POLISH_AZ}]+')
        self.item['induction_stove'] = self.deduce_bool(text, rf'indukc[{const.REGEX_POLISH_AZ}]+')
        self.item['animals'] = self.deduce_surrounding_text(text, rf'zwierz[{const.REGEX_POLISH_AZ}]+', 30)
        self.item['deposit'] = self.deduce_deposit(text)
        
