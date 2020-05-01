#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse

from logging import getLogger, DEBUG, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())

ids = {
  '千代田': { 'autonomy': '区', 'id': 'chiyoda' },
  '中央': { 'autonomy': '区', 'id': 'chuo' },
  '港': { 'autonomy': '区', 'id': 'minato' },
  '新宿': { 'autonomy': '区', 'id': 'shinjuku' },
  '文京': { 'autonomy': '区', 'id': 'bunkyo' },
  '台東': { 'autonomy': '区', 'id': 'taito' },
  '墨田': { 'autonomy': '区', 'id': 'sumida' },
  '江東': { 'autonomy': '区', 'id': 'koto' },
  '品川': { 'autonomy': '区', 'id': 'shinagawa' },
  '目黒': { 'autonomy': '区', 'id': 'meguro' },
  '大田': { 'autonomy': '区', 'id': 'ota' },
  '世田谷': { 'autonomy': '区', 'id': 'setagaya' },
  '渋谷': { 'autonomy': '区', 'id': 'shibuya' },
  '中野': { 'autonomy': '区', 'id': 'nakano' },
  '杉並': { 'autonomy': '区', 'id': 'suginami' },
  '豊島': { 'autonomy': '区', 'id': 'toshima' },
  '北': { 'autonomy': '区', 'id': 'kita' },
  '荒川': { 'autonomy': '区', 'id': 'arakawa' },
  '板橋': { 'autonomy': '区', 'id': 'itabashi' },
  '練馬': { 'autonomy': '区', 'id': 'nerima' },
  '足立': { 'autonomy': '区', 'id': 'adachi' },
  '葛飾': { 'autonomy': '区', 'id': 'katsushika' },
  '江戸川': { 'autonomy': '区', 'id': 'edogawa' },
  '八王子': { 'autonomy': '市', 'id': 'hachioji' },
  '立川': { 'autonomy': '市', 'id': 'tachikawa' },
  '武蔵野': { 'autonomy': '市', 'id': 'musashino' },
  '三鷹': { 'autonomy': '市', 'id': 'mitaka' },
  '青梅': { 'autonomy': '市', 'id': 'ome' },
  '府中': { 'autonomy': '市', 'id': 'fuchu' },
  '青梅': { 'autonomy': '市', 'id': 'ome' },
  '昭島': { 'autonomy': '市', 'id': 'akishima' },
  '調布': { 'autonomy': '市', 'id': 'chofu' },
  '町田': { 'autonomy': '市', 'id': 'machida' },
  '小金井': { 'autonomy': '市', 'id': 'koganei' },
  '小平': { 'autonomy': '市', 'id': 'kodaira' },
  '日野': { 'autonomy': '市', 'id': 'hino' },
  '東村山': { 'autonomy': '市', 'id': 'higashimurayama' },
  '国分寺': { 'autonomy': '市', 'id': 'kokubunji' },
  '国立': { 'autonomy': '市', 'id': 'kunitachi' },
  '福生': { 'autonomy': '市', 'id': 'fussa' },
  '狛江': { 'autonomy': '市', 'id': 'komae' },
  '東大和': { 'autonomy': '市', 'id': 'higashiyamato' },
  '清瀬': { 'autonomy': '市', 'id': 'kiyose' },
  '東久留米': { 'autonomy': '市', 'id': 'higashikurume' },
  '武蔵村山': { 'autonomy': '市', 'id': 'musashimurayama' },
  '多摩': { 'autonomy': '市', 'id': 'tama' },
  '稲城': { 'autonomy': '市', 'id': 'inagi' },
  '羽村': { 'autonomy': '市', 'id': 'hamura' },
  'あきる野': { 'autonomy': '市', 'id': 'akiruno' },
  '西東京': { 'autonomy': '市', 'id': 'nishitokyo' },
  '瑞穂': { 'autonomy': '町', 'id': 'mizuho' },
  '日の出': { 'autonomy': '町', 'id': 'hinode' },
  '奥多摩': { 'autonomy': '町', 'id': 'okutama' },  
  '大島': { 'autonomy': '町', 'id': 'oshima' },
  '八丈': { 'autonomy': '町', 'id': 'hachijo' },
  '檜原': { 'autonomy': '村', 'id': 'hinohara' },
  '利島': { 'autonomy': '村', 'id': 'toshimamura' },
  '新島': { 'autonomy': '村', 'id': 'niijima' },
  '神津島': { 'autonomy': '村', 'id': 'kouzushima' },
  '三宅': { 'autonomy': '村', 'id': 'miyake' },  
  '御蔵島': { 'autonomy': '村', 'id': 'mikurasima' },
  '青ヶ島': { 'autonomy': '村', 'id': 'aogashima' },
  '小笠原': { 'autonomy': '村', 'id': 'ogasawara' }
}

def csvlist():
    files = os.listdir('csv')
    files.sort()
    return files

def create(name: str):
    id = ids[name]['id']
    path = 'data/' + id + '.csv'
    with open(path, mode='w') as f:
        for file in csvlist():
            num = get('csv/' + file, name)
            match = re.search('(\d{8})', file)
            f.write(match.group(1) + ',' + num)


def get(file: str, name: str):
    with open(file, mode='r') as f:
        for line in f:
            texts = line.split(',')
            if (texts[0] == name):
                return texts[1]
        return None
    

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--debug', help='Debugログ', action='store_true')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(DEBUG)

    for name in ids:
        create(name)

if __name__ == '__main__':
    main()
