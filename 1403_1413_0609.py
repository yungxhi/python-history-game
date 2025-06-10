import pygame  # 게임 화면, 버튼, 이벤트 처리 등 그래픽 기능을 제공
import sys     # 시스템 종료를 위한 모듈 (예: sys.exit())

# -------------------------------
# 화면 및 시계 설정
# -------------------------------
pygame.init()  # pygame 사용 전 초기화
screen = pygame.display.set_mode((1100, 700))  # 1100x900 크기의 창 생성
pygame.display.set_caption("한국사 퀴즈")     # 창 제목 설정
clock = pygame.time.Clock()  # FPS 초당 프레임 수 조절

font = pygame.font.Font("SB-L.ttf", 36)

# -------------------------------
# 색상 정의 (R, G, B 값으로 표현)
# -------------------------------
WHITE = (255, 255, 255)  # 흰색 (배경용)
GRAY = (200, 200, 200)   # 회색 (버튼용)
BLACK = (0, 0, 0)        # 검정색 (글자용)
BLUE = (80, 120, 255)    # 파란색 (결과 출력용)
GREEN = (0, 180, 0)      # 초록색 (정답 표시용)
RED = (200, 0, 0)        # 빨간색 (오답 표시용)

# -------------------------------
# 퀴즈 데이터 (문제, 보기, 정답)
# -------------------------------

# 퀴즈 데이터 구조
quizzes = {
    '고조선': [
        ("고조선은 어떤 기간에 존재했는가?", #문제
        ["a) BC 2333년 ~ AD 108년", "b) BC 2333년 ~ BC 108년", "c) BC 108년 ~ AD 668년", "d) BC 2333년 ~ AD 668년"],#보기
        1),#답
        ("고조선의 건국 신화는 무엇인가?",#이하 동문
        ["a) 단군 신화", "b) 고구려 신화", "c) 신라 신화", "d) 백제 신화"],
        0),
        ("고조선의 수도는 어디인가?",
        ["a) 평양", "b) 대구", "c) 부산", "d) 서울"],
        0),
    ],
    '삼국 시대': [
        ("광개토대왕의 업적은?",
        ["a) 한강 유역 차지", "b) 백제를 멸망시킴", "c) 만주와 한반도 북부까지 확장", "d) 신라를 복속시킴"],
        2),
        ("백제 멸망과 관련 깊은 전투는?",
        ["a) 살수 대첩", "b) 황산벌 전투", "c) 안시성 전투", "d) 계백 대첩"],
        1),
        ("신라 삼국 통일 주도자는?",
        ["a) 김춘추", "b) 을지문덕", "c) 근초고왕", "d) 온달"],
        0),
    ],
    '후삼국시대': [
        ("왕건이 통일할 수 있었던 요인으로 보기 어려운 것은?",
        ["a) 해상 무역 기반", "b) 중앙집권 체제", "c) 호족과의 연합", "d) 신검과 대립 활용"],
        1),
        ("궁예 통치 실패 원인은?",
        ["a) 왕권 분산", "b) 외교 실패", "c) 폭정과 의심", "d) 수도 이전"],
        2),
        ("신라가 고려에 항복한 이유로 거리가 먼 것은?",
        ["a) 정통성 인정", "b) 불교 문화 파괴", "c) 군사적 약세", "d) 후대우 약속"],
        1),
    ],
    '고려시대': [
        ("고려를 건국한 왕은?",
        ["a) 궁예", "b) 견훤", "c) 왕건", "d) 정몽주"],
        2),
        ("거란과의 전투에서 활약한 장수는?",
        ["a) 이순신", "b) 강감찬", "c) 윤관", "d) 최무선"],
        1),
        ("고려의 최고 과거 시험은?",
        ["a) 잡과", "b) 소과", "c) 대과", "d) 문과"],
        3),
    ],
    '조선시대': [
        ("조선을 건국한 인물은?",
        ["a) 이성계", "b) 세종대왕", "c) 정몽주", "d) 이방원"],
        0),
        ("훈민정음 반포 연도는?",
        ["a) 1443년", "b) 1446년", "c) 1453년", "d) 1392년"],
        1),
        ("성균관의 목적은?",
        ["a) 무관 양성", "b) 천문 연구", "c) 유학 교육", "d) 군사 훈련"],
        2),
    ],
    '일제강점기': [
        ("1919년 일제에 항거한 독립운동은?",
        ["a) 광주 학생운동", "b) 3·1 운동", "c) 의열단 결성", "d) 임시정부 수립"],
        1),
        ("임시정부 초대 대통령은?",
        ["a) 김구", "b) 안중근", "c) 이승만", "d) 윤봉길"],
        2),
        ("문화 수호 운동은?",
        ["a) 실학 운동", "b) 민족 문화 수호 운동", "c) 친일 문학 운동", "d) 갑신정변"],
        1),
    ]
}

