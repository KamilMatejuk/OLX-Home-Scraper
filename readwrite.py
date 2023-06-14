import os
import csv
from typing import List
import const


def get_links() -> List[str]:
    if not os.path.exists(const.LINKS_FILE):
        print(f'File {const.LINKS_FILE} doesn\'t exist')
        return []
    with open(const.LINKS_FILE, 'r') as f:
        return [line.replace('\n', '') for line in f.readlines()]


def save_links(links: List[str]) -> None:
    with open(const.LINKS_FILE, 'w+') as f:
        links = [link + '\n' for link in links if not link.endswith('\n')]
        f.writelines(links)


def save_link(link: str) -> None:
    with open(const.LINKS_FILE, 'a+') as f:
        f.write(link + '\n')

def get_items() -> List[dict]:
    if not os.path.exists(const.ITEMS_FILE):
        print(f'File {const.ITEMS_FILE} doesn\'t exist')
        return []
    items = []
    with open(const.ITEMS_FILE, 'r') as f:
        for row in csv.DictReader(f, delimiter=',', fieldnames=const.ITEMS_HEADERS):
            items.append(row)
    return items[1:]

def save_items(items: List[dict]) -> None:
    with open(const.ITEMS_FILE, 'w+') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=const.ITEMS_HEADERS)
        writer.writeheader()
        writer.writerows(items)

def save_item(item: dict) -> None:
    with open(const.ITEMS_FILE, 'r+') as f:
        if len(f.readlines()) == 0:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=const.ITEMS_HEADERS)
            writer.writeheader()
    with open(const.ITEMS_FILE, 'a') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=const.ITEMS_HEADERS)
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].replace('\n', '').strip()
        item = {k: v for k, v in item.items() if k in const.ITEMS_HEADERS}
        writer.writerow(item)
