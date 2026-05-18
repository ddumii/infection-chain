import pygame as pg, math

# 1. 초기화 및 설정
pg.init()
sw, sh = 800, 600
screen = pg.display.set_mode((sw, sh)) # 창 생성
clock = pg.time.Clock() # FPS 조절용

# 2. 총알 클래스
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        # 총알 이미지 생성 및 회전
        self.image = pg.transform.rotate(pg.Surface((10, 4), pg.SRCALPHA), angle)
        self.image.fill((255, 255, 0)) # 노란색 채우기
        self.rect = self.image.get_rect(center=pos) # 위치 설정
        # 각도를 라디안으로 바꿔 이동 방향(속도) 계산
        rad = math.radians(angle)
        self.vel = pg.math.Vector2(math.cos(rad), -math.sin(rad)) * 10

    def update(self):
        self.rect.center += self.vel # 매 프레임 속도만큼 이동
        # 화면 밖으로 나가면 메모리에서 삭제
        if not screen.get_rect().contains(self.rect): self.kill()

# 3. 플레이어 클래스
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 기본 외형(원) 그리기
        self.orig = pg.Surface((25, 25), pg.SRCALPHA)
        pg.draw.circle(self.orig, (135, 206, 235), (12, 12), 12)
        self.image, self.pos = self.orig, pg.math.Vector2(sw/2, sh/2)
        self.rect = self.image.get_rect(center=self.pos)
        
        # [체력 시스템] 총 체력 3 설정
        self.max_hp = 3.0
        self.hp = self.max_hp

    def update(self):
        m_pos = pg.math.Vector2(pg.mouse.get_pos()) # 마우스 위치 확인
        self.pos += (m_pos - self.pos) * 0.1 # [핵심] 마우스로 부드럽게 추적 (LERP)
        
        # 마우스 방향으로 이미지 회전
        rel = m_pos - self.pos
        angle = math.degrees(-math.atan2(rel.y, rel.x))
        self.image = pg.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect(center=self.pos) # 회전 후 중심 고정

    # [수정] 왼쪽 상단에 큰 체력바를 고정으로 그리는 메서드
    def draw_hp_bar(self, surf):
        if self.hp <= 0: return
        
        # 체력바 위치 및 크기 설정 (좌측 상단 고정값)
        bar_x = 20      # 왼쪽 여백
        bar_y = 20      # 상단 여백
        bar_width = 200 # 가로 길이
        bar_height = 20 # 세로 두께
        
        # 남은 체력 비율 계산
        fill = (self.hp / self.max_hp) * bar_width
        
        # 배경(빨간색)과 현재 체력(초록색) 사각형 생성
        bg_rect = pg.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = pg.Rect(bar_x, bar_y, fill, bar_height)
        
        # 테두리를 함께 그려 퀄리티를 높임 (옵션)
        pg.draw.rect(surf, (200, 0, 0), bg_rect)     # 깎인 체력 (빨강)
        pg.draw.rect(surf, (0, 255, 0), fill_rect)   # 남은 체력 (초록)
        pg.draw.rect(surf, (255, 255, 255), bg_rect, 2) # 흰색 테두리 (두께 2px)

# 4. 객체 및 그룹 관리
player = Player()
all_sprites = pg.sprite.Group(player) # 모든 그림 객체 그룹
bullets = pg.sprite.Group() # 총알 전용 그룹

# 게임오버 상태 변수
game_over = False

# 5. 메인 루프
run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT: run = False # X 버튼 누르면 종료
        
        # 게임오버가 아닐 때만 총알 발사 가능
        if not game_over:
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                # 클릭 시점의 각도를 계산해 총알 생성
                m = pg.mouse.get_pos()
                ang = math.degrees(-math.atan2(m[1]-player.pos.y, m[0]-player.pos.x))
                all_sprites.add(Bullet(player.pos, ang))

    # 게임 진행 중일 때만 이동 및 로직 업데이트
    if not game_over:
        all_sprites.update() 

    # 그리기 영역
    screen.fill((30, 30, 30)) # 배경 지우기
    all_sprites.draw(screen)  # 모든 객체 그리기
    
    # [수정된 위치] 왼쪽 배경 상단에 체력바 표시
    player.draw_hp_bar(screen) 
    
    # 체력이 0이 되면 게임오버 처리 및 문구 출력
    if player.hp <= 0:
        player.hp = 0
        game_over = True
        
        font = pg.font.SysFont(None, 60)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (sw//2 - text.get_width()//2, sh//2 - text.get_height()//2))

    pg.display.flip() # 화면 업데이트
    clock.tick(100) # 100 FPS 유지

pg.quit()