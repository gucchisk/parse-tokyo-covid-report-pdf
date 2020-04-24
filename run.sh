#!/usr/bin/env bash

# PDF をとってくる
NEW_PDF_FILE=$(pipenv run ./fetch_tokyo_covid_report_pdf.py)
if [[ -z "${NEW_PDF_FILE}" ]] ;then
  echo "No new PDF. exited"
  exit 255
fi

# PDF から CSV を生成
NEW_CSV_FILE=${NEW_PDF_FILE//pdf/csv}

echo "pipenv run ./parse_tokyo_covid_report_pdf.py ${NEW_PDF_FILE} > ${NEW_CSV_FILE}"

pipenv run ./parse_tokyo_covid_report_pdf.py ${NEW_PDF_FILE} > ${NEW_CSV_FILE}



# latest.csv のコピーを生成
# cp "${NEW_CSV_FILE}" csv/latest.csv