# -------------------------------
# 게임 상태 및 변수 초기화
# -------------------------------
stage = 'select'  # 현재 게임 상태 ('select' = 시대 선택, 'quiz' = 문제 중, 'result' = 결과 화면)
selected_era = ''  # 사용자가 선택한 시대 (문제 분류 키로 사용)
question_idx = 0  # 현재 진행 중인 문제 번호 (0, 1, 2, 더 추가할 예정)
score = 0  # 맞춘 문제 수 (점수)
clicked = False  # 문제 하나당 한 번만 클릭되도록 제어하는 플래그


# -------------------------------
# draw_button(): 버튼 생성 및 텍스트 출력 함수 구글링
# -------------------------------
def draw_button(text, x, y, w, h, color=GRAY):
    """
    - text: 버튼에 표시할 문자열
    - x, y: 버튼의 좌측 상단 좌표
    - w, h: 버튼의 너비와 높이
    - color: 버튼 배경색 (기본 회색)
    """
    pygame.draw.rect(screen, color, (x, y, w, h))  # 버튼 배경 그리기
    txt_surface = font.render(text, True, BLACK)  # 텍스트 이미지 생성
    txt_rect = txt_surface.get_rect(center=(x + w // 2, y + h // 2))  # 가운데 정렬 위치 계산
    screen.blit(txt_surface, txt_rect)  # 텍스트 화면에 출력
    return pygame.Rect(x, y, w, h)  # 클릭 감지를 위한 사각형 정보 반환


# -------------------------------
# 메인 루프 (게임이 종료될 때까지 반복)
# -------------------------------
running = True  # 게임 루프 실행 여부 제어 변수
while running:
    screen.fill(WHITE)  # 배경 흰색으로 초기화 (지우기)
    mouse_pos = pygame.mouse.get_pos()  # 마우스 현재 위치 (선택 시 사용 가능)

    # 이벤트 감지 (마우스 클릭, 창 닫기 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 창 닫기 시 루프 종료

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 시대 선택 화면일 때
            if stage == 'select':
                for idx, era in enumerate(quizzes.keys()):
                    # 버튼 위치 계산 (시대 목록 버튼들)
                    btn = pygame.Rect(100, 100 + idx * 70, 700, 50)
                    if btn.collidepoint(event.pos):  # 클릭 좌표가 버튼 안에 있으면
                        selected_era = era  # 선택한 시대 저장
                        stage = 'quiz'  # 문제 풀이 화면으로 전환
                        question_idx = 0  # 첫 번째 문제부터 시작
                        score = 0  # 점수 초기화
                        clicked = False  # 클릭 상태 초기화

            # 퀴즈 문제 화면일 때
            elif stage == 'quiz' and not clicked:
                q_data = quizzes[selected_era][question_idx]  # 현재 문제 정보 가져오기
                for i in range(4):  # 보기 4개 반복
                    btn = pygame.Rect(100, 200 + i * 70, 700, 50)  # 보기 버튼 위치
                    if btn.collidepoint(event.pos):
                        if i == q_data[2]:  # 정답 확인
                            score += 1  # 정답이면 점수 +1
                        clicked = True  # 더블 클릭 방지 플래그 설정

            # 결과 화면일 때
            elif stage == 'result':
                stage = 'select'  # 다시 시대 선택으로 돌아가기

    # -------------------------------
    # 화면 출력 영역
    # -------------------------------
    if stage == 'select':
        # 시대 선택 화면
        title = font.render("시대를 선택하세요", True, BLACK)
        screen.blit(title, (100, 40))
        for idx, era in enumerate(quizzes.keys()):
            draw_button(era, 100, 100 + idx * 70, 700, 50)

    elif stage == 'quiz':
        # 문제 화면
        q_data = quizzes[selected_era][question_idx]
        question_surface = font.render(f"문제 {question_idx + 1}. {q_data[0]}", True, BLACK)
        screen.blit(question_surface, (100, 100))

        for i in range(4):
            draw_button(q_data[1][i], 100, 200 + i * 70, 700, 50)

        if clicked:
            pygame.time.delay(100)  # 0.1초 대기
            question_idx += 1  # 다음 문제로 이동
            clicked = False  # 클릭 상태 초기화

            if question_idx >= len(quizzes[selected_era]):
                stage = 'result'  # 모든 문제 완료 → 결과 화면 전환

    elif stage == 'result':
        # 결과 출력 화면
        result_text = f"[{selected_era}] 총점: {score} / 3점"
        result_surface = font.render(result_text, True, BLUE)
        screen.blit(result_surface, (100, 250))
        draw_button("다시 시작하기", 300, 350, 300, 60)

    pygame.display.flip()  # 화면 업데이트
    clock.tick(60)  # 초당 60프레임 유지

pygame.quit()  # 게임 종료 시 pygame 자원 정리
