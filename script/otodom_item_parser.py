import re
import time
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
    
    @SeleniumConnector.with_selenium()
    def parse(self, browser) -> List[str]:
        self.browser = browser
        if 'from404' in self.browser.current_url:
            print(f'\tError: \t 404 redirection')
            return
        self.close_popup()
        self.parse_price()
        self.parse_date()
        self.parse_location()
        self.parse_highlighted_options()
        self.parse_phone()
        self.parse_all_content()
        readwrite.save_item(self.item)
    
    def close_popup(self):
        xpath = '//*[@id="onetrust-accept-btn-handler"]'
        utils.click_button_by_xpath(self.browser, xpath)
    
    def parse_price(self) -> None:
        xpath = '/html/body/div[1]/main/div[3]/div[2]/header/strong'
        price = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        price = float(price.replace('zł', '').replace(' ', '').replace(',', '.'))
        self.item['price_base'] = price
    
    def parse_date(self) -> None:
        xpath = '/html/body/div[1]/main/div[3]/div[2]/div[6]/div[3]'
        date = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        if s := re.search(r'Data dodania: *([0-9]+) (dni|dzień) temu', date):
            date = datetime.datetime.now() - datetime.timedelta(days=int(s.group(1)))
            self.item['date'] = datetime.datetime.strftime(date, '%d.%m.%Y')
            return
        if s := re.search(rf'Data dodania: *([0-9]+) godzin[{const.REGEX_POLISH_AZ}]* temu', date):
            date = datetime.datetime.now() - datetime.timedelta(hours=int(s.group(1)))
            self.item['date'] = datetime.datetime.strftime(date, '%d.%m.%Y')
            return
        else: print('Data dodania nie w dniach !!!!!!!!!!!!!!')
    
    def parse_location(self) -> None:
        xpath = '/html/body/div[1]/main/div[3]/div[2]/header/div/a'
        location = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        self.item['location_approximation'] = location.split(',')[0].strip()
    
    def parse_highlighted_options(self) -> None:
        xpath = '/html/body/div[1]/main/div[3]/div[2]/div[1]/div'
        options_div = utils.get_soup_by_xpath(self.browser, xpath)[0]
        options = {}
        for div in options_div.findChildren('div', recursive=False):
            divs = div.select('div > div')
            key = divs[0].text
            value = divs[-1].text
            options[key] = value if value != 'Zapytaj' else ''
        
        get_digits = lambda x: re.sub(r'[^0-9,\.]', '', x).replace(',', '.').strip()
        try: self.item['area'] = float(get_digits(options['Powierzchnia']))
        except: pass
        try: self.item['price_additional'] = float(get_digits(options['Czynsz']))
        except: pass
        try: self.item['rooms'] = int(get_digits(options['Liczba pokoi']))
        except: pass
        try: self.item['deposit'] = float(get_digits(options['Kaucja']))
        except: pass
        try: self.item['level'] = int(get_digits(options['Piętro'].strip().split('/')[0]))
        except: pass
        try: self.item['build_type'] = options['Rodzaj zabudowy'].strip()
        except: pass
        # try: self.item['balcony'] = (options['Balkon / ogród / taras'].strip() != '')
        # except: pass
        try: self.item['furniture'] = (options['Stan wykończenia'].strip() == 'do zamieszkania')
        except: pass

    def parse_phone(self):
        xpath = '/html/body/div[1]/main/div[3]/aside/div/div[1]/div/div/div[3]/div/button'
        utils.click_button_by_xpath(self.browser, xpath)
        time.sleep(5) # required
        xpath = '/html/body/div[1]/main/div[3]/aside/div/div[1]/div/div/div[3]/div/a'
        phone = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        self.item['phone'] = phone.replace(' ', '')

    def parse_all_content(self):
        children_with_text = []
        xpath = '/html/body/div[1]/main/div[3]/div[2]/div[1]'
        element = utils.get_soup_by_xpath(self.browser, xpath)[0]
        children_with_text += element.find_all(text=True)
        xpath = '/html/body/div[1]/main/div[3]/div[2]/section[2]/div/div/div'
        element = utils.get_soup_by_xpath(self.browser, xpath)[0]
        children_with_text += element.find_all(text=True)
        not_allowed = ['Szczegóły ogłoszenia']
        self.item['whole_text'] = '. '.join([c for c in children_with_text if len(c) > 1 and all([na not in c for na in not_allowed])])
