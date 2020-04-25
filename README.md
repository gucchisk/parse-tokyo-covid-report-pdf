# parse-tokyo-covid-report-pdf

fork元の[parse-tokyo-covid-report-pdf](https://github.com/smatsumt/parse-tokyo-covid-report-pdf)を改変しております。

## fetch_tokyo_covid_report_pdf.py
https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/index.html から最新の "新型コロナウイルスに関連した患者の発生について" のページを抽出し、ページに添付されて別紙のPDFファイルのURLを検出しダウンロードします。  
オリジナルはファイル名が更新された日付になっていますが、実際の情報の日付（更新日時の前日）になるように変更してます。

## parse_tokyo_covid_report_pdf.py
上記のfetch_tokyo_covid_report_pdf.pyでダウンロードしたPDFファイルから区ごとの発生状況を読み取り、カンマ区切りで出力します。

## Usage

※最初の1回のみ
```shell script
$ pip3 install -r requirements.txt
```
or
```
$ pipenv install
```

```
$ pipenv run ./parse_tokyo_covid_report_pdf.py 20200411.pdf
# 千代田,10
# 中央,33
# 港,143
...
```
