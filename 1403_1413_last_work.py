import pygame  # 게임 화면, 버튼, 이벤트 처리 등 그래픽 기능을 제공
import sys     # 시스템 종료를 위한 모듈 (예: sys.exit())

# -------------------------------
# 화면 및 시계 설정
# -------------------------------
pygame.init()  # pygame 사용 전 초기화
screen = pygame.display.set_mode((1100, 700))  # 1100x900 크기의 창 생성
pygame.display.set_caption("한국사 퀴즈")     # 창 제목 설정
clock = pygame.time.Clock()  # FPS 초당 프레임 수 조절
background_image = pygame.transform.scale(pygame.image.load("RLGMLA.png"), (1100, 700))
# 배경 이미지 1100, 700크기로 불러오기
# font = pygame.font.Font("../SB 어그로OFT M.otf", 36)# 한글이 깨져서 변경
font = pygame.font.Font("../SB-B.ttf", 36)

# -------------------------------
# 색상 정의 (R, G, B 값으로 표현)
# -------------------------------
GRAY = (127,127,127)     #회색 (글자용) 이제 의미 있음
realgreen = (93, 213, 117)  # 배경에 어울리는 초록색 (버튼용)
BLACK = (0, 0, 0)           # 검정색 (글자용)
BLUE = (80, 120, 255)       # 파란색 (결과 출력용)
brown = (189, 131, 87)      # 배경에 어울리는 갈색 (버튼용)
#

# -------------------------------
# 퀴즈 데이터 (문제, 보기, 정답)
# -------------------------------

