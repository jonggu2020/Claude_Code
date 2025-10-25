# ChillMCP 서버 분석 리포트
이 문서는 제공된 `main.py` 파일의 MCP 기능, 상태 관리 로직 및 자동 검증 시스템을 통한 테스트 결과를 요약합니다.
## 1. 🎯 MCP 기능 (Tools)
`main.py`는 `FastMCP`를 기반으로 하며, 모든 휴식/농땡이 도구는 `handle_chill_tool`이라는 중앙 핸들러를 통해 관리됩니다.

**제공되는 도구 목록:**
* `take_a_break`: 기본 휴식 (멍때리기)
* `watch_netflix`: 넷플릭스 시청
* `show_meme`: 재밌는 밈 보기
* `bathroom_break`: 화장실 가기 (힐링 공간)
* `coffee_mission`: 커피 사러 가기
* `urgent_call`: 급한 전화 받는 척하기
* `deep_thinking`: 점심 메뉴 고민 (심각한 척)
* `email_organizing`: 이메일 정리 (쇼핑)
* `chicken_beer`: 치맥하러 나가기

**주요 특징:**
* **창의적 응답**: 각 도구는 3가지의 재치 있는 한글 메시지와 영문 요약(Break Summary) 중 하나를 랜덤으로 반환합니다. (예: "🚽 화장실은 나만의 힐링 공간... 스마트폰은 필수템").
* **코드 품질**: 중앙 핸들러(`handle_chill_tool`)를 사용하여 코드 중복을 제거하고(DRY 원칙 준수) 로깅 시스템을 완비했습니다.

---
## 2. 상태 변화 로직 (State Management)
서버는 `stress_level` (스트레스)과 `boss_alert_level` (상사 경계) 두 가지 핵심 상태를 관리합니다.
### Stress Level (0-100)
* **자동 증가**: 60초마다 1포인트씩 자동으로 증가합니다 (최대 100).
* **도구 사용 시 감소**: MCP 도구 호출 시 1~100 사이의 랜덤 값만큼 즉시 감소합니다 (최소 0).

### Boss Alert Level (0-5)
* **도구 사용 시 증가**:
    * 도구 호출 시 확률적으로 1포인트 증가합니다 (최대 5).
    * 이 확률은 `--boss_alertness` 파라미터(기본값 50%)로 제어됩니다. (예: 100% 설정 시 항상 증가).
* **자동 감소**:
    * `--boss_alertness_cooldown` 파라미터(기본값 300초)에 설정된 시간마다 1포인트씩 자동으로 감소합니다 (최소 0).
* **패널티**:
    * `boss_alert_level`이 5에 도달하면, 도구 호출 시 5초의 지연(Penalty)이 발생합니다.
    * *참고: `Test.md`와 `README.md`의 요구사항은 20초였으나, `main.py` 파일에는 "타임아웃 방지" 목적으로 5초로 수정되어 있습니다.*

---

### 3. 필수 검증 결과

* **커맨드라인 파라미터**: `--boss_alertness` 및 `--boss_alertness_cooldown` 파라미터 인식 및 로직 적용 100% 통과.
* **정규표현식 파싱**: `Break Summary`, `Stress Level`, `Boss Alert Level` 필드 모두 100% 파싱 성공.
* **`boss_alertness=100` 시나리오**: 100% 확률로 Boss Alert가 증가하는 확률 로직 완벽 구현.

---

## 4. 설치 및 실행 방법

### 1. 사전 요구사항

이 프로젝트를 실행하기 위해서는 로컬 컴퓨터에 **Python 3.11**이 설치되어 있어야 합니다.

* **Python 3.11 설치 확인 (Windows)**
    ```bash
    py -3.11 --version
    ```
### 2. 설치 및 설정

**가상환경 생성**
```bash
py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```