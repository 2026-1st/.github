# Git / GitHub 가이드

> VCS(버전 관리 시스템)를 처음 접하는 학생을 위한 **Git·GitHub 기초 및 팀 협업 방법** 안내입니다.

---

## 목차

1. [Git이 뭔가요?](#1-git이-뭔가요)
2. [Git vs GitHub](#2-git-vs-github)
3. [설치 및 초기 설정](#3-설치-및-초기-설정)
4. [핵심 개념 한눈에 보기](#4-핵심-개념-한눈에-보기)
5. [자주 쓰는 명령어](#5-자주-쓰는-명령어)
6. [팀 협업 워크플로우](#6-팀-협업-워크플로우)
7. [좋은 커밋 메시지 작성법](#7-좋은-커밋-메시지-작성법)
8. [브랜치 전략](#8-브랜치-전략)
9. [이슈(Issue) 활용](#9-이슈issue-활용)
10. [Pull Request(PR) 만들기](#10-pull-requestpr-만들기)
11. [자주 발생하는 문제 해결](#11-자주-발생하는-문제-해결)
12. [추가 학습 자료](#12-추가-학습-자료)

---

## 1. Git이 뭔가요?

**Git**은 파일의 변경 이력을 추적하는 **버전 관리 시스템(Version Control System, VCS)**입니다.

- 과거 버전으로 되돌릴 수 있습니다.
- 팀원이 동시에 같은 파일을 수정해도 **충돌(conflict) 을 감지하고 병합**할 수 있습니다.
- 누가, 언제, 무엇을 바꿨는지 기록이 남습니다.

### 왜 써야 하나요?

| 상황 | Git 없이 | Git 있으면 |
|------|----------|-----------|
| 코드 실수로 망가짐 | 이전 버전 없음 😢 | 언제든 되돌리기 가능 ✅ |
| 팀원이 같은 파일 수정 | 파일 덮어씀 😱 | 충돌 감지 후 병합 ✅ |
| "지난 주 버전이 더 좋았는데" | 찾을 수 없음 😰 | 커밋 기록에서 복원 ✅ |
| 새 기능 시도 | 원본 파일이 망가질 수 있음 | 브랜치에서 안전하게 시도 ✅ |

---

## 2. Git vs GitHub

| | Git | GitHub |
|---|-----|--------|
| 정체 | 로컬 버전 관리 소프트웨어 | Git 저장소를 호스팅하는 웹 서비스 |
| 설치 | 내 컴퓨터에 설치 | 웹 브라우저로 접근 |
| 역할 | 변경 이력 추적 | 협업·공유·PR·이슈 관리 |

> 비유: Git = 사진 찍는 카메라, GitHub = 사진을 올리는 앨범 서비스

---

## 3. 설치 및 초기 설정

### Git 설치

- **Windows**: [https://git-scm.com/download/win](https://git-scm.com/download/win) 에서 다운로드 후 설치
- **macOS**: 터미널에서 `git --version` 입력 (없으면 Xcode Command Line Tools 설치 안내가 뜸)
- **Linux (Ubuntu)**: `sudo apt install git`

설치 확인:

```bash
git --version
# 예: git version 2.43.0
```

### 최초 사용자 정보 설정 (한 번만)

```bash
git config --global user.name "홍길동"
git config --global user.email "hong@ajou.ac.kr"
```

> ⚠️ GitHub 계정 이메일과 동일하게 설정해야 커밋 기여자로 인식됩니다.

---

## 4. 핵심 개념 한눈에 보기

```
작업 디렉토리(Working Directory)
    ↓  git add
스테이징 영역(Staging Area / Index)
    ↓  git commit
로컬 저장소(Local Repository)
    ↓  git push
원격 저장소(Remote Repository, GitHub)
```

| 용어 | 설명 |
|------|------|
| **Repository (저장소)** | 프로젝트 파일과 변경 이력 전체를 담는 공간 |
| **Commit** | 변경 사항을 로컬 저장소에 저장하는 행위. "스냅샷"이라고 생각하면 됨 |
| **Branch** | 독립적인 작업 흐름. 원본(`main`)을 건드리지 않고 기능 개발 가능 |
| **Merge** | 브랜치를 다른 브랜치에 합치는 것 |
| **Pull Request (PR)** | 내 브랜치를 `main`에 합쳐달라고 요청하는 것 (GitHub 기능) |
| **Clone** | 원격 저장소를 내 컴퓨터로 복사 |
| **Push** | 로컬 커밋을 원격 저장소(GitHub)로 업로드 |
| **Pull** | 원격 저장소의 최신 변경사항을 내 컴퓨터로 가져오기 |
| **Conflict (충돌)** | 두 브랜치가 같은 줄을 다르게 수정했을 때 발생 |

---

## 5. 자주 쓰는 명령어

### 저장소 복제

```bash
# GitHub에서 팀 저장소 클론
git clone https://github.com/<팀-계정>/<저장소-이름>.git
cd <저장소-이름>
```

### 상태 확인

```bash
git status          # 현재 변경된 파일 목록 확인
git log --oneline   # 커밋 이력 간략히 보기
git diff            # 아직 스테이징 안 된 변경사항 보기
```

### 변경사항 저장 (add → commit)

```bash
git add 파일명          # 특정 파일만 스테이징
git add .               # 현재 디렉토리의 모든 변경 파일 스테이징
git commit -m "메시지"  # 커밋 (메시지 작성 규칙은 아래 참고)
```

### 원격 저장소와 동기화

```bash
git pull origin main    # 원격 main 브랜치의 최신 변경을 로컬에 가져오기
git push origin <브랜치명>   # 내 브랜치를 원격에 업로드
```

### 브랜치 관련

```bash
git branch                  # 브랜치 목록 확인
git branch <브랜치명>       # 새 브랜치 만들기
git switch <브랜치명>       # 브랜치 이동
git switch -c <브랜치명>    # 새 브랜치 만들면서 이동 (권장)
git merge <브랜치명>        # 현재 브랜치에 다른 브랜치 병합
```

---

## 6. 팀 협업 워크플로우

아래는 4인 팀이 실제로 사용할 수 있는 기본 플로우입니다.

```
1. 저장소 클론 또는 pull로 최신화
        ↓
2. 작업할 브랜치 생성 (예: feature/eda-analysis)
        ↓
3. 코드 작성·수정
        ↓
4. git add → git commit (의미 있는 단위로)
        ↓
5. git push origin <브랜치명>
        ↓
6. GitHub에서 Pull Request 열기
        ↓
7. 팀원 코드 리뷰 (선택) → Merge
        ↓
8. 로컬 main 브랜치 pull로 최신화
```

### 실전 예시

```bash
# 최신 main 가져오기
git switch main
git pull origin main

# 새 작업 브랜치 생성
git switch -c feature/data-preprocessing

# 작업 후 저장
git add notebooks/preprocess.ipynb
git commit -m "feat: 결측치 처리 및 이상치 제거 추가"

# 원격에 업로드
git push origin feature/data-preprocessing

# GitHub에서 PR 생성 → 팀원 리뷰 → Merge
```

---

## 7. 좋은 커밋 메시지 작성법

커밋 메시지는 **채점 항목**에 포함됩니다. 명확한 메시지를 작성하세요.

### 기본 형식

```
<타입>: <무엇을 했는지 간결하게>

(선택) 자세한 설명 – 왜 이 변경을 했는지, 어떤 방법을 썼는지
```

### 타입 예시

| 타입 | 의미 |
|------|------|
| `feat` | 새 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 수정 (README 등) |
| `refactor` | 동작 변화 없이 코드 구조 개선 |
| `data` | 데이터 추가·수정 |
| `exp` | 실험 추가·수정 |
| `chore` | 기타 설정 변경 (패키지, 환경 등) |

### 좋은 예 vs 나쁜 예

| ❌ 나쁜 예 | ✅ 좋은 예 |
|-----------|-----------|
| `수정함` | `fix: SVM 하이퍼파라미터 C 범위 오류 수정` |
| `업데이트` | `feat: 랜덤포레스트 모델 학습 및 교차검증 추가` |
| `asdf` | `docs: README에 실행 방법 및 환경 정보 추가` |
| `final_진짜최종` | `exp: 정규화 방법 비교 실험 (MinMax vs Standard)` |

---

## 8. 브랜치 전략

팀 프로젝트에서 권장하는 간단한 브랜치 구조입니다.

```
main ──────────────────────────────── (최종 완성 코드)
  └── feature/eda              (EDA 담당 팀원)
  └── feature/model-training   (모델 학습 담당 팀원)
  └── feature/report           (보고서 작성 담당 팀원)
  └── fix/seed-setting         (버그 수정)
```

### 브랜치 이름 규칙

| 패턴 | 용도 |
|------|------|
| `feature/<설명>` | 새 기능·분석 작업 |
| `fix/<설명>` | 버그·오류 수정 |
| `docs/<설명>` | 문서 작업 |
| `exp/<설명>` | 실험·비교 |

> 💡 **팁**: `main` 브랜치에 직접 커밋하지 말고, 항상 브랜치를 만들어 작업한 뒤 PR로 병합하세요.

---

## 9. 이슈(Issue) 활용

GitHub 이슈는 **할 일·버그·토론**을 추적하는 공간입니다.

### 이슈 만들기

GitHub 저장소 → `Issues` 탭 → `New issue` 클릭

### 이슈 예시

```
제목: [EDA] 타겟 변수 불균형 확인 필요

## 배경
훈련 데이터에서 클래스 0:1 비율이 약 9:1로 심각한 불균형 관측됨.

## 할 일
- [ ] 클래스별 샘플 수 시각화
- [ ] SMOTE 또는 가중치 조정 방법 조사
- [ ] 비교 실험 설계
```

### 커밋에서 이슈 닫기

커밋 메시지에 `closes #이슈번호`를 쓰면 PR merge 시 이슈가 자동으로 닫힙니다.

```bash
git commit -m "feat: SMOTE 적용으로 클래스 불균형 처리 closes #3"
```

---

## 10. Pull Request(PR) 만들기

### PR 생성 순서

1. 브랜치를 push한 뒤 GitHub 저장소에 접속합니다.
2. 노란색 배너에 `Compare & pull request` 버튼이 뜨면 클릭.
   (없으면 `Pull requests` 탭 → `New pull request`)
3. **base**: `main`, **compare**: 내 브랜치 선택.
4. PR 제목과 설명 작성.
5. `Create pull request` 클릭.

### 좋은 PR 설명 예시

```markdown
## 변경 사항
- 랜덤포레스트 모델 학습 코드 추가 (notebooks/03_model_rf.ipynb)
- 5-fold 교차검증 및 F1 스코어 측정

## 관련 이슈
closes #7

## 리뷰 요청 사항
- seed 고정 방법이 올바른지 확인 부탁드립니다.
```

---

## 11. 자주 발생하는 문제 해결

### 충돌(Conflict)이 발생했을 때

```bash
git pull origin main
# CONFLICT 메시지가 뜨면 해당 파일을 열어 아래와 같은 부분을 찾습니다:

<<<<<<< HEAD
내 코드
=======
상대방 코드
>>>>>>> origin/main
```

1. `<<<<<<<`, `=======`, `>>>>>>>` 표시를 모두 지우고 최종 코드를 남깁니다.
2. `git add <파일명>` 후 `git commit` 으로 충돌 해결을 완료합니다.

### 잘못된 커밋 메시지를 수정하고 싶을 때 (push 전)

```bash
git commit --amend -m "새 메시지"
```

### 실수로 잘못된 파일을 add했을 때

```bash
git restore --staged <파일명>   # 스테이징에서만 제거 (파일 내용 유지)
```

### 변경사항을 되돌리고 싶을 때 (커밋 전)

```bash
git restore <파일명>   # 마지막 커밋 상태로 되돌림 (주의: 변경사항 삭제됨)
```

### `.ipynb` 파일이 너무 커서 push가 안 될 때

Jupyter 노트북은 실행 결과(output)까지 저장되어 파일이 커질 수 있습니다.

```bash
# 노트북 output 초기화 후 커밋
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

또는 Jupyter에서 `Kernel → Restart & Clear Output` 후 저장하세요.

---

## 12. 추가 학습 자료

| 자료 | 링크 | 특징 |
|------|------|------|
| Pro Git Book (한국어) | [https://git-scm.com/book/ko/v2](https://git-scm.com/book/ko/v2) | 공식 무료 전자책, 가장 체계적 |
| GitHub 공식 문서 | [https://docs.github.com/ko](https://docs.github.com/ko) | 한국어 지원, 실습 포함 |
| GitHub Skills | [https://skills.github.com](https://skills.github.com) | GitHub에서 만든 실습 코스 (영어) |
| Git 시각화 도구 | [https://learngitbranching.js.org/?locale=ko](https://learngitbranching.js.org/?locale=ko) | 브랜치 개념을 시각적으로 학습 (한국어) |
| Atlassian Git 튜토리얼 | [https://www.atlassian.com/ko/git/tutorials](https://www.atlassian.com/ko/git/tutorials) | 단계별 튜토리얼, 그림 풍부 |

### 추천 학습 순서 (Git 처음이라면)

1. [learngitbranching.js.org](https://learngitbranching.js.org/?locale=ko) – 브랜치 시각화로 기초 감잡기 (30분)
2. [GitHub Skills – Introduction to GitHub](https://github.com/skills/introduction-to-github) – 실제 저장소로 실습 (1시간)
3. 이 가이드의 [팀 협업 워크플로우](#6-팀-협업-워크플로우) 실습

---

> 💬 Git 사용 중 막히는 부분이 있으면 이슈를 열거나 강의 채널에 질문해 주세요!