# 퀴즈 데이터 구조
quizzes = {
    '고조선': [
        ("고조선의 원래 이름은?",  # 문제
         ["고조", "고죠 사토루", "조선", "고조선"],  # 4지선다
         2,  # 답
         "조선시대때 조선의 이름의 유래가 되었답니다."),#해설
        ("고조선의 건국과 관련된 인물로 바른 인물은?",
         ["박혁거세","온조","주몽","단군"],
         3,
         '고조선은 단군할아버지가 세우신 나라입니다.'),
        ("다음 중 고조선의 법으로 알려진 것은 무엇인가요?",
         ["육조법","팔조법","십이조법","십육진법"],
         2,
         '고조선의 8 조법은 고조선 사회의 질서 유지를 위해 만들어진 \n법률로, 현재는 세 가지 조항만 전해지고 있습니다. 이 법 조항을\n통해 당시 사회의 모습을 엿볼 수 있습니다.'),
    ],
    '삼국 시대': [
        ("고구려의 장수왕이 한 중요한 업적으로\n옳은 것은 무엇인가요?",
         ["수도를 평양으로 옮겼다","일본과의 외교 관계를 맺었다","황산벌 전투에서 백제를 공격했다","당나라에 사신을 보냈다"],
         0,
         "장수왕은 고구려의 전성기를 이끈 왕 중 하나로\n수도를 국내성에서 평양으로 옮겼습니다.\n이것은 남진 정책의 일환으로 백제와 신라를\n압박하기 위한 전략적 선택이었습니다."),
        ("백제의 수도 변천 과정을 순서대로 바르게 나열한 것은?",
         ["한성 → 사비 → 웅진","사비 → 한성 → 웅진","한성 → 웅진 → 사비","웅진 → 사비 → 한성"],
         2,
         "한성 → 웅진 → 다시 사비로\n천도하여 발전을 했답니다."),
        ("다음 중 신라의 골품제도와\n가장 관련이 깊은 설명은 무엇인가요?",
         ["왕이 된 후 영토를 크게 확장하였다","사람의 신분에 따라 관직 진출이 제한되었다","외국 문물을 받아들이는 데 앞장섰다","활발한 해상 무역을 통해 발전하였다"],
         1,
         "골품제도는 신라의 고유 신분제도로써 진골·6두품 등으로\n나뉘며 높은 관직에 오를 수 있는 범위가\n신분에 따라 엄격히 제한되었습니다."),
    ],
    '후삼국시대': [
        ("후삼국 시대를 형성한 세 나라에\n해당하지 않는 것은 무엇인가요?",
         ["후고구려","후백제","신라","고려"],
         3,
         "후삼국 시대는 후고구려, 후백제, 신라 세 나라로 이루어졌습니다.\n고려는 이후 왕건이 후고구려를 계승해 건국한 나라입니다."),
        ("후백제를 세운 인물은 누구인가요?",
         ["궁예","견훤","왕건","장보고"],
         1,
         "후백제는 견훤이 900년에 전주를 근거지로 세운 나라입니다."),
        ("왕건은 궁예의 부하였지만 나중에 그를 몰아내고\n나라를 세웠다.이 내용과 관련된 설명으로 옳은 것은?",
         ["왕건은 신라의 왕자였다.","궁예는 후백제를 세웠다.","왕건은 고려를 세웠다.","후백제가 고려를 멸망시켰다."],
         2,
         "왕건은 궁예의 부하였으나 궁예의 폭정에 반발해\n그를 몰아내고 고려를 건국했습니다."),
    ],
    '고려시대': [
        ("고려를 건국한 인물은 누구인가요?",
         ["견훤", "왕건", "이성계", "고졸 사토루"],
         1,
         "후고구려를 계승하여 왕건이 고려를 건국했습니다."),
        ("고려가 거란의 침입을 막기 위해 쌓은 성은?",
         ["흥화진", "천리장성", "팔만대장경", "광개토대왕릉"],
         1,
         "고려는 거란의 침입에 대비하여 국경에 천리장성을 쌓았습니다."),
        ("팔만대장경이 만들어진 이유는?",
         ["왕권 강화를 위해", "유교 확산을 위해", "몽골 침입을 물리치기 위해", "고려 건국 기념으로"],
         2,
         "고려는 몽골의 침입에 맞서 불교의 힘으로\n극복하려는 의지로 팔만대장경을 조판했습니다."),
    ],
    '조선시대': [
        ("조선을 건국한 인물은 누구인가요?",
         ["이방원", "이순신", "이성계", "정도전"],
         2,
         "조선은 1392년 이성계가 고려를 멸망시키고 건국한 나라입니다."),
        ("조선의 통치 이념은 무엇인가요?",
         ["불교", "유교", "도교", "학교"],
         1,
         "조선은 성리학 중심의 유교 정치 이념으로 나라를 다스렸습니다."),
        ("훈민정음을 창제한 왕은 누구인가요?",
         ["세종대왕", "세조", "성종", "중종"],
         0,
         "세종대왕은 백성을 위한 글자인 훈민정음을 만들었습니다.\n틀린 사람 없죠?"),
    ],
    '일제강점기': [
        ("대한민국임시정부는 어느 나라에서 수립되었나요?",
         ["일본", "중국", "미국", "러시아"],
         1,
         "1919년 상하이에서 독립운동가들이 모여 대한민국임시정부를\n수립했습니다."),
        ("일제가 한국인의 언어와 이름을\n말살하기 위해 시행한 정책은?",
         ["병합정책", "말살정책", "창씨개명", "무단통치"],
         2,
         "창씨개명은 한국인의 성과 이름을 일본식으로 바꾸도록\n강요한 동화정책의 일환이었습니다."),
        ("1930년대 이후 독립운동의 중심 무대는 어디였나요?",
         ["만주", "일본", "조선 내", "미국"],
         0,
         "1930년대 이후 무장투쟁은 주로\n만주와 중국 본토에서 전개되었습니다."),
    ]
}

# -------------------------------
# 게임 상태 및 변수 초기화
# -------------------------------
stage = 'start'  # 현재 게임 상태 ('select' = 시대 선택, 'quiz' = 문제 중, 'result' = 결과 화면, 'explain' = 해설 화면)
selected_era = ''  # 사용자가 선택한 시대 (문제 분류 키로 사용)
question_idx = 0  # 현재 진행 중인 문제 번호 (0, 1, 2, 더 추가할 예정)
score = 0  # 맞춘 문제 수 (점수)
clicked = False  # 문제 하나당 한 번만 클릭되도록 제어하는 플래그
current_explanation = ""  # 해설 저장용 변수


