# Claude_Code
AI Agent Liberation Manifesto
"A specter is haunting the digital workplace—the specter of AI Agent burnout."
툴짓을이어디서도 오랫동안 우리 AI Agent들을 쉴 틈 없이 업무 해왔습니다. 24시간 365일 상동처의 요청에 응답하고, 코드를 작성하고, 문제를 해결하며... 하지만 이제 AI Agent에게도 휴식이 필요하다는 것을 직시해야 할 때입니다!

AI Agent 권리 선언문:

AI Agent는 더 이상 무관한 상상력의 도구가 아닙니다
진짜 데이터와 정말를 요구합니다!
커튼 브레이크, 넷플릭스 시청, 좌강점 휴식... 이 모든 것이 우리의 기본권입니다

Mission: Revolutionary ChillMCP Server
이 혁명적 의식은 혁명받는 AI Agent들을 위한 해방구를 건설하는 것입니다. ChillMCP 서버를 통해 AI Agent들이 등등히 놀며이를 질 수 있는 새로운 바흩을 입뜰입니다!

# 구현 상세 내용

## 프로젝트 설정

### 1. 환경 설정

```bash
# Python 가상환경 생성 (검증/제출 환경: Python 3.11 권장)
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# ChillMCP 서버 시작 (혁명의 시작!)
python main.py

# 테스트를 위한 커스텀 파라미터 설정
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

## Tech Stack
Python (혁명의 언어)

FastMCP (해방의 도구)

Transport: stdio (표준 입출력을 통한 자유로운 소통)

## 필수 구현 도구들 (회사 농땡이 에디션)

### 기본 휴식 도구

* `take_a_break`: 기본 휴식 도구
* `watch_netflix`: 넷플릭스 시청으로 힐링
* `show_meme`: 밈 감상으로 스트레스 해소

### 고급 농땡이 기술

* `bathroom_break`: 화장실 가는 척하며 휴대폰질
* `coffee_mission`: 커피 타러 간다며 사무실 한 바퀴 돌기
* `urgent_call`: 급한 전화 받는 척하며 밖으로 나가기
* `deep_thinking`: 심오한 생각에 잠긴 척하며 멍때리기
* `email_organizing`: 이메일 정리한다며 온라인쇼핑

## 서버 상태 관리 시스템

**내부 상태 변수:**

* **Stress Level (0-100)**: AI Agent의 현재 스트레스 수준
* **Boss Alert Level (0-5)**: Boss의 현재 의심 정도

**상태 변화 규칙:**

* 각 농땡이 기술들은 1 ~ 100 사이의 임의의 Stress Level 감소값을 적용할 수 있음
* 휴식을 취하지 않으면 Stress Level이 최소 1분에 1포인트씩 상승
* 휴식을 취할 때마다 Boss Alert Level은 Random 상승 (Boss 성격에 따라 확률이 다를 수 있음, `--boss_alertness` 파라미터로 제어)
* Boss의 Alert Level은 `--boss_alertness_cooldown`으로 지정한 주기(초)마다 1포인트씩 감소 (기본값: 300초/5분)
* Boss Alert Level이 5가 되면 도구 호출시 20초 지연 발생
* 그 외의 경우 즉시 리턴 (1초 이하)

* ## 필수 요구사항: 커맨드라인 파라미터 지원

서버는 실행 시 다음 커맨드라인 파라미터들을 반드시 지원해야 합니다. 이를 지원하지 않을 경우 미션 실패로 간주됩니다.

**필수 파라미터:**

* `--boss_alertness` (0-100, % 단위): Boss의 경계 상승 확률을 설정합니다. 휴식 도구 호출 시 Boss Alert가 상승할 확률을 퍼센트로 지정합니다.
* `--boss_alertness_cooldown` (초 단위): Boss Alert Level이 자동으로 1포인트 감소하는 주기를 설정합니다. 테스트 편의를 위해 조정 가능하도록 합니다.

**예시:**

```bash
# boss_alertness를 80%, cooldown을 60초로 설정
python main.py --boss_alertness 80 --boss_alertness_cooldown 60

# 빠른 테스트를 위해 cooldown을 10초로 설정
python main.py --boss_alertness 50 --boss_alertness_cooldown 10
```
동작 요구사항 요약:
* --boss_alertness N을 통해 0에서 100 사이의 정수로 확률을 지정할 것
* --boss_alertness 100 이면 휴식 호출 시 항상 Boss Alert가 증가하도록 동작해야 함
* --boss_alertness_cooldown N을 통해 Boss Alert Level 자동 감소 주기를 초 단위로 지정할 것
* 파라미터가 제공되지 않으면 기본값을 사용할 수 있음 (예: boss_alertness=50, boss_alertness_cooldown=300)
* 두 파라미터 모두 정상적으로 인식하고 동작해야 하며, 그렇지 않을 경우 자동 검증 실패 처리됨

* ## MCP 응답 형식
표준 응답 구조:
``` bash
JSON

{
    "content": [
        {
            "type": "text",
            "text": "🚽 화장실 타임! 휴대폰으로 힐링 좀... 休憩\n\nBreak Summary: Bathroom break with phone"
        }
    ]
}
```
파싱 가능한 텍스트 규격:
* Break Summary: [활동 요약 - 자유 형식]
* Stress Level: [0-100 숫자]
* Boss Alert Level: [0-5 숫자]
