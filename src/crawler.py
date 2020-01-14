import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

p = re.compile(r"<[^>]*?>")
tag_to_text = lambda x: p.sub("", x).split('\n')
split_tr = lambda x: str(x).split('</tr>')
pd.set_option('display.max_rows', 100)

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_uma_info_link(url):
    soup = url_to_soup(url)
    link_list = [os.environ['HOME_URL'] + x.get('href') for x in soup.find_all('a', class_='tx-mid tx-low')]
    return link_list

def get_previous_race_result(url):
    soup = url_to_soup(url)
    race_table = soup.select("table.tb01")[2]
    pre_race_result = [tag_to_text(x) for x in split_tr(race_table)]
    return pre_race_result

def get_horse_data(url):
    uma_info_link_list = get_uma_info_link(url)
    # print(uma_info_link_list)
    for x in uma_info_link_list:
        pre_race_result = get_previous_race_result(x)
        df = pd.DataFrame(pre_race_result)[1:][[2, 3, 7, 10, 11, 13, 14, 15, 19, 23]].dropna().rename(columns={
            2: 'date', 3: 'place', 7: 'race_name', 10: 'len', 11: 'wether', 13: 'popularity', 14: 'rank', 15: 'time', 19: 'weight', 23: 'money'
        })
        print(df)

    # https://www.nankankeiba.com/uma_info/2008200010.do
    # https://www.nankankeiba.com/uma_info/2015110103.do
    # race_result = get_previous_race_result('https://www.nankankeiba.com/uma_info/2008200010.do')
    # print(race_result)
    # data = pd.DataFrame(race_result)[1:][[2, 3, 7, 10, 11, 13, 14, 15, 19, 23]].dropna().rename(columns={
    #     2:'date', 3:'place', 7:'race_name', 10:'len', 11:'wether', 13:'popularity', 14:'rank', 15:'time', 19:'weight', 23:'money'
    # })
    # print(data)

def main():
    get_horse_data(os.environ['TOKEY_DAISHOTEN'])

if __name__ == '__main__':
    try:
        main()
    except:
        pass
