#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/index.html の
"患者の発生について" （別紙）から、区ごとの発生状況を読み取り、カンマ区切りで出力
"""

import argparse
import re
import math
from collections import defaultdict

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextLine
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from logging import getLogger, DEBUG, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())

# 区ごとの情報が記載されている箇所の座標情報
# PDF は左下原点のため、START のほうが Y が大きい。
TABLE_START_Y1 = 400
TABLE_END_Y1 = 150


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', type=str, help='別紙 PDF のファイル名')
    parser.add_argument('--debug', help='Debugログ', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(DEBUG)

    # 指定範囲内の LTTextLine を読み取り
    texts = parse_txt(args.filename)
    first_page_texts = next(texts)
    table_texts = filter(lambda b: TABLE_END_Y1 < b.y1 < TABLE_START_Y1, first_page_texts)

    start = 0
    endlabel = 0
    for table_text in table_texts:
        if (re.search('千代田', table_text.get_text()) != None):
            start = math.ceil(table_text.y1)
            continue
        if (re.search('新島', table_text.get_text()) != None):
            endlabel = math.floor(table_text.y1)

    firstnum = 0
    for table_text in table_texts:
        if (re.search('\d+', table_text.get_text()) != None):
            firstnum = math.floor(table_text.y1)
            break
    diff = start - firstnum
    end = endlabel - diff

    table_texts = filter(lambda b: end < b.y1 < start, first_page_texts)

    # 読み取った LTTextLine を 行ごとに区分け
    lines = defaultdict(list)
    for table_text in table_texts:
        t_list = table_text.get_text().strip().split()  # たまに一つの LTTextLine に複数テキストがあるので split
        logger.debug(t_list)
        new_list = []
        for t in t_list:
            if (len(t) > 10):
                continue
            if (len(t) > 4):
                new_list.append(t[0:4])
                new_list.append(t[4:len(t)])
            else:
                new_list.append(t)
        logger.debug(new_list)
        if (len(new_list) > 0):
            lines[table_text.y1].extend(new_list)

    # 各行で対応する要素を出力
    for k1, k2 in pairs(lines):
        for place, count in zip(lines[k1], lines[k2]):
            if (re.search('^\d+$', count) != None):
                print(f"{place},{count}")


def pairs(iterable, c=2):
    """
    c ごとに iterable を区切る generator
    :param iterable: 区切る対象
    :param c: 区切る数。デフォルト 2
    :return:

    pairs('ABCDE') --> ['A', 'B'], ['C', 'D'], ['E']
    pairs(range(6)) --> [0, 1], [2, 3], [4, 5]
    pairs(range(7)) --> [0, 1], [2, 3], [4, 5], [6]
    """
    r = []
    for i, item in enumerate(iterable):
        r.append(item)
        if i % c == c - 1:
            yield r
            r = []
    if r:  # 余りがあったら、それも yield
        yield r


def parse_txt(filename: str):
    """
    from [【PDFMiner】PDFからテキストの抽出 \- Qiita](https://qiita.com/mczkzk/items/894110558fb890c930b5)
      LTTextBox でなく LTTextLine 単位でとるよう改変
    :param filename: PDF ファイル名
    :return: 1 ページごとに List[LTTextLine] を generate
    """

    def find_textboxes_recursively(layout_obj):
        """
        再帰的にテキストライン（LTTextLine）を探して、テキストボックスのリストを取得する。
        """
        # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
        if isinstance(layout_obj, LTTextLine):
            return [layout_obj]

        # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
        if isinstance(layout_obj, LTContainer):
            boxes = []
            for child in layout_obj:
                boxes.extend(find_textboxes_recursively(child))

            return boxes

        return []  # その他の場合は空リストを返す。

    # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
    laparams = LAParams(detect_vertical=True)

    # 共有のリソースを管理するリソースマネージャーを作成。
    resource_manager = PDFResourceManager()

    # ページを集めるPageAggregatorオブジェクトを作成。
    device = PDFPageAggregator(resource_manager, laparams=laparams)

    # Interpreterオブジェクトを作成。
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(filename, 'rb') as f:
        # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する。
        # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号（0始まり）のリストを指定するとよい。
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)  # ページを処理する。
            layout = device.get_result()  # LTPageオブジェクトを取得。

            # ページ内のテキストボックスのリストを取得する。
            boxes = find_textboxes_recursively(layout)

            # テキストボックスの左上の座標の順でテキストボックスをソートする。
            # y1（Y座標の値）は上に行くほど大きくなるので、正負を反転させている。
            boxes.sort(key=lambda b: (-b.y1, b.x0))

            yield boxes


if __name__ == '__main__':
    main()
