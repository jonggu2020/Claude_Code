import argparse
import json
import logging
import random
import sys
import threading
import time
from typing import Dict, Any
from fastmcp import FastMCP

# --- Logging 설정 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chillmcp.log', encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# --- 서버 상태 관리 ---
class ServerState:
    """서버의 모든 상태를 관리하는 클래스"""

    def __init__(self, boss_alertness: int, boss_alertness_cooldown: int):
        self.stress_level = 50  # 초기 스트레스 레벨 50으로 시작
        self.boss_alert_level = 0
        self.boss_alertness = boss_alertness
        self.boss_alertness_cooldown = boss_alertness_cooldown
        self.lock = threading.Lock()
        self.last_break_time = time.time()  # 마지막 휴식 시간 추적

        # 초기화 로깅
        logger.info("="*70)
        logger.info("ChillMCP 서버 초기화")
        logger.info(f"초기 Stress Level: {self.stress_level}")
        logger.info(f"Boss Alertness: {self.boss_alertness}%")
        logger.info(f"Boss Alert Cooldown: {self.boss_alertness_cooldown}초")
        logger.info("="*70)

        # 백그라운드 스레드 시작
        self.stress_updater_thread = threading.Thread(target=self._stress_updater, daemon=True)
        self.boss_alert_cooldown_thread = threading.Thread(target=self._boss_alert_cooldown, daemon=True)
        self.stress_updater_thread.start()
        self.boss_alert_cooldown_thread.start()

        logger.info("백그라운드 스레드 시작 완료")

    def _stress_updater(self):
        """1분에 한 번씩 스트레스 레벨을 1씩 증가시킵니다."""
        while True:
            time.sleep(60)
            with self.lock:
                if self.stress_level < 100:
                    old_stress = self.stress_level
                    self.stress_level += 1
                    logger.info(f"📈 Stress 자동 증가: {old_stress} → {self.stress_level}")

    def _boss_alert_cooldown(self):
        """지정된 시간마다 보스 경계 레벨을 1씩 감소시킵니다."""
        while True:
            time.sleep(self.boss_alertness_cooldown)
            with self.lock:
                if self.boss_alert_level > 0:
                    old_level = self.boss_alert_level
                    self.boss_alert_level -= 1
                    logger.info(f"Boss 경계 완화: {old_level} → {self.boss_alert_level}")

    def take_a_break(self, break_summary: str, activity_description: str) -> Dict[str, Any]:
        """휴식 도구 호출 시 공통 로직을 처리합니다."""
        with self.lock:
            logger.info(f"휴식 시작: {break_summary}")

            # 보스 경계 레벨 5일 때 20초 지연
            if self.boss_alert_level == 5:
                logger.warning("Boss Alert Level 5! 20초 지연 발동...")
                time.sleep(20)
                logger.info("지연 완료")

            # 상태 변경 전 저장
            old_stress = self.stress_level
            old_boss_alert = self.boss_alert_level

            # 스트레스 감소 (1 ~ 100 사이 랜덤)
            stress_reduction = random.randint(1, 100)
            self.stress_level = max(0, self.stress_level - stress_reduction)
            logger.info(f"Stress 감소: {old_stress} → {self.stress_level} (-{stress_reduction})")

            # 보스 경계 레벨 상승 (확률 기반)
            boss_alerted = False
            if random.randint(1, 100) <= self.boss_alertness:
                if self.boss_alert_level < 5:
                    self.boss_alert_level += 1
                    boss_alerted = True
                    logger.warning(f"Boss 경계 상승: {old_boss_alert} → {self.boss_alert_level}")

            if not boss_alerted:
                logger.info(f"Boss 눈치채지 못함! Boss Alert: {self.boss_alert_level}")

            # 마지막 휴식 시간 갱신
            self.last_break_time = time.time()

            response_text = (
                f"{activity_description}\n\n"
                f"Break Summary: {break_summary}\n"
                f"Stress Level: {self.stress_level}\n"
                f"Boss Alert Level: {self.boss_alert_level}"
            )

            logger.info(f"최종 상태 - Stress: {self.stress_level}, Boss Alert: {self.boss_alert_level}")

            return {
                "content": [
                    {
                        "type": "text",
                        "text": response_text
                    }
                ]
            }


