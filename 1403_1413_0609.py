import pygame  # 게임 화면, 버튼, 이벤트 처리 등 그래픽 기능을 제공
import sys     # 시스템 종료를 위한 모듈 (예: sys.exit())

# -------------------------------
# 화면 및 시계 설정
# -------------------------------
pygame.init()  # pygame 사용 전 초기화
screen = pygame.display.set_mode((1100, 700))  # 1100x900 크기의 창 생성
pygame.display.set_caption("한국사 퀴즈")     # 창 제목 설정
clock = pygame.time.Clock()  # FPS 초당 프레임 수 조절
background_image = pygame.transform.scale(pygame.image.load("main.png"), (1100, 700))
# 배경 이미지 1100, 700크기로 불러오기
# font = pygame.font.Font("../SB 어그로OFT M.otf", 36)# 한글이 깨져서 변경
font = pygame.font.Font("../SB-B.ttf", 36)

# -------------------------------
# 색상 정의 (R, G, B 값으로 표현)
# -------------------------------
#WHITE = (255, 255, 255)   흰색 (배경용) 이제 의미 없음
realgreen = (93, 213, 117)   # 배경에 어울리는 초록색 (버튼용)
BLACK = (0, 0, 0)        # 검정색 (글자용)
BLUE = (80, 120, 255)    # 파란색 (결과 출력용)
GREEN = (0, 180, 0)      # 초록색 (정답 표시용)
RED = (200, 0, 0)        # 빨간색 (오답 표시용)
#

# -------------------------------
# 퀴즈 데이터 (문제, 보기, 정답)
# -------------------------------

# 퀴즈 데이터 구조
quizzes = {
    '고조선': [
        ("",#문제
         ["","","",""],#4지선다
         0,#답
         ""),#해설
        ("",
         ["","","",""],
         0,
         ''),
        ("",
         ["","","",""],
         0,
         ''),
    ],
    '삼국 시대': [
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
    ],
    '후삼국시대': [
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
    ],
    '고려시대': [
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
    ],
    '조선시대': [
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
    ],
    '일제강점기': [
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
        ("",
         ["","","",""],
         0),
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
current_explanation = ""  # 해설 저장용 변수


# -------------------------------
# draw_button(): 버튼 생성 및 텍스트 출력 함수 구글링
# -------------------------------
def draw_button(text, x, y, w, h, color=realgreen):
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
running = True
while running:
    screen.blit(background_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()  # 마우스 현재 위치 저장

    for event in pygame.event.get():  # 사용자 입력 이벤트 처리
        if event.type == pygame.QUIT:  # 창 닫기 이벤트
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
            if stage == 'select':  # 시대 선택 화면일 때
                for idx, era in enumerate(quizzes.keys()):
                    btn = pygame.Rect(100, 100 + idx * 70, 700, 50)
                    if btn.collidepoint(event.pos):  # 버튼 클릭 감지
                        selected_era = era  # 선택한 시대 저장
                        stage = 'quiz'  # 퀴즈 모드로 전환
                        question_idx = 0  # 문제 번호 초기화
                        score = 0  # 점수 초기화
                        clicked = False  # 클릭 플래그 초기화

            elif stage == 'quiz' and not clicked:  # 퀴즈 진행 중이며 아직 선택 안 했을 때
                q_data = quizzes[selected_era][question_idx]  # 현재 문제 데이터 가져오기
                for i in range(4):  # 보기 4개 반복
                    btn = pygame.Rect(100, 200 + i * 70, 700, 50)
                    if btn.collidepoint(event.pos):  # 보기 클릭 감지
                        if i == q_data[2]:  # 정답 확인
                            score += 1  # 정답이면 점수 증가
                        current_explanation = q_data[3]  # 해설 저장
                        clicked = True  # 중복 클릭 방지
                        stage = 'explain'  # 해설 화면으로 전환

            elif stage == 'explain':  # 해설 화면 클릭 시
                question_idx += 1  # 다음 문제로 이동
                if question_idx >= len(quizzes[selected_era]):
                    stage = 'result'  # 모든 문제 완료 시 결과 화면 전환
                else:
                    stage = 'quiz'  # 다음 문제로 이동
                clicked = False  # 클릭 플래그 초기화
                current_explanation = ""  # 해설 초기화

            elif stage == 'result':  # 결과 화면에서 클릭 시
                stage = 'select'  # 다시 시대 선택 화면으로 이동

    # -------------------------------
    # 화면 출력
    # -------------------------------
    if stage == 'select':  # 시대 선택 화면
        title = font.render("시대를 선택하세요", True, BLACK)
        screen.blit(title, (100, 40))
        for idx, era in enumerate(quizzes.keys()):
            draw_button(era, 100, 100 + idx * 70, 700, 50)

    elif stage == 'quiz':  # 퀴즈 문제 화면
        q_data = quizzes[selected_era][question_idx]
        question_surface = font.render(f"문제 {question_idx + 1}. {q_data[0]}", True, BLACK)
        screen.blit(question_surface, (100, 100))
        for i in range(4):  # 보기 버튼 출력
            draw_button(q_data[1][i], 100, 200 + i * 70, 700, 50)

    elif stage == 'explain':  # 해설 화면
        explanation_surface = font.render("해설:", True, BLACK)
        screen.blit(explanation_surface, (100, 100))
        wrapped_lines = current_explanation.split("\n")  # 줄바꿈 대응
        for idx, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, GREEN)
            screen.blit(line_surface, (100, 150 + idx * 40))
        draw_button("다음 문제", 300, 400, 300, 60)

    elif stage == 'result':  # 결과 화면
        result_text = f"[{selected_era}] 총점: {score} / {len(quizzes[selected_era])}점"
        result_surface = font.render(result_text, True, BLUE)
        screen.blit(result_surface, (100, 250))
        draw_button("다시 시작하기", 300, 350, 300, 60)

    pygame.display.flip()  # 화면 업데이트
    clock.tick(60)  # 초당 60프레임 유지
