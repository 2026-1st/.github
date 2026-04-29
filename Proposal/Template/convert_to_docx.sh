#!/usr/bin/env zsh

set -euo pipefail

cd "$(dirname "$0")"

mkdir -p ../Submission

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc이 설치되어 있지 않습니다. 설치 후 다시 실행하세요."
  echo "macOS 예시: brew install pandoc"
  exit 1
fi

if ! command -v /Users/songhune/.pyenv/versions/3.10.10/bin/python >/dev/null 2>&1; then
  echo "Python 실행 파일을 찾을 수 없습니다."
  exit 1
fi

/Users/songhune/.pyenv/versions/3.10.10/bin/python build_reference_docx.py

tmp_docx="proposal.raw.docx"

pandoc proposal.md \
  --from markdown \
  --to docx \
  --standalone \
  --citeproc \
  --bibliography=references.bib \
  --reference-doc=reference.docx \
  --output "$tmp_docx"

/Users/songhune/.pyenv/versions/3.10.10/bin/python postprocess_docx.py "$tmp_docx" ../Submission/proposal.docx
rm -f "$tmp_docx"

echo "생성 완료: ../Submission/proposal.docx"
