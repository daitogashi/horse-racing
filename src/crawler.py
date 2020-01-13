import requests
import os
from bs4 import BeautifulSoup

tag_to_text = lambda x: p.sub("", x).split('\n')
split_tr = lambda x: str(x).split('</tr>')

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def horse_page_link(url):
    soup = url_to_soup(url)
    link_list = [os.environ['HOME_URL'] + x.get('href') for x in soup.find_all('a', class_='tx-mid tx-low')]
    return link_list

def main():
    print(os.environ['TOKEY_DAISHOTEN'])
    print(horse_page_link(os.environ['TOKEY_DAISHOTEN']))

if __name__ == '__main__':
    try:
        main()
    except:
        pass
