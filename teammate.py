import pandas as pd
from collections import defaultdict, Counter
import math

# -----------------------------
# 1. 엑셀 로딩
# -----------------------------
FILE_PATH = "/Users/songhune/Downloads/[2026-1]기계학습기초 팀배정 사전설문지(응답).xlsx"
SHEET_NAME = "설문지 응답 시트1"  # 파일 구조 기준[file:1]

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

# 컬럼 이름은 실제 엑셀 헤더와 맞춰야 함[file:1]
COL_STUDENT_ID = "학번"
COL_MAJOR = "소속학과(전공)"
COL_PYTHON = "현재 시점에서, 본인의 파이썬 사용 경험을 스스로 평가해 주세요."
COL_GIT = "git/github사용 경험을 스스로 평가해 주세요 (1: 사용해 본 적 없음, 3: clone/commit/push 가능, 5: branch/PR/merge까지 익숙함)"
COL_ML = "현재 시점에서, 기계학습 모델 학습 및 평가 경험을 스스로 평가해 주세요."
COL_TEAMLOAD = "이번 학기 본 수업 외에 팀 프로젝트가 있는 과목 수"
COL_TIMES = "팀 프로젝트 미팅이 어려운 시간대를 모두 선택해 주세요."
COL_WISHLIST = "가능하다면 함께 하고 싶은 팀원이 있나요? (이름이 아니라 학번으로만 적어 주세요. 최대 2명까지)"

# -----------------------------
# 2. 학생 구조 만들기
# -----------------------------
students = []

def parse_teamload(x):
    # 예: "2개", "3개 이상" 같은 문자열을 정수로 단순화[file:1]
    if isinstance(x, str):
        if "3개 이상" in x:
            return 3
        digits = "".join(ch for ch in x if ch.isdigit())
        return int(digits) if digits else 0
    if pd.isna(x):
        return 0
    return int(x)

def parse_times(x):
    # "평일 오전, 평일 오후, 주말 저녁" 같은 문자열을 리스트로[file:1]
    if not isinstance(x, str):
        return []
    return [t.strip() for t in x.split(",") if t.strip()]

def parse_wishlist(x):
    # "202127180, 2022xxxx" 같은 학번 문자열을 리스트로 파싱[file:1]
    if not isinstance(x, str):
        return []
    parts = [p.strip() for p in x.replace(" ", "").split(",") if p.strip()]
    # 숫자만 남기거나, 그대로 문자열 학번으로 사용
    return parts

for _, row in df.iterrows():
    sid = str(row[COL_STUDENT_ID]).strip()
    major = str(row[COL_MAJOR]).strip()
    try:
        python_score = float(row[COL_PYTHON])
    except Exception:
        python_score = 0.0
    try:
        git_score = float(row[COL_GIT])
    except Exception:
        git_score = 0.0
    try:
        ml_score = float(row[COL_ML])
    except Exception:
        ml_score = 0.0

    teamload = parse_teamload(row[COL_TEAMLOAD])
    times = parse_times(row[COL_TIMES])
    wishlist = parse_wishlist(row.get(COL_WISHLIST, ""))

    skill_score = 0.4 * python_score + 0.3 * git_score + 0.3 * ml_score
    alpha = 0.3
    adjusted_score = skill_score - alpha * teamload

    students.append({
        "id": sid,
        "major": major,
        "python": python_score,
        "git": git_score,
        "ml": ml_score,
        "teamload": teamload,
        "times": times,
        "wishlist": wishlist,
        "skill_score": skill_score,
        "adjusted_score": adjusted_score,
    })

# 총 인원 확인
N = len(students)
TEAM_SIZE = 4
NUM_TEAMS = math.ceil(N / TEAM_SIZE)

print(f"총 인원: {N}, 팀 수: {NUM_TEAMS}")

# -----------------------------
# 3. 상/중/하 구간 나누기
# -----------------------------
students_sorted = sorted(students, key=lambda s: s["adjusted_score"], reverse=True)

# 단순 비율: 상위 25%, 하위 25%, 나머지 중간 (모래시계형이면 상/하가 더 많을 수 있음)
n_high = max(1, int(0.25 * N))
n_low = max(1, int(0.25 * N))

for i, s in enumerate(students_sorted):
    if i < n_high:
        s["level"] = "high"
    elif i >= N - n_low:
        s["level"] = "low"
    else:
        s["level"] = "mid"

# id -> student 매핑
id2student = {s["id"]: s for s in students_sorted}

