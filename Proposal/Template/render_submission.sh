#!/usr/bin/env zsh

set -euo pipefail

cd "$(dirname "$0")"

mkdir -p ../Submission

bibtex proposal >/tmp/proposal_bib.log 2>&1 || true
xelatex -interaction=nonstopmode proposal.tex >/tmp/proposal_tex1.log 2>&1
xelatex -interaction=nonstopmode proposal.tex >/tmp/proposal_tex2.log 2>&1

cp -f proposal.pdf ../Submission/proposal.pdf

./convert_to_docx.sh

rm -f proposal.aux proposal.bbl proposal.blg proposal.log proposal.out proposal.pdf

echo "생성 완료: ../Submission/proposal.pdf"
echo "생성 완료: ../Submission/proposal.docx"