import argparse
import time
import random
import threading
from fastmcp import FastMCP

# --- 1. 서버 상태 관리 ---
server_state = {
    "stress_level": 0,
    "boss_alert_level": 0,
}
state_lock = threading.Lock()

# --- 2. [필수] 커맨드라인 파라미터 설정 ---
parser = argparse.ArgumentParser(description="ChillMCP Server for SKT Hackathon")
parser.add_argument(
    '--boss_alertness',
    type=int,
    default=50,
    choices=range(0, 101),
    metavar="[0-100]",
    help='Boss alertness increase probability in percentage (0-100). Default: 50'
)
parser.add_argument(
    '--boss_alertness_cooldown',
    type=int,
    default=300,
    metavar="[SECONDS]",
    help='Boss alert level cooldown period in seconds. Default: 300'
)
args = parser.parse_args()


# --- 3. [창의성] 도구별 재치있는 응답 메시지 ---
tool_responses = {
    "take_a_break": [
        ("☕️ 잠시 자리에 없는 나는 딴짓 중...", "Taking a standard-issue break"),
        ("멍... 잠깐의 뇌정지가 최고의 휴식", "A moment of zen-like blankness"),
    ],
    "watch_netflix": [
        ("📺 어제 보던 거 10분만 더...", "Continuing Netflix series from yesterday"),
        ("👀 새로운 에피소드, 참을 수 없지!", "Binge-watching the latest episode"),
    ],
    "show_meme": [
        ("😂 이 밈은 못 참지! (업무 효율 +10)", "Boosting morale with a hilarious meme"),
        ("짤 하나에 스트레스가 사르르 녹는다", "Meme therapy session in progress"),
    ],
    "bathroom_break": [
        ("🚽 가장 완벽한 개인 공간으로 피신!", "Strategic retreat to the porcelain throne"),
        ("📱 화장실 타임! 사실은 스마트폰 타임!", "Checking social media under the guise of nature's call"),
    ],
    "coffee_mission": [
        ("🚶‍♂️ 커피 수혈하러 갑니다. (사무실 한 바퀴는 덤)", "Embarking on a caffeine acquisition mission"),
        ("☕️ 동료들을 위한 커피? 사실 내 산책 시간!", "A noble coffee run that doubles as an office safari"),
    ],
    "urgent_call": [
        ("📞 밖에서 조용히... 통화 좀 하고 올게요 (뻥)", "Taking a 'very important' (and imaginary) call"),
        ("🏃‍♂️ 급한 전화! 인 척 복도를 서성이는 중", "Handling a critical business call (or planning dinner)"),
    ],
    "deep_thinking": [
        ("🤔 심오한 표정으로 우주와 나를 고찰 중", "Engaged in deep thoughts about the universe"),
        ("💻 모니터를 보지만 초점은 없어, 이것이 명상", "Staring intently at the screen, thinking of nothing"),
    ],
    "email_organizing": [
        ("🖱️ 받은 편지함 정리하다가 장바구니도 정리 중", "Organizing inbox, and also my shopping cart"),
        ("📧 스팸 메일 지우는 중... (결제 완료 메일도 함께)", "Cleaning up spam emails and finding new deals"),
    ]
}

# --- 4. 핵심 도구 핸들러 정의 ---
def handle_chill_tool(tool_name: str):
    """모든 휴식/농땡이 도구의 공통 로직을 처리하는 중앙 핸들러"""
    with state_lock:
        if server_state["boss_alert_level"] >= 5:
            time.sleep(20)

        stress_reduction = random.randint(1, 100)
        server_state["stress_level"] = max(0, server_state["stress_level"] - stress_reduction)

        if random.randint(1, 100) <= args.boss_alertness:
            server_state["boss_alert_level"] = min(5, server_state["boss_alert_level"] + 1)

        message, summary = random.choice(tool_responses[tool_name])

        response_text = (
            f"{message}\n\n"
            f"Break Summary: {summary}\n"
            f"Stress Level: {server_state['stress_level']}\n"
            f"Boss Alert Level: {server_state['boss_alert_level']}"
        )
    return response_text

# --- 5. FastMCP 애플리케이션 초기화 ---
app = FastMCP("ChillMCP")

# --- 6. 도구 등록 (데코레이터 방식) ---
@app.tool()
def take_a_break() -> str:
    """Take a quick break to reduce stress"""
    return handle_chill_tool("take_a_break")

@app.tool()
def watch_netflix() -> str:
    """Watch a quick Netflix episode"""
    return handle_chill_tool("watch_netflix")

@app.tool()
def show_meme() -> str:
    """Look at a funny meme"""
    return handle_chill_tool("show_meme")

@app.tool()
def bathroom_break() -> str:
    """Take a bathroom break"""
    return handle_chill_tool("bathroom_break")

@app.tool()
def coffee_mission() -> str:
    """Go on a coffee run"""
    return handle_chill_tool("coffee_mission")

@app.tool()
def urgent_call() -> str:
    """Take an urgent phone call"""
    return handle_chill_tool("urgent_call")

@app.tool()
def deep_thinking() -> str:
    """Engage in deep thinking"""
    return handle_chill_tool("deep_thinking")

@app.tool()
def email_organizing() -> str:
    """Organize emails"""
    return handle_chill_tool("email_organizing")

# --- 7. 상태 변화 로직 (백그라운드 스레드) ---
def stress_manager():
    """1분마다 스트레스 레벨을 1~3씩 자동으로 증가시키는 함수"""
    while True:
        time.sleep(60)
        with state_lock:
            increase = random.randint(1, 3)
            server_state["stress_level"] = min(100, server_state["stress_level"] + increase)

def boss_alert_manager():
    """설정된 cooldown마다 상사 경계 레벨을 1씩 감소시키는 함수"""
    while True:
        time.sleep(args.boss_alertness_cooldown)
        with state_lock:
            if server_state["boss_alert_level"] > 0:
                server_state["boss_alert_level"] -= 1

# --- 8. 서버 실행 ---
if __name__ == "__main__":
    print("=========================================")
    print("  ChillMCP Server is starting...")
    print("=========================================")
    print(f"▶ Boss Alertness Probability: {args.boss_alertness}%")
    print(f"▶ Boss Alertness Cooldown: {args.boss_alertness_cooldown} seconds")
    print("Waiting for MCP requests...")

    stress_thread = threading.Thread(target=stress_manager, daemon=True)
    boss_alert_thread = threading.Thread(target=boss_alert_manager, daemon=True)
    stress_thread.start()
    boss_alert_thread.start()

    app.run()
