import argparse
import time
import random
import threading
import logging
from datetime import datetime
from fastmcp import FastMCP

# 로그 설정
logging.basicConfig(
    filename='chillmcp.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 1. 서버 상태 관리 ---
server_state = {
    "stress_level": 50,  # 초기값 50으로 시작
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
        ("☕️ 잠시 자리를 비웁니다... 사실 멍때리는 중", "Taking a well-deserved mental break from spreadsheets"),
        ("🧘‍♂️ 스트레칭이라고 쓰고 유튜브 숏츠라고 읽는다", "Engaging in therapeutic desk yoga (aka phone scrolling)"),
        ("💭 5분만... 딱 5분만 쉬면 다시 일할게요", "Entering a brief zen state before returning to productivity"),
    ],
    "watch_netflix": [
        ("📺 점심시간 끝나는데 한 화만 더 보면 안 될까?", "Continuing last night's cliffhanger episode during lunch break"),
        ("🍿 업무 효율을 위한 문화생활이라 우기는 중", "Conducting essential market research on trending entertainment"),
        ("👀 이번 화는 진짜 마지막... 다음 화 시작됐네?", "Accidentally binge-watching while pretending to work on reports"),
    ],
    "show_meme": [
        ("😂 이 밈 하나면 오늘 하루 버틸 수 있어!", "Boosting team morale with cutting-edge internet humor"),
        ("🤣 밈 저장 폴더가 업무 폴더보다 큰 건 비밀", "Curating a professional collection of motivational memes"),
        ("💯 웃다가 상사 눈 마주쳤지만 괜찮아, 밈이 더 중요해", "Sharing workplace-appropriate comedy for stress relief"),
    ],
    "bathroom_break": [
        ("🚽 화장실은 나만의 힐링 공간... 스마트폰은 필수템", "Strategic retreat to the porcelain throne for focus time"),
        ("📱 급한 일이라며... 사실 SNS 확인 중", "Handling urgent personal matters in private sanctuary"),
        ("💼 변기 커버에 앉아 인생을 고민하는 시간", "Taking a contemplative break in the executive washroom"),
    ],
    "coffee_mission": [
        ("☕️ 커피 한 잔이면 사무실 한 바퀴는 공짜!", "Embarking on essential caffeine acquisition mission"),
        ("🚶‍♂️ 동료들 커피 주문받다가 20분 지나갔네", "Conducting thorough survey of team beverage preferences"),
        ("🏃‍♂️ 카페 대기줄도 업무의 연장선... 맞죠?", "Networking with fellow professionals at the coffee station"),
    ],
    "urgent_call": [
        ("📞 '여보세요?' 아무도 없지만 진지한 표정 유지", "Handling critical business negotiations with imaginary client"),
        ("🤫 복도에서 20분째 통화 중... 사실 아무도 안 걸려옴", "Managing time-sensitive communications in corridor conference room"),
        ("😅 급한 척 나갔다가 자판기 앞에서 멍때리는 중", "Coordinating urgent project details while contemplating snack options"),
    ],
    "deep_thinking": [
        ("🤔 화면 응시 중... 사실 점심 메뉴 고민 중", "Engaging in profound strategic planning for afternoon efficiency"),
        ("💻 모니터 보고 있지만 영혼은 주말 여행 중", "Deep-diving into complex problem-solving with intense focus"),
        ("🧠 심각한 표정 = 업무 중... 실제로는 로또 번호 생각 중", "Conducting critical analysis of project feasibility and dinner plans"),
    ],
    "email_organizing": [
        ("📧 받은편지함 정리 중... 장바구니도 같이 정리", "Optimizing inbox workflow and online shopping cart simultaneously"),
        ("🛒 스팸메일 지우다가 쿠팡 오늘의 딜 확인 중", "Implementing efficient email management while checking flash sales"),
        ("💳 업무 메일 사이에 결제완료 메일이 섞여있어도 OK", "Streamlining communication channels and payment confirmations"),
    ]
}

# --- 4. 핵심 도구 핸들러 정의 ---
def handle_chill_tool(tool_name: str):
    """모든 휴식/농땡이 도구의 공통 로직을 처리하는 중앙 핸들러"""
    with state_lock:
        # 페널티 적용: Boss Alert Level이 5면 5초 대기 (타임아웃 방지)
        if server_state["boss_alert_level"] >= 5:
            logging.warning(f"⚠️  Boss is watching! 5 second penalty applied for {tool_name}")
            time.sleep(5)  # 20초에서 5초로 변경

        # 스트레스 감소 (1-100 랜덤)
        stress_reduction = random.randint(1, 100)
        old_stress = server_state["stress_level"]
        server_state["stress_level"] = max(0, server_state["stress_level"] - stress_reduction)

        # 상사 경계도 증가 (설정된 확률로, 5 미만일 때만)
        boss_increased = False
        if server_state["boss_alert_level"] < 5:
            if random.randint(1, 100) <= args.boss_alertness:
                old_boss = server_state["boss_alert_level"]
                server_state["boss_alert_level"] += 1
                boss_increased = True
                logging.info(f"👔 Boss Alert increased: {old_boss} → {server_state['boss_alert_level']}")

        # 랜덤 응답 메시지 선택
        message, summary = random.choice(tool_responses[tool_name])

        # 로그 기록
        logging.info(f"🎯 Tool used: {tool_name} | Stress: {old_stress}→{server_state['stress_level']} | Boss: {server_state['boss_alert_level']}" + (" ⬆️" if boss_increased else ""))

        # 범위 검증 (안전장치)
        stress_level = max(0, min(100, server_state["stress_level"]))
        boss_level = max(0, min(5, server_state["boss_alert_level"]))

        # 필수 파싱 형식에 맞춰 응답 생성
        response_text = (
            f"{message}\n\n"
            f"Break Summary: {summary}\n"
            f"Stress Level: {stress_level}\n"
            f"Boss Alert Level: {boss_level}"
        )
    
    return response_text

