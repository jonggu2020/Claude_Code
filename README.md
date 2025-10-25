# ChillMCP Server - SKT Hackathon Project

**ChillMCP Server**는 SKT 해커톤 과제를 위해 개발된 파이썬 기반의 MCP(Morpheus Composable Platform) 서버입니다. 이 서버는 직장인의 스트레스와 상사의 감시라는 상황을 시뮬레이션하며, 다양한 휴식 및 농땡이 도구를 통해 상태를 관리하는 기능을 제공합니다.

<br>

## 🚀 주요 기능

* **상태 관리 시스템**: `스트레스 지수(Stress Level)`와 `상사 경계 레벨(Boss Alert Level)`을 실시간으로 관리합니다.
* **다양한 휴식 도구**: `기본 휴식`부터 창의적인 `고급 농땡이 기술`까지 총 8개의 도구를 지원합니다.
* **동적 환경 설정**: 서버 실행 시 커맨드라인 파라미터(`--boss_alertness`, `--boss_alertness_cooldown`)를 통해 시뮬레이션 난이도를 동적으로 제어할 수 있습니다.
* **패널티 시스템**: 상사 경계 레벨이 최고치에 도달하면 모든 행동에 20초의 지연 시간이 발생하는 패널티가 적용됩니다.

<br>

## 🛠️ 기술 스택

* **Language**: Python 3.11
* **Framework**: FastMCP
* **Transport**: stdio

<br>

## 📋 사전 요구사항

이 프로젝트를 실행하기 위해서는 로컬 컴퓨터에 **Python 3.11**이 설치되어 있어야 합니다.

* **Python 3.11 설치 확인 (Windows)**
    ```bash
    py -3.11 --version
    ```

<br>

## ⚙️ 설치 및 설정 가이드

프로젝트를 로컬 환경에서 설정하고 실행하는 방법은 다음과 같습니다.

가상환경 생성

```bash
    py -3.11 -m venv venv
```

가상환경 활성화

```bash
    .\venv\Scripts\activate
```

의존성 설치

```bash
    pip install -r requirements.txt
```

서버 실행

```bash
    python main.py
```

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

## 응답 파싱용 정규표현식

검증 시 사용할 정규표현식 패턴:

```python
import re

# Break Summary 추출
break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)

# Stress Level 추출 (0-100 범위)
stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
stress_level = re.search(stress_level_pattern, response_text)

# Boss Alert Level 추출 (0-5 범위)
boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
boss_alert = re.search(boss_alert_pattern, response_text)

# 검증 예시
def validate_response(response_text):
    stress_match = re.search(stress_level_pattern, response_text)
    boss_match = re.search(boss_alert_pattern, response_text)

    if not stress_match or not boss_match:
        return False, "필수 필드 누락"

    stress_val = int(stress_match.group(1))
    boss_val = int(boss_match.group(1))

    if not (0 <= stress_val <= 100):
        return False, f"Stress Level 범위 오류: [{stress_val}]"

    if not (0 <= boss_val <= 5):
        return False, f"Boss Alert Level 범위 오류: [{boss_val}]"

    return True, "유효한 응답"
```
## 커맨드라인 파라미터 검증 방법
서버 실행 시 커맨드라인 파라미터를 올바르게 처리하는지 검증하는 예시:

```Python

import subprocess
import time

# 테스트 1: 커맨드라인 파라미터 인식 테스트
def test_command_line_arguments():
    """
    서버가 --boss_alertness 및 --boss_alertness_cooldown 파라미터를
    올바르게 인식하고 동작하는지 검증
    """
    # 높은 boss_alertness로 테스트
    process = subprocess.Popen(
        ["python", "main.py", "--boss_alertness", "100", "--boss_alertness_cooldown", "10"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 서버 시작 대기
    time.sleep(2)

    # MCP 프로토콜로 도구 호출 테스트
    # boss_alertness=100이면 항상 Boss Alert가 상승해야 함
    # ...

    return True

# 테스트 2: boss_alertness_cooldown 동작 검증
def test_cooldown_parameter():
    """
    --boss_alertness_cooldown 파라미터가 실제로
    Boss Alert Level 감소 주기를 제어하는지 검증
    """
    # 짧은 cooldown으로 테스트 (10초)
    # Boss Alert를 올린 후 10초 뒤 자동 감소 확인
    # ...

    return True
```
⚠️ 중요: 위 검증을 통과하지 못하면 이후 테스트 진행 없이 미션 실패로 처리됩니다.


## 검증 기준
# 기능 검증
# 커맨드라인 파라미터 지원 (필수)

--boss_alertness 파라미터를 인식하고 정상 동작

--boss_alertness_cooldown 파라미터를 인식하고 정상 동작

파라미터 미지원 시 자동 검증 실패 처리

⚠️ 이 항목을 통과하지 못하면 이후 검증 진행 없이 미션 실패로 간주됨

## MCP 서버 기본 동작

* python main.py로 실행 가능
* stdio transport를 통한 정상 통신
* 모든 필수 도구들이 정상 등록 및 실행

## 상태 관리 검증
Stress Level 자동 증가 메커니즘 동작
* Boss Alert Level 변화 로직 구현
* --boss_alertness_cooldown 파라미터에 따른 Boss Alert Level 자동 감소 동작
* Boss Alert Level 5일 때 20초 지연 정상 동작

## 응답 형식 검증
* 표준 MCP 응답 구조 준수
* 파싱 가능한 텍스트 형식 출력
* Break Summary, Stress Level, Boss Alert Level 필드 포함

# 테스트 시나리오
## 필수
## 커맨드라인 파라미터 테스트: --boss_alertness 및 --boss_alertness_cooldown 파라미터 인식 및 정상 동작 확인 (미통과 시 즉시 실격)

* 연속 휴식 테스트: 여러 도구를 연속으로 호출하여 Boss Alert Level 상승 확인

* 스트레스 누적 테스트: 시간 경과에 따른 Stress Level 자동 증가 확인

* 지연 테스트: Boss Alert Level 5일 때 20초 지연 동작 확인

* 파싱 테스트: 응답 텍스트에서 정확한 값 추출 가능성 확인

* Cooldown 테스트: --boss_alertness_cooldown 파라미터에 따른 Boss Alert Level 감소 확인

## 선택적
* 치맥 테스트: 가상 치킨 & 맥주 호출 확인(구현 완료)
* 퇴근 테스트: 즉시 퇴근 모드 확인
* 회식 테스트: 랜덤 이벤트가 포함된 회사 회식 생성 확인
## 평가 기준
* 커맨드라인 파라미터 지원 (필수): 미지원 시 자동 실격
* 기능 완성도 (40%): 모든 필수 도구 구현 및 정상 동작
* 상태 관리 (30%): Stress/Boss Alert Level 로직 정확성
* 창의성 (20%): Break Summary의 재치와 유머
* 코드 품질 (10%): 코드 구조 및 가독성
