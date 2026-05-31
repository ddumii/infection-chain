import pygame as pg, math, os

# 1. 초기화 및 설정
pg.init()
sw, sh = 1920, 1080
screen = pg.display.set_mode((sw, sh)) # 창 생성
clock = pg.time.Clock() # FPS 조절용

# 시스템 마우스 커서 숨기기
pg.mouse.set_visible(False)

# 스크립트 위치 확인 및 이미지 에셋들 로드
base_path = os.path.dirname(__file__)

# 배경 이미지 로드
try:
    bg_path = os.path.join(base_path, "assets", "background.png")
    background_img = pg.image.load(bg_path).convert()
    background_img = pg.transform.smoothscale(background_img, (sw, sh))
except Exception as e:
    print(f"배경 이미지를 로드하지 못했습니다: {e}")
    background_img = None

# [수정] 커서 이미지(Player) 로드 및 크기 2배 확대 (100x100 -> 200x200)
try:
    img_path = os.path.join(base_path, "assets", "player.png")
    cursor_img = pg.image.load(img_path).convert_alpha()
    cursor_img = pg.transform.smoothscale(cursor_img, (200, 200))
except Exception as e:
    print(f"커서 이미지를 로드하지 못했습니다: {e}")
    cursor_img = pg.Surface((200, 200), pg.SRCALPHA)
    pg.draw.circle(cursor_img, (135, 206, 235), (100, 100), 99)

# [수정] 총알 이미지 글로벌 로드 및 크기 2배 확대 (120x60 -> 240x120)
try:
    bullet_path = os.path.join(base_path, "assets", "gun.png")
    bullet_asset_raw = pg.image.load(bullet_path).convert_alpha()
    bullet_asset_pre_rotated = pg.transform.rotate(bullet_asset_raw, -90)
    bullet_orig_global = pg.transform.smoothscale(bullet_asset_pre_rotated, (240, 120))
except Exception as e:
    print(f"총알 이미지를 로드하지 못했습니다: {e}")
    bullet_orig_global = pg.Surface((80, 32), pg.SRCALPHA)
    bullet_orig_global.fill((255, 255, 0))

# 2. 총알 클래스
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pg.transform.rotate(bullet_orig_global, angle)
        self.rect = self.image.get_rect(center=pos) 
        
        rad = math.radians(angle)
        self.vel = pg.math.Vector2(math.cos(rad), -math.sin(rad)) * 10

    def update(self):
        self.rect.center += self.vel 
        if not screen.get_rect().contains(self.rect): self.kill()

# 3. 플레이어 클래스
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 플레이어 외형이 200으로 커졌으므로 내부 판정 범위(Surface)도 200x200으로 맞춰줍니다.
        self.orig = pg.Surface((200, 200), pg.SRCALPHA)
        self.image, self.pos = self.orig, pg.math.Vector2(sw/2, sh/2)
        self.rect = self.image.get_rect(center=self.pos)
        
        self.max_hp = 3
        self.hp = int(self.max_hp)

        # BAR 이미지들 로드 (가로로 길어진 409x70 크기 유지)
        self.hp_images = []
        for i in range(1, 4):
            loaded = False
            for ext in [f"BAR{i}.PNG", f"bar{i}.png"]:
                try:
                    path = os.path.join(base_path, "assets", ext)
                    img = pg.image.load(path).convert_alpha()
                    img = pg.transform.smoothscale(img, (409, 70))
                    self.hp_images.append(img)
                    loaded = True
                    break
                except Exception: continue
            
            if not loaded:
                cols = [(0, 200, 0), (200, 200, 0), (200, 0, 0)]
                s = pg.Surface((409, 70), pg.SRCALPHA)
                s.fill(cols[i-1])
                self.hp_images.append(s)

    def update(self):
        m_pos = pg.math.Vector2(pg.mouse.get_pos()) 
        self.pos += (m_pos - self.pos) * 0.1 
        
        rel = m_pos - self.pos
        angle = math.degrees(-math.atan2(rel.y, rel.x))
        self.image = pg.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect(center=self.pos) 

    def draw_hp_bar(self, surf):
        if self.hp <= 0: return
        img_idx = self.max_hp - self.hp
        if 0 <= img_idx < len(self.hp_images):
            surf.blit(self.hp_images[img_idx], (20, 20))

# 4. 객체 및 그룹 관리
player = Player()
all_sprites = pg.sprite.Group(player) 
bullets = pg.sprite.Group() 

game_over = False

# 5. 메인 루프
run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT: run = False 
        
        if not game_over:
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                m = pg.mouse.get_pos()
                ang = math.degrees(-math.atan2(m[1]-player.pos.y, m[0]-player.pos.x))
                all_sprites.add(Bullet(player.pos, ang))

    if not game_over: all_sprites.update() 

    # 그리기 영역
    if background_img: screen.blit(background_img, (0, 0))
    else: screen.fill((30, 30, 30)) 
        
    all_sprites.draw(screen)  
    player.draw_hp_bar(screen) 
    
    if player.hp <= 0:
        player.hp = 0; game_over = True
        font = pg.font.SysFont(None, 60)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (sw//2 - text.get_width()//2, sh//2 - text.get_height()//2))

    # 게임오버가 아니면 커스텀 커서 그리기
    if not game_over:
        m_pos = pg.mouse.get_pos()
        # [수정] 200x200 크기의 대형 이미지가 마우스 정중앙에 조준되도록 오프셋 값을 절반인 100으로 변경
        screen.blit(cursor_img, (m_pos[0] - 100, m_pos[1] - 100))

    pg.display.flip() 
    clock.tick(100) 

pg.quit()