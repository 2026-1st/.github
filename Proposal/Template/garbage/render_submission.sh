#!/usr/bin/env zsh

set -euo pipefail

cd "$(dirname "$0")"

mkdir -p ../Submission

pushd latex >/dev/null
bibtex proposal >/tmp/proposal_bib.log 2>&1 || true
xelatex -interaction=nonstopmode proposal.tex >/tmp/proposal_tex1.log 2>&1
xelatex -interaction=nonstopmode proposal.tex >/tmp/proposal_tex2.log 2>&1
popd >/dev/null

cp -f latex/proposal.pdf ../Submission/Team1_proposal.pdf

./convert_to_docx.sh

rm -f latex/proposal.aux latex/proposal.bbl latex/proposal.blg latex/proposal.log latex/proposal.out latex/proposal.pdf

echo "생성 완료: ../Submission/Team1_proposal.pdf"
echo "생성 완료: ../Submission/Team1_proposal.docx"