# Proposal 작업 안내

이제 작업 폴더는 Proposal로 관리한다.

## 폴더 구조

- Template: 원본 템플릿, 참고문헌, 변환 스크립트
- Submission: 최종 제출본 PDF/DOCX

## 제목 양식 통일

문서 제목은 아래 형식으로 통일한다.

- 2026-1 기계학습기초 팀 프로젝트 Proposal

제출 파일명은 아래처럼 고정한다.

- proposal.pdf
- proposal.docx

## 제출 안내

최종 제출본은 Submission 폴더에만 둔다.

5월 8일까지 최종 파일을 정리해서 push 한다.

지각 제출은 20\% 감점한다.

## Overleaf 사용

1. proposal.tex, ieee_fullname.bst, references.bib를 업로드한다.
2. Compiler를 XeLaTeX로 설정한다.
3. 제목 양식을 유지한 채 팀 정보와 내용을 수정한다.
4. 최종 PDF는 Submission 기준 결과물과 동일하게 관리한다.

## 최종 렌더링

```bash
chmod +x render_submission.sh convert_to_docx.sh
./render_submission.sh
```

위 명령은 Template 원본으로부터 최종 PDF와 DOCX를 생성해 Submission 폴더에 넣는다.

현재 DOCX 변환은 Pandoc 기본 출력이 아니라 reference.docx와 후처리 스크립트를 기준으로 생성된다. 따라서 A4, 좁은 여백, 1단-2단 전환, 제목/본문 스타일이 템플릿 기준으로 유지된다.