# --- 5. FastMCP 애플리케이션 초기화 ---
app = FastMCP("ChillMCP")

# --- 6. 필수 도구 8개 등록 ---

# 기본 휴식 도구 (3개)
@app.tool()
def take_a_break() -> str:
    """Take a basic break to reduce stress and relax"""
    return handle_chill_tool("take_a_break")

@app.tool()
def watch_netflix() -> str:
    """Watch a Netflix episode to unwind during break time"""
    return handle_chill_tool("watch_netflix")

@app.tool()
def show_meme() -> str:
    """Look at funny memes to boost morale and reduce stress"""
    return handle_chill_tool("show_meme")

# 고급 농땡이 기술 (5개)
@app.tool()
def bathroom_break() -> str:
    """Take a bathroom break (with phone for maximum relaxation)"""
    return handle_chill_tool("bathroom_break")

@app.tool()
def coffee_mission() -> str:
    """Go on a coffee run that doubles as a nice walk around the office"""
    return handle_chill_tool("coffee_mission")

@app.tool()
def urgent_call() -> str:
    """Pretend to take an urgent phone call to step away from desk"""
    return handle_chill_tool("urgent_call")

@app.tool()
def deep_thinking() -> str:
    """Appear to be deep in thought while actually daydreaming"""
    return handle_chill_tool("deep_thinking")

@app.tool()
def email_organizing() -> str:
    """Organize emails while sneakily doing some online shopping"""
    return handle_chill_tool("email_organizing")

# --- 7. 상태 변화 로직 (백그라운드 스레드) ---
def stress_manager():
    """1분마다 스트레스 레벨을 1씩 자동으로 증가시키는 함수"""
    while True:
        time.sleep(60)
        with state_lock:
            old_stress = server_state["stress_level"]
            server_state["stress_level"] = min(100, server_state["stress_level"] + 1)
            logging.info(f"📈 Stress increased: {old_stress} → {server_state['stress_level']} (+1)")

def boss_alert_manager():
    """설정된 cooldown마다 상사 경계 레벨을 1씩 감소시키는 함수"""
    while True:
        time.sleep(args.boss_alertness_cooldown)
        with state_lock:
            if server_state["boss_alert_level"] > 0:
                old_level = server_state["boss_alert_level"]
                server_state["boss_alert_level"] -= 1
                logging.info(f"👔 Boss alert decreased: {old_level} → {server_state['boss_alert_level']}")

# --- 8. 서버 실행 ---
if __name__ == "__main__":
    print("=" * 60)
    print("  🎮 ChillMCP Server - SKT Hackathon Edition")
    print("=" * 60)
    print(f"⚙️  Configuration:")
    print(f"   • Boss Alertness Probability: {args.boss_alertness}%")
    print(f"   • Boss Alertness Cooldown: {args.boss_alertness_cooldown} seconds")
    print(f"\n📊 Initial State:")
    print(f"   • Stress Level: {server_state['stress_level']}")
    print(f"   • Boss Alert Level: {server_state['boss_alert_level']}")
    print(f"\n📝 Logs will be written to: chillmcp.log")
    print(f"💡 Monitor logs: tail -f chillmcp.log")
    print(f"\n🚀 Server starting... Waiting for MCP requests...")
    print("=" * 60)

    # 초기 상태 로그 기록
    logging.info("=" * 60)
    logging.info(f"ChillMCP Server Started")
    logging.info(f"Boss Alertness: {args.boss_alertness}% | Cooldown: {args.boss_alertness_cooldown}s")
    logging.info(f"Initial - Stress: {server_state['stress_level']} | Boss Alert: {server_state['boss_alert_level']}")
    logging.info("=" * 60)

    # 백그라운드 스레드 시작
    stress_thread = threading.Thread(target=stress_manager, daemon=True)
    boss_alert_thread = threading.Thread(target=boss_alert_manager, daemon=True)
    stress_thread.start()
    boss_alert_thread.start()

    # FastMCP 서버 실행
    app.run()