# -----------------------------
# 4. 희망 팀원 관계 정리 (큐/스택)
# -----------------------------
strong_pairs = []  # 서로 희망
weak_pairs = []    # 한쪽만 희망

# 학번별 wishlist 집계
wish_map = defaultdict(set)  # a -> {b1, b2}
for s in students_sorted:
    for w in s["wishlist"]:
        wish_map[s["id"]].add(w)

# strong / weak 판별
paired = set()
for a, ws in wish_map.items():
    for b in ws:
        if b not in id2student:
            continue
        # a < b 조건으로 중복 방지
        if (b in wish_map and a in wish_map[b]) and (a < b):
            strong_pairs.append((a, b))
            paired.add(a); paired.add(b)

# weak: strong에 포함되지 않은 단방향
for a, ws in wish_map.items():
    for b in ws:
        if b not in id2student:
            continue
        if (a, b) in strong_pairs or (b, a) in strong_pairs:
            continue
        # 양방향이 아닌 경우 weak
        weak_pairs.append((a, b))

# -----------------------------
# 5. 팀 상태 구조
# -----------------------------
teams = []
for t in range(NUM_TEAMS):
    teams.append({
        "name": f"{t+1}조",
        "members": [],
        "skill_sum": 0.0,
        "high": 0,
        "mid": 0,
        "low": 0,
        "majors": Counter(),
        "times": Counter(),  # 어려운 시간대 카운트
    })

assigned = set()  # 배정된 학번

def can_add_member(team, student):
    """기본 제약: 인원 4명 이하, high/mid/low 과도 몰림 방지."""
    if len(team["members"]) >= TEAM_SIZE:
        return False

    # level 제한 (예: low 3명 이상 금지, high 2명 이상 금지 등)
    lvl = student["level"]
    high = team["high"]
    mid = team["mid"]
    low = team["low"]

    if lvl == "high" and high >= 1:
        # 리더는 팀당 1명 정도로 제한
        return False
    if lvl == "low" and low >= 2:
        # low는 2명까지
        return False

    return True

def score_team_for_student(team, student, mate=None):
    """
    팀에 student (또는 student+mate)를 넣었을 때의 점수 계산.
    전공, 희망 매칭, skill 균형, level 분포, 시간 제약 반영.
    """
    # 가중치
    w_major = 3.0
    w_wish = 4.0
    w_skill = 2.0
    w_level = 1.5
    w_time = 1.0

    added = [student]
    if mate is not None:
        added.append(mate)

    # 인원 제약 먼저 체크
    if len(team["members"]) + len(added) > TEAM_SIZE:
        return -1e9  # 불가능

    # high/low 제약 체크
    high = team["high"]
    mid = team["mid"]
    low = team["low"]
    for s in added:
        if s["level"] == "high" and high >= 1:
            return -1e9
        if s["level"] == "low" and low >= 2:
            return -1e9
        # 가상 update
        if s["level"] == "high":
            high += 1
        elif s["level"] == "mid":
            mid += 1
        else:
            low += 1

    # 1) 전공 스코어
    # 같은 전공이 많을수록 가산점, 단 3명 이상이면 감점
    major_score = 0.0
    for s in added:
        m = s["major"]
        current = team["majors"][m]
        major_score += (1 + current)  # 같은 전공 있을수록++
        if current + 1 >= 3:
            major_score -= 1.5  # 과도 집중 패널티

    # 2) 희망 매칭 스코어
    wish_score = 0.0
    for s in added:
        sid = s["id"]
        # 이미 이 팀에 s가 희망하는 사람이 있는지
        for w in s["wishlist"]:
            if w in team["members"]:
                wish_score += 2.0
    # strong-pair가 같이 들어가는 경우 추가 가산
    if mate is not None:
        sid_a, sid_b = student["id"], mate["id"]
        if (sid_a, sid_b) in strong_pairs or (sid_b, sid_a) in strong_pairs:
            wish_score += 3.0

    # 3) skill 균형 스코어
    total_skill = team["skill_sum"] + sum(s["skill_score"] for s in added)
    future_size = len(team["members"]) + len(added)
    # 팀 평균 skill이 전체 평균에 가까울수록 좋게
    global_avg = sum(s["skill_score"] for s in students_sorted) / N
    future_avg = total_skill / future_size
    skill_score_term = -abs(future_avg - global_avg)

    # 4) level 분포 스코어 (상1, 중/하 과몰 방지)
    level_score = 0.0
    # high 1명 확보 상태면 보너스
    if high == 1:
        level_score += 1.0
    # low가 0~2 범위에 있으면 약간 보너스
    if 0 <= low <= 2:
        level_score += 0.5

    # 5) 시간 제약 스코어 (충돌 최소화)
    time_score = 0.0
    for s in added:
        for tslot in s["times"]:
            # 이미 이 시간대가 어려운 사람이 많으면 패널티
            time_score -= 0.2 * team["times"][tslot]

    total_score = (
        w_major * major_score +
        w_wish * wish_score +
        w_skill * skill_score_term +
        w_level * level_score +
        w_time * time_score
    )
    return total_score

