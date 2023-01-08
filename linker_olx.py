from enum import Enum


def get_filter_choice(enum, choosen_list, url_name):
    all_options = [e for e in enum]
    if all([item in choosen_list for item in all_options]): return ''
    link = []
    for i, item in enumerate(choosen_list):
        link.append(f'search%5Bfilter_enum_{url_name}%5D%5B{i}%5D={item.value}')
    return '&'.join(part for part in link)

def get_filter_range(min, max, url_name):
    if min is None and max is None: return ''
    link = []
    if min is not None:
        link.append(f'search%5Bfilter_float_{url_name}:from%5D={min}')
    if max is not None:
        link.append(f'search%5Bfilter_float_{url_name}:to%5D={max}')
    return '&'.join(part for part in link)


BASE_LINK = 'https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/'
BASE_LINK += '?search%5Border%5D=created_at:desc' # sort by creation date


class BuildType(Enum):
    BLOK = 'blok'
    KAMIENICA = 'kamienica'
    DOM = 'wolnostojacy'
    SZEREGOWIEC = 'szeregowiec'
    APARTAMENTOWIEC = 'apartamentowiec'
    LOFT = 'loft'
    POZOSTALE = 'pozostale'
FILTER_BUILD_TYPE = [
    BuildType.BLOK,
    BuildType.KAMIENICA,
    BuildType.DOM,
    BuildType.SZEREGOWIEC,
    BuildType.APARTAMENTOWIEC,
    BuildType.LOFT,
    BuildType.POZOSTALE,
]
link_build_type = get_filter_choice(BuildType, FILTER_BUILD_TYPE, 'buildtype')


class Rooms(Enum):
    KAWALERKA = 'one'
    DWA = 'two'
    TRZY = 'three'
    CZTERY_PLUS = 'four'
FILTER_ROOMS = [
    Rooms.KAWALERKA,
    Rooms.DWA,
    Rooms.TRZY,
    Rooms.CZTERY_PLUS,
]
link_rooms = get_filter_choice(Rooms, FILTER_ROOMS, 'rooms')


class Level(Enum):
    SUTERENA = 'floor_-1'
    PARTER = 'floor_0'
    JEDEN = 'floor_1'
    DWA = 'floor_2'
    TRZY = 'floor_3'
    CZTERY = 'floor_4'
    PIEC = 'floor_5'
    SZESC = 'floor_6'
    SIEDEM = 'floor_7'
    OSIEM = 'floor_8'
    DZIEWIEC = 'floor_9'
    DZIESIEC = 'floor_10'
    POWYZEJ_DZIESIEC = 'floor_11'
    PODDASZE = 'floor_17'
FILTER_LEVEL = [
    Level.SUTERENA,
    Level.PARTER,
    Level.JEDEN,
    Level.DWA,
    Level.TRZY,
    Level.CZTERY,
    Level.PIEC,
    Level.SZESC,
    Level.SIEDEM,
    Level.OSIEM,
    Level.DZIEWIEC,
    Level.DZIESIEC,
    Level.POWYZEJ_DZIESIEC,
    Level.PODDASZE,
]
link_level = get_filter_choice(Level, FILTER_LEVEL, 'floor_select')


class Furniture(Enum):
    YES = 'one'
    NO = 'two'
FILTER_FURNITURE = [
    Furniture.YES,
    Furniture.NO,
]
link_furniture = get_filter_choice(Furniture, FILTER_FURNITURE, 'furniture')


PRICE_MIN = None
PRICE_MAX = None
link_price = get_filter_range(PRICE_MIN, PRICE_MAX, 'price')


AREA_MIN = None
AREA_MAX = None
link_area = get_filter_range(AREA_MIN, AREA_MAX, 'm')

links = [link_build_type, link_rooms, link_level, link_furniture, link_price, link_area]
LINK = BASE_LINK + '&'.join([item for item in links if len(item) > 0])
