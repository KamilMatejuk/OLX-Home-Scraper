import time
import locale
import datetime
from typing import List

import sys
sys.path.append("..")
import const
import readwrite
import script.utils as utils
from script.item_parser import ItemParser
from connection.connection import SeleniumConnector


class OlxItemParser(ItemParser):

    @SeleniumConnector.with_selenium()
    def parse(self, browser) -> List[str]:
        self.browser = browser
        self.container_xpath = f'/html/body/div[1]/div[2]/div[3]/div[3]/div[1]/div[{2 if self.check_img() else 1}]'
        self.close_popup()
        self.parse_price()
        self.parse_date()
        self.parse_location()
        self.parse_highlighted_options()
        # self.parse_text()
        self.parse_phone()
        self.parse_all_content()
        readwrite.save_item(self.item)
    
    def check_img(self) -> bool:
        try:
            xpath = '/html/body/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/img'
            utils.get_soup_by_xpath(self.browser, xpath, 5)[0]
            return True
        except: return False
    
    def close_popup(self):
        xpath = '//*[@id="onetrust-accept-btn-handler"]'
        utils.click_button_by_xpath(self.browser, xpath)

    def parse_price(self) -> None:
        xpath = f'{self.container_xpath}/div[3]/h3'
        price = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        price = float(price.replace('zł', '').replace(' ', ''))
        self.item['price_base'] = price
    
    def parse_date(self) -> None:
        xpath = f'{self.container_xpath}/div[1]/span/span'
        date = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        locale.setlocale(locale.LC_TIME, 'pl_PL.utf8')
        if 'dzisiaj' in date.lower():
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, '%d %B %Y')
        self.item['date'] = datetime.datetime.strftime(date, '%d.%m.%Y')

    def parse_location(self) -> None:
        xpath = '/html/body/div[1]/div[2]/div[3]/div[3]/div[2]/div[2]/div/section/div[1]/div/p[1]'
        location = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        self.item['location_approximation'] = location.replace('Wrocław,', '').strip()
        
    def parse_highlighted_options(self) -> None:
        xpath = f'{self.container_xpath}/ul'
        options_ul = utils.get_soup_by_xpath(self.browser, xpath)[0]
        options = []
        for li in options_ul.find_all('li'):
            options.append(li.find_all('p')[0].text)
        self.parse_highlighted(options, 'Rodzaj zabudowy:', 'build_type')
        self.parse_highlighted(options, 'Liczba pokoi:', 'rooms')
        self.parse_highlighted(options, 'Poziom:', 'level', lambda x: int(x))
        self.parse_highlighted(options, 'Umeblowane:', 'furniture')
        self.parse_highlighted(options, 'Powierzchnia:', 'area', lambda x: float(x.replace('m²', '').strip()))
        self.parse_highlighted(options, 'Czynsz (dodatkowo):', 'price_additional', lambda x: float(x.replace('zł', '').replace(' ', '')))
    
    def parse_highlighted(self, options, option_str, header, f=None) -> None:
        values = filter(lambda o: option_str in o, options)
        if value := next(values, None):
            self.item[header] = value.replace(option_str, '').strip()
            if f is not None:
                try: self.item[header] = f(self.item[header])
                except: pass
    
    # def parse_text(self):
    #     xpath = f'{self.container_xpath}/div[8]/div'
    #     text = utils.get_soup_by_xpath(self.browser, xpath)[0].text
    #     self.item['location'] = self.deduce_value(text, rf'(ul[{const.REGEX_POLISH_AZ}.]*)([{const.REGEX_POLISH_AZ}0-9 ]+)', 2)
    #     self.item['shower'] = self.deduce_bool(text, rf'przysznic[{const.REGEX_POLISH_AZ}]+')
    #     self.item['bath'] = self.deduce_bool(text, rf'wann[{const.REGEX_POLISH_AZ}]+')
    #     self.item['balcony'] = self.deduce_bool(text, rf'balkon[{const.REGEX_POLISH_AZ}]+')
    #     self.item['dishwasher'] = self.deduce_bool(text, rf'zmywark[{const.REGEX_POLISH_AZ}]+')
    #     self.item['induction_stove'] = self.deduce_bool(text, rf'indukc[{const.REGEX_POLISH_AZ}]+')
    #     self.item['animals'] = self.deduce_surrounding_text(text, rf'zwierz[{const.REGEX_POLISH_AZ}]+', 30)
    #     self.item['deposit'] = self.deduce_deposit(text)

    def parse_phone(self):
        xpath = '/html/body/div[1]/div[2]/div[3]/div[3]/div[2]/div[1]/div[3]/div/button[1]'
        utils.click_button_by_xpath(self.browser, xpath)
        time.sleep(5) # required
        phone = utils.get_soup_by_xpath(self.browser, xpath)[0].text
        self.item['phone'] = phone.replace(' ', '')

    def parse_all_content(self):
        element = utils.get_soup_by_xpath(self.browser, self.container_xpath)[0]
        children_with_text = element.find_all(text=True)
        not_allowed = ['{', '}', 'Opis', 'Ubezpieczenie Najemcy']
        self.item['whole_text'] = '. '.join([c for c in children_with_text if len(c) > 1 and all([na not in c for na in not_allowed])])