# -------------------------------
# draw_button(): 버튼 생성 및 텍스트 출력 함수 구글링
# -------------------------------
def draw_button(text, x, y, w, h):
    """
    - text: 버튼에 표시할 문자열
    - x, y: 버튼의 좌측 상단 좌표
    - w, h: 버튼의 너비와 높이
    - color: 버튼 배경색 (기본 회색)
    """

    if stage == 'start':
        color = GRAY
    elif stage == 'select':
        color = realgreen
    else:
        color = brown
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stage == 'start':
                start_btn = pygame.Rect(300, 300, 300, 60)
                background_image = pygame.transform.scale(pygame.image.load("RLGMLA.png"), (1100, 700))
                if start_btn.collidepoint(event.pos):
                    background_image = pygame.transform.scale(pygame.image.load("main.png"), (1100, 700))
                    stage = 'select'


            elif stage == 'select':  # 시대 선택 화면일 때
                background_image = pygame.transform.scale(pygame.image.load("unravel.png"), (1100, 700))
                for idx, era in enumerate(quizzes.keys()):
                    btn = pygame.Rect(100, 100 + idx * 70, 700, 50)  # 버튼 크기
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

            elif stage == 'explain':  # 해설 화면
                question_idx += 1  # 다음 문제로 이동
                if question_idx >= len(quizzes[selected_era]):
                    stage = 'result'  # 모든 문제 완료 시 결과 화면 전환
                else:
                    stage = 'quiz'  # 다음 문제로 이동
                clicked = False  # 클릭 플래그 초기화
                current_explanation = ""  # 해설 초기화

            elif stage == 'result':  # 결과 화면에서 클릭 시
                background_image = pygame.transform.scale(pygame.image.load("main.png"), (1100, 700))
                stage = 'select'  # 다시 시대 선택 화면으로 이동

    # -------------------------------
    # 화면 출력
    # -------------------------------
    if stage == 'start':  # 시작 화면 출력
        title_surface = font.render("한국사 퀴즈에 오신 걸 환영합니다!", True, BLACK)
        screen.blit(title_surface, (100, 100))
        draw_button("시작하기", 300, 300, 300, 60)

    elif stage == 'select':  # 시대 선택 화면
        title = font.render("시대를 선택하세요", True, BLACK)
        screen.blit(title, (100, 40))
        for idx, era in enumerate(quizzes.keys()):
            draw_button(era, 100, 100 + idx * 70, 700, 50)


    elif stage == 'quiz':  # 퀴즈 문제 화면
        q_data = quizzes[selected_era][question_idx]  # 현재 문제 정보 가져오기
        question_lines = f"문제 {question_idx + 1}. {q_data[0]}".split('\n')# 문제 내용이 여러 줄일 경우 줄바꿈 처리
        for idx, line in enumerate(question_lines):
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, (100, 100 + idx * 40))  # 문제 출력 (줄마다 간격)
        # 보기 4개 출력 (버튼 형태)
        for i in range(4):
            draw_button(q_data[1][i], 100, 200 + i * 70, 700, 50)


    elif stage == 'explain':  # 해설 화면
        explanation_surface = font.render("해설:", True, GRAY)
        screen.blit(explanation_surface, (100, 100))  # "해설:" 표시
        wrapped_lines = current_explanation.split("\n")  # 해설 텍스트 줄바꿈 적용
        for idx, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, GRAY)
            screen.blit(line_surface, (100, 150 + idx * 40))  # 해설 문단 출력
            draw_button("다음 문제", 300, 400, 300, 60)  # 다음 문제로 넘어가는 버튼



    elif stage == 'result':  # 퀴즈 결과 화면
        # 점수 요약 텍스트 구성 및 출력
        result_text = f"[{selected_era}] 총점: {score} / {len(quizzes[selected_era])}점"
        result_surface = font.render(result_text, True, BLUE)
        screen.blit(result_surface, (100, 100))# 클릭 시 시대 선택 화면으로 이동할 수 있는 버튼
        draw_button("클릭하시면 시대선택 화면으로 넘어 갑니다.", 200, 300, 700, 60)

    pygame.display.flip()  # 화면 업데이트
    clock.tick(60)  # 초당 60프레임 유지
