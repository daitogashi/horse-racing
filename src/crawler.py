import csv
import json
import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

p = re.compile(r"<[^>]*?>")
tag_to_text = lambda x: p.sub("", x).split('\n')
split_tr = lambda x: str(x).split('</tr>')
pd.set_option('display.max_rows', 100)


# テスト用のクラス、メソッド付き
class MyClass:
    def my_method(self):
        return True

# テスト用のクラス、ネストして使う用
class ChildClass:
    pass

def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError

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

def get_horse_name(url):
    soup = url_to_soup(url)
    horse_name = soup.find('h2', id='tl-prof')
    return horse_name.text

def get_horse_data(url):
    pre_race_result = get_previous_race_result(url)
    df = pd.DataFrame(pre_race_result)[2:12][[2, 3, 7, 10, 11, 13, 14, 15, 19, 23]].dropna().rename(columns={
        2: 'date', 3: 'place', 7: 'race_name', 10: 'len', 11: 'weather', 13: 'popularity', 14: 'rank', 15: 'time', 19: 'weight', 23: 'money'
    })
    return df

def test():
    data = {}
    uma_info_link_list = get_uma_info_link(os.environ['TOKEY_DAISHOTEN'])
    for url in uma_info_link_list:
        data[url] = {}
        df = get_horse_data(url)
        for idx, row in df.iterrows():
            idx = str(idx)
            data[url][idx] = {}

            if row['popularity'] == '':
                continue

            # 今回は不要なデータ
            # data[url][idx]['date'] = row['date']
            # data[url][idx]['place'] = row['place']

            # 必要なデータ
            data[url][idx]['horse_cnt'] = int(row['rank'].split('/')[1])
            data[url][idx]['money'] = int(row['money'].replace(',', ''))
            data[url][idx]['result_rank'] = int(row['rank'].split('/')[0])
            data[url][idx]['len'] = int(row['len'][0:4])  # 当時との差分
            data[url][idx]['popularity'] = int(row['popularity'])
            data[url][idx]['weight'] = int(row['weight'])
            try:
                time = datetime.strptime(row['time'], '%M:%S.%f')
                data[url][idx]['sec'] = int(time.minute * 60 + time.second + time.microsecond / 1000000)
            except ValueError:
                time = datetime.strptime(row['time'], '%S.%f')
                data[url][idx]['sec'] = int(time.second + time.microsecond / 1000000)
            data[url][idx]['same_place'] = 1 if row['place'].replace('☆ ', '').startswith('大井') else 0
            # 馬場状態
            data[url][idx]['soil_heavy'] = 1 if row['weather'][-2:] == '/重' else 0  # 当日と同じデータだけにする
            data[url][idx]['soil_s_heavy'] = 1 if row['weather'][-2:] == '稍重' else 0  # 当日と同じデータだけにする
            data[url][idx]['soil_good'] = 1 if row['weather'][-2:] == '/良' else 0  # 当日と同じデータだけにする
            data[url][idx]['soil_bad'] = 1 if row['weather'][-2:] == '不良' else 0  # 当日と同じデータだけにする
    print(data)

def nankankeiba_20191229():
    data = []
    uma_info_link_list = get_uma_info_link(os.environ['TOKEY_DAISHOTEN'])
    for url in uma_info_link_list:
        object = MyClass()
        object.url = url
        object.horse_race_data = []
        df = get_horse_data(url)
        for idx, row in df.iterrows():
            if row['popularity'] == '':
                continue
            race_data = ChildClass()
            race_data.horse_cnt = int(row['rank'].split('/')[1])
            race_data.money = int(row['money'].replace(',', ''))
            race_data.result_rank = int(row['rank'].split('/')[0])
            race_data.len = int(row['len'][0:4])  # 当時との差分
            race_data.popularity = int(row['popularity'])
            race_data.weight = int(row['weight'])
            try:
                time = datetime.strptime(row['time'], '%M:%S.%f')
                race_data.sec = int(time.minute * 60 + time.second + time.microsecond / 1000000)
            except ValueError:
                time = datetime.strptime(row['time'], '%S.%f')
                race_data.sec = int(time.second + time.microsecond / 1000000)
            race_data.same_place = 1 if row['place'].replace('☆ ', '').startswith('大井') else 0
            # 馬場状態
            race_data.soil_heavy = 1 if row['weather'][-2:] == '/重' else 0 # 当日と同じデータだけにする
            race_data.soil_s_heavy = 1 if row['weather'][-2:] == '稍重' else 0 # 当日と同じデータだけにする
            race_data.soil_good = 1 if row['weather'][-2:] == '/良' else 0 # 当日と同じデータだけにする
            race_data.soil_bad = 1 if row['weather'][-2:] == '不良' else 0 # 当日と同じデータだけにする
            object.horse_race_data.append(race_data)
        data.append(object)
    print(json.dumps(data, default=default_method, indent=2))

def main():
    nankankeiba_20191229()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
