#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/index.html の
"患者の発生について" （別紙）PDF ファイル、最新のものを "pdf" フォルダにとってくる

新しくとってきたファイルを stdout に出力する。(なければ、何も出さない)
"""

import argparse
import re
import sys
import requests
import datetime
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from logging import getLogger, DEBUG, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())

BASE_URL = "https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1010035/"
LATEST_REPORT_LIST_KEYWORD = "最新の本部報"
REPORT_PAGE_KEYWORD = "新型コロナウイルスに関連した患者の発生について"
APPENDIX_SELECTOR = "li.pdf > a"
RELEASEDATE_SELECTOR = "div.releasedate > p"
DATE_FORMAT = '%Y%m%d'

# 最新の本部報のURLを取得
def find_latest_report_list_page():
    logger.debug(f"find latest")
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all("a"):
        if LATEST_REPORT_LIST_KEYWORD in str(a.string):
            return urljoin(BASE_URL, a.get("href"))
    return ""

# PDFのURLを取得
def find_report_pdf(report_page_url: str):
    r = requests.get(report_page_url)
    soup = BeautifulSoup(r.content, "html.parser")
    a = soup.select_one(APPENDIX_SELECTOR)

    p = soup.select_one(RELEASEDATE_SELECTOR)
    m = re.search(r"令和(\d+)年(\d+)月(\d+)日", p.string)
    date = '{0}{1:02d}{2:02d}'.format(int(m.group(1)) + 2018, int(m.group(2)), int(m.group(3)))
    logger.debug('date:' + date)
    return (urljoin(report_page_url, a.get("href")), date)

# def find_report_page(date: str):
#     logger.debug(f"find {date}")
#     t = tomorrow(date)
#     y = int(t[0:4]) - 2018
#     m = int(t[4:6])
#     d = int(t[6:8])
#     pattern = '令和{0}年{1}月{2}日'.format(y, m, d)
#     r = requests.get(BASE_URL)
#     soup = BeautifulSoup(r.content, "html.parser")
#     for a in soup.find_all("a"):
#         if REPORT_PAGE_KEYWORD in str(a.string):
#             dt = a.find_previous("dt")
#             if (re.search(pattern, dt.string) != None):
#                 return urljoin(BASE_URL, a.get("href"))
#     return ""

# 本部報リスト(url)から最新の患者の発生についてのページのURLを取得
def find_latest_report_page(url: str):
    logger.debug(f"find latest from {url}")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all("a"):
        if REPORT_PAGE_KEYWORD in str(a.string):
            return urljoin(BASE_URL, a.get("href"))
    return ""

# 本部報リスト(url)から指定された日付の患者の発生についてのページのURLを取得
def find_report_page(url: str, date: str):
    logger.debug(f"find date: {date} from {url}")
    t = tomorrow(date)
    y = int(t[0:4]) - 2018
    m = int(t[4:6])
    d = int(t[6:8])
    pattern = '令和{0}年{1}月{2}日'.format(y, m, d)
    parent = parent_url(url)
    logger.debug(parent)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all("a"):
        if REPORT_PAGE_KEYWORD in str(a.string):
            url = parent + "/" + a.get("href")
            r = requests.get(url)
            logger.debug(f"check {url}")
            s = BeautifulSoup(r.content, 'html.parser')
            if (re.search(pattern, s.select_one('.releasedate>p').text) != None):
                logger.debug(f"found: {date} report")
                return url
    return ""

# PDFを取得
def fetch_pdf(report_pdf_url: str, datestr=None):
    url_path = urlsplit(report_pdf_url).path
    path = Path(url_path)
    logger.debug(path)
    if (datestr == None):
        filename = yesterday(path.stem[0:8]) + path.suffix
    else:
        filename = datestr + ".pdf"
    local_path = Path("pdf") / filename
    # ダウンロード済みかをチェック、すでにファイルがあれば何もしない
    if local_path.exists():
        return ""

    # ダウンロード
    urlretrieve(report_pdf_url, str(local_path))
    return str(local_path)

def parent_url(urlstr: str):
    url = urlsplit(urlstr)
    parent_path = Path(url.path).parents[0]
    return url.scheme + "://" + url.hostname + str(parent_path)

def yesterday(date: str):
    today = datetime.datetime.strptime(date, DATE_FORMAT)
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime(DATE_FORMAT)

def tomorrow(date: str):
    today = datetime.datetime.strptime(date, DATE_FORMAT)
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.strftime(DATE_FORMAT)

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--date', type=str, help='取得したい日付(YYYYmmdd)')
    parser.add_argument('--debug', help='Debugログ', action='store_true')
    parser.add_argument('-u', '--url', type=str, help='URL')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(DEBUG)

    if (args.url == None):
        report_list_url = find_latest_report_list_page()
    else:
        report_list_url = args.url

    logger.debug(f"list: {report_list_url}")
        
    if (args.date == None):
        report_page_url = find_latest_report_page(report_list_url)
    else:
        if (re.match('\d{8}$', args.date) != None):
            report_page_url = find_report_page(report_list_url, args.date)
        else:
            parser.print_help()

    logger.debug(f"report: {report_page_url}")
    if not report_page_url:
        sys.exit(1)  # まったくないことはないはず

    (report_pdf_url, datestr) = find_report_pdf(report_page_url)
    logger.debug(report_pdf_url)
    if not report_pdf_url:
        sys.exit(1)  # まったくないことはないはず
    local_pdf_path = fetch_pdf(report_pdf_url, yesterday(datestr))

    # ダウンロードした場合、ダウンロードしたファイル名を stdout に出す
    print(local_pdf_path)

if __name__ == '__main__':
    main()
