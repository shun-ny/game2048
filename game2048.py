import pygame
import random

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
TILE_MARGIN = 3

BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

DEFAULT_TILE_COLOR = (60, 58, 50)

def draw_cell(screen, row, col, value):
    
    rect = pygame.Rect(
        col * TILE_SIZE + TILE_MARGIN,
        row * TILE_SIZE + TILE_MARGIN,
        TILE_SIZE - TILE_MARGIN * 2,
        TILE_SIZE - TILE_MARGIN * 2
    )
    

    # Tile의 값에 해당하는 그림을 그림
    try:
        cell_color = TILE_COLORS[value]
    except KeyError:
        cell_color = DEFAULT_TILE_COLOR
    
    pygame.draw.rect(screen, cell_color, rect)
    if value!=0:
        text_screen = font.render(str(value),True, (0,0,0))
        
        cell_x=rect.centerx - (text_screen.get_width()//2)
        cell_y=rect.centery - (text_screen.get_height()//2)
        screen.blit(text_screen,(cell_x,cell_y))

# is_cw : True 이면 시계방향 회전, False이면 반시계방향 회전
def rotate(is_cw,board_map):
    if is_cw:
        return [list(r) for r in zip(*board_map[::-1])]
    return [list(r) for r in zip(*board_map)][::-1]

def merge_row(board_row):
    org_len = len(board_row)
    new_row = []
    skip_merge = False

    for i in range(org_len):
        if skip_merge is True:
            skip_merge = False
            continue

        if board_row[i] == 0:
            continue
        elif i + 1 < org_len and board_row[i] == board_row[i+1]:
            new_row.append(board_row[i]*2)  # 동일한 숫자를 더하는 것임으로 곱하기 2로 간다
            skip_merge = True
        else:
            new_row.append(board_row[i])
    while len(new_row) < org_len:
        new_row.append(0)

    return new_row

def is_game_over(board_map):
    # 1. 빈 공간이 있는지 확인
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board_map[r][c] == 0:
                return False

    # 2. 가로로 인접한 같은 숫자가 있는지 확인
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if board_map[r][c] == board_map[r][c+1]:
                return False

    # 3. 세로로 인접한 같은 숫자가 있는지 확인
    for r in range(GRID_SIZE - 1):
        for c in range(GRID_SIZE):
            if board_map[r][c] == board_map[r+1][c]:
                return False

    # 위 조건에 해당 없으면 움직일 수 없는 상태임
    return True

def draw_game_over(screen):
    # 화면을 반투명하게 덮는 오버레이
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180) # 투명도
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))

    # 게임오버 텍스트 출력
    over_font = pygame.font.SysFont("Arial", 80, True)
    text = over_font.render("!!!Game Over!!!", True, (119, 110, 101))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # 재시작 안내 (선택 사항)
    retry_font = pygame.font.SysFont("Arial", 30, True)
    retry_text = retry_font.render("Press 'R' to Restart or 'Q' to Quit", True, (119, 110, 101))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(retry_text, retry_rect)
        

# 사용자가 지정한 횟수 만큼 CW90 회전후 merge, CCW90 회전
def rotate_merge(rot_times, board_map):
    rotated_map = board_map

    # CW90
    for _ in range(rot_times):
        rotated_map = rotate(True, rotated_map)
    # Merge
    new_board = []
    for row in rotated_map:
        new_row = merge_row(row)
        new_board.append(new_row)

    # CCW90
    for _ in range(rot_times):
        new_board = rotate(False, new_board)
    
    return new_board

def handle_key(key_event, board_map):
    new_board = None

    match key_event:
        case pygame.K_LEFT:
            new_board = rotate_merge(0, board_map)
        case pygame.K_RIGHT:
            new_board = rotate_merge(2, board_map)
        case pygame.K_UP:
            new_board = rotate_merge(3, board_map)
        case pygame.K_DOWN:
            new_board = rotate_merge(1, board_map)
        case _:
            pass            
    return new_board

def spawn_tile(board_map):
    # 비어있는 위치 찾기
    empty_cells = [
        (r,c)
        for r in range (GRID_SIZE)
        for c in range (GRID_SIZE)
        if board_map[r][c] == 0
    ]

    # 비어 있는 위치가 있으면
    if empty_cells:
        # - 어느 위치에 생성할지 결정
        r, c = random.choice(empty_cells)
    
        # - 어느 숫자를 생성할지 결정
        v = random.choices([2,4], weights=[0.9, 0.1])[0] #확률넣어주기
        
        # - 맵을 업뎃
        board_map[r][c] = v


def render_board(screen, board_map):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_cell(screen, row, col, board_map[row][col])

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 Game") # 창 제목 추가
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 60, True)
    running = True
    game_over = False

    # Board map 초기화
    board_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] 

    # 시작 시 타일 2개 생성
    spawn_tile(board_map)
    spawn_tile(board_map)

    # 루프가 이 블록(if __name__...) 안으로 들어와야 합니다!
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                
                if game_over and event.key == pygame.K_r:
                    board_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    spawn_tile(board_map)
                    spawn_tile(board_map)
                    game_over = False
                
                if not game_over:
                    old_board = [row[:] for row in board_map]
                    new_board = handle_key(event.key, board_map)
                    
                    if new_board is not None and new_board != old_board:
                        board_map = new_board
                        spawn_tile(board_map)
                        if is_game_over(board_map):
                            game_over = True

        screen.fill(BG_COLOR)
        render_board(screen, board_map)

        # 게임 오버 시 메시지 출력 추가
        if game_over:
            draw_game_over(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()