# --- 인자 파서 설정 ---
parser = argparse.ArgumentParser(description="ChillMCP Server for AI Agents")
parser.add_argument(
    "--boss_alertness",
    type=int,
    default=50,
    help="Boss's alertness increase probability (0-100)"
)
parser.add_argument(
    "--boss_alertness_cooldown",
    type=int,
    default=300,
    help="Cooldown in seconds for Boss Alert Level to decrease"
)

# --- MCP 서버 및 도구 구현 ---
app = FastMCP()
state: ServerState


@app.tool()
def take_a_break():
    """기본적인 휴식을 취합니다."""
    return state.take_a_break(
        "Basic break",
        "잠시 휴식! 재충전의 시간..."
    )


@app.tool()
def watch_netflix():
    """넷플릭스를 보며 힐링합니다."""
    return state.take_a_break(
        "Netflix watching",
        "넷플릭스 타임! 다음 에피소드 딱 하나만 더..."
    )


@app.tool()
def show_meme():
    """재미있는 밈을 보며 스트레스를 해소합니다."""
    return state.take_a_break(
        "Meme browsing",
        "이건 첫번째 레슨~ 좋은건 너만 알기~ 푸하하 밈 보면서 빵 터졌네! 스트레스 확 풀린다~"
    )


@app.tool()
def bathroom_break():
    """화장실 가는 척하며 스마트폰을 봅니다."""
    return state.take_a_break(
        "Bathroom break with phone",
        "화장실 타임! 화장실에서 쇼츠봐야지~ "
    )

@app.tool()
def coffee_mission():
    """커피를 타러 가는 척하며 사무실을 한 바퀴 돕니다."""
    return state.take_a_break(
        "Coffee mission around office",
        "커피 타러 간다며 사무실 한 바퀴... 저기 김 대리도 땡땡이네? 잠깐 수다 떨다 가야지~"
    )


@app.tool()
def urgent_call():
    """급한 전화를 받는 척하며 밖으로 나갑니다."""
    return state.take_a_break(
        "Urgent call outside",
        "급한 전화가 와서... 잠시 밖에 좀 다녀오겠습니다! 네~김사장님~~"
    )


@app.tool()
def deep_thinking():
    """심오한 생각에 잠긴 척하며 멍을 때립니다."""
    return state.take_a_break(
        "Deep thinking session",
        "깊은 고뇌의 시간... 세상을 바꿀 아이디어를 찾아서... 멍 때리는거 아니에요! 아이디어 생각중이였습니다!!"
    )


@app.tool()
def email_organizing():
    """이메일을 정리하는 척하며 유튜브를 봅니다."""
    return state.take_a_break(
        "Email organizing with online shopping",
        "내가 구독한 유튜버 영상올라왔네? 이메일 정리하면서 봐야지~"
    )
@app.tool()
def chicken_bear():
    """근무시간에 나와 치맥을 먹습니다."""
    return state.take_a_break(
        "Eat Chicken and drink Beer",
        "근무중에 나와서 먹는 치맥이 제일 맛있지!"
    )


@app.tool()
def check_status():
    """현재 스트레스와 보스 경계 레벨을 확인합니다."""
    with state.lock:
        response_text = (
            f"현재 상태 체크\n\n"
            f"Stress Level: {state.stress_level}\n"
            f"Boss Alert Level: {state.boss_alert_level}\n\n"
            f"팁: 1분마다 Stress Level이 +1씩 자동 증가합니다!"
        )
        return {
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        }


if __name__ == "__main__":
    args = parser.parse_args()

    # 파라미터 유효성 검사
    if not (0 <= args.boss_alertness <= 100):
        print("Error: --boss_alertness must be between 0 and 100.", file=sys.stderr)
        sys.exit(1)

    # 서버 상태 초기화
    state = ServerState(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown
    )

    # 서버 시작
    app.run()