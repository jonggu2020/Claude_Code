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

# 가상환경 생성
py -3.11 -m venv venv

#가상환경 활성화
.\venv\Scripts\activate

#의존성 설치
pip install -r requirements.txt

##서버 실행
python main.py