def add_to_team(team, student):
    team["members"].append(student["id"])
    team["skill_sum"] += student["skill_score"]
    if student["level"] == "high":
        team["high"] += 1
    elif student["level"] == "mid":
        team["mid"] += 1
    else:
        team["low"] += 1
    team["majors"][student["major"]] += 1
    for tslot in student["times"]:
        team["times"][tslot] += 1
    assigned.add(student["id"])

# -----------------------------
# 6. 리더(상위 그룹) 먼저 배정
# -----------------------------
high_students = [s for s in students_sorted if s["level"] == "high"]
others = [s for s in students_sorted if s["level"] != "high"]

# high 학생을 팀에 한 명씩 배정 (전공 고려)
for s in high_students:
    best_team = None
    best_score = -1e9
    for team in teams:
        if len(team["members"]) >= TEAM_SIZE:
            continue
        # high는 team에 아직 없을 때만
        if team["high"] >= 1:
            continue
        sc = score_team_for_student(team, s)
        if sc > best_score:
            best_score = sc
            best_team = team
    if best_team is None:
        # 어쩔 수 없이 아무 팀이나 (제약 느슨하게)
        best_team = min(teams, key=lambda tm: len(tm["members"]))
    add_to_team(best_team, s)

# -----------------------------
# 7. 나머지 학생 배정 (pair 우선, 그 다음 single)
# -----------------------------
def get_unassigned_student_by_id(sid):
    if sid in assigned:
        return None
    return id2student.get(sid)

# strong pair 먼저
for a, b in strong_pairs:
    sa = get_unassigned_student_by_id(a)
    sb = get_unassigned_student_by_id(b)
    if sa is None or sb is None:
        continue

    best_team = None
    best_score = -1e9
    for team in teams:
        sc = score_team_for_student(team, sa, sb)
        if sc > best_score:
            best_score = sc
            best_team = team

    if best_team is not None and best_score > -1e8:
        add_to_team(best_team, sa)
        add_to_team(best_team, sb)

# weak pair (한쪽만 희망)
for a, b in weak_pairs:
    sa = get_unassigned_student_by_id(a)
    sb = get_unassigned_student_by_id(b)
    # 일단 희망을 낸 쪽(sa)을 중심으로 처리
    if sa is None:
        continue

    # 둘 다 미배정이면 같이 넣는 것 시도
    if sb is not None:
        best_team = None
        best_score = -1e9
        for team in teams:
            sc = score_team_for_student(team, sa, sb)
            if sc > best_score:
                best_score = sc
                best_team = team
        if best_team is not None and best_score > -1e8:
            add_to_team(best_team, sa)
            add_to_team(best_team, sb)
            continue

    # 같이 못 넣으면 sa만 단독으로 배정
    best_team = None
    best_score = -1e9
    for team in teams:
        sc = score_team_for_student(team, sa)
        if sc > best_score:
            best_score = sc
            best_team = team
    if best_team is not None and best_score > -1e8:
        add_to_team(best_team, sa)

# 남은 학생들(single 처리)
for s in students_sorted:
    if s["id"] in assigned:
        continue
    best_team = None
    best_score = -1e9
    for team in teams:
        sc = score_team_for_student(team, s)
        if sc > best_score:
            best_score = sc
            best_team = team
    if best_team is None:
        # fallback: 인원 적은 팀
        best_team = min(teams, key=lambda tm: len(tm["members"]))
    add_to_team(best_team, s)

# -----------------------------
# 8. 결과 출력
# -----------------------------
for team in teams:
    print("====", team["name"], "====")
    print("인원:", len(team["members"]),
          "skill_sum:", round(team["skill_sum"], 2),
          "high/mid/low:", team["high"], team["mid"], team["low"])
    print("전공 분포:", dict(team["majors"]))
    print("멤버 학번:", ", ".join(team["members"]))
    print()