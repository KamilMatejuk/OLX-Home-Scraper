import const
import datetime
import readwrite
from script.olx_list_parser import OlxListParser
from script.olx_item_parser import OlxItemParser
from script.otodom_item_parser import OtodomItemParser


if __name__ == '__main__':
    if const.TYPE == const.Workload.CREATE_LINKS_LIST:
        print('Creating list of links')
        parser = OlxListParser()
        parser.get_list_of_links()
        exit()
    
    if const.TYPE == const.Workload.CLEAN_UP_LINKS_LIST:
        print('Cleaning up list of links')
        links = readwrite.get_links()
        print(f'Before: {len(links)}')
        links = sorted(list(dict.fromkeys(links)))
        print(f'After: {len(links)}')
        readwrite.save_links(links)
        exit()

    if const.TYPE == const.Workload.CREATE_ITEMS_CVS:
        print('Creating items file')
        analyzed = list(map(lambda x: x['link'], readwrite.get_items()))
        links = readwrite.get_links()
        new_links = list(filter(lambda l: l not in analyzed, links))
        diff = len(links) - len(new_links)
        if diff > 0: print(f'Skipping {diff} links, already in file')
        print()
        links_olx = list(filter(lambda l: l.startswith('https://www.olx.pl'), new_links))
        print(f'Found {len(links_olx)} links in olx domain')
        links_otodom = list(filter(lambda l: l.startswith('https://www.otodom.pl'), new_links))
        print(f'Found {len(links_otodom)} links in otodom domain')
        links_other = list(filter(lambda l: l not in links_olx and l not in links_otodom, new_links))
        print(f'Found {len(links_other)} links in other domains')
        print()
        for i, link in enumerate(links_olx):
            print(link)
            OlxItemParser(link).parse()
            print(f'[{str(i+1):>4}/{len(links_olx)}] Parsed')
        for i, link in enumerate(links_otodom):
            print(link)
            OtodomItemParser(link).parse()
            print(f'[{str(i+1):>4}/{len(links_otodom)}] Parsed')
        exit()
    
    if const.TYPE == const.Workload.CLEAN_UP_ITEMS_LIST:
        print('Cleaning up list of items')
        items = readwrite.get_items()
        print(f'Before: {len(items)}')
        items = list(filter(lambda i: i['link'] != 'link', items))
        items = [dict(t) for t in {tuple(d.items()) for d in items}]
        items = sorted(items, reverse=True, key=lambda i: datetime.datetime.strptime(i['date'], '%d.%m.%Y'))
        print(f'After: {len(items)}')
        readwrite.save_items(items)
        exit()
    
    if const.TYPE == const.Workload.DEDUCE_DETAILS:
        items = readwrite.get_items()
        for i in items:
            print(i['location'])
        exit()