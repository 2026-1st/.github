#!/usr/bin/env zsh

set -euo pipefail

cd "$(dirname "$0")"

mkdir -p ../Submission

pushd latex >/dev/null
bibtex report >/tmp/report_bib.log 2>&1 || true
xelatex -interaction=nonstopmode report.tex >/tmp/report_tex1.log 2>&1
xelatex -interaction=nonstopmode report.tex >/tmp/report_tex2.log 2>&1
popd >/dev/null

cp -f latex/report.pdf ../Submission/Team1_report.pdf

./convert_to_docx.sh

rm -f latex/report.aux latex/report.bbl latex/report.blg latex/report.log latex/report.out latex/report.pdf

echo "생성 완료: ../Submission/Team1_report.pdf"
echo "생성 완료: ../Submission/Team1_report.docx"