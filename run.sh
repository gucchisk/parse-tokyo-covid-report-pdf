#!/usr/bin/env bash

# PDF をとってくる
echo "pipenv run ./fetch_tokyo_covid_report_pdf.py"
NEW_PDF_FILE=$(pipenv run ./fetch_tokyo_covid_report_pdf.py)
STATUS=$?

if [ $STATUS -ne 0 ]; then
    exit $STATUS
fi
if [[ -z "${NEW_PDF_FILE}" ]] ;then
  echo "No new PDF. exited"
  exit 255
fi

# PDF から CSV を生成
NEW_CSV_FILE=${NEW_PDF_FILE//pdf/csv}

echo "pipenv run ./parse_tokyo_covid_report_pdf.py ${NEW_PDF_FILE} > ${NEW_CSV_FILE}"
pipenv run ./parse_tokyo_covid_report_pdf.py ${NEW_PDF_FILE} > ${NEW_CSV_FILE}

# list.txtを更新
echo "./update_list.py"
./update_list.py

# 区市町村別のcsvを作成
echo "./create_ward_report.py"
./create_ward_report.py
