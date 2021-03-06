# coding:UTF-8
import json
import csv

def json2csv():
    json_file = open('data/test.json', 'r')
    csv_file = open('data/test.csv', 'w')

    # JSONファイルのロード
    json_dict = json.load(json_file)
    json_file.close()

    # list of dictの抽出
    target_dicts = json_dict['data']

    # csvファイルのロード
    output = csv.writer(csv_file) # ここがうまくいってない

    # dataの書き込み
    output.writerow(target_dicts[0].keys())  # header row
    # print(target_dicts[0].keys())
    for target_dict in target_dicts:
        print(target_dict)
        output.writerow(target_dict.values())  # values row
    csv_file.close()

def main():
    json2csv()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)