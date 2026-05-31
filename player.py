import pygame as pg
import math
import os

base_path = os.path.dirname(__file__)

# 1. 플레이어 이미지 로드 (80x80 크기 최적화)
try:
    img_path = os.path.join(base_path, "assets", "player.png")
    player_image_asset = pg.image.load(img_path).convert_alpha()
    player_image_asset = pg.transform.smoothscale(player_image_asset, (150, 150))
except Exception as e:
    player_image_asset = pg.Surface((80, 80), pg.SRCALPHA)
    pg.draw.circle(player_image_asset, (135, 206, 235), (40, 40), 39)

# 2. 총알 이미지 로드 (30x15 크기 최적화)
try:
    bullet_path = os.path.join(base_path, "assets", "gun.png")
    bullet_asset_raw = pg.image.load(bullet_path).convert_alpha()
    bullet_asset_pre_rotated = pg.transform.rotate(bullet_asset_raw, -90)
    bullet_orig_global = pg.transform.smoothscale(bullet_asset_pre_rotated, (30, 15))
except Exception as e:
    bullet_orig_global = pg.Surface((20, 6), pg.SRCALPHA)
    bullet_orig_global.fill((255, 255, 0)) # 노란색 레이저

# --- 총알 클래스 ---
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pg.transform.rotate(bullet_orig_global, angle)
        self.rect = self.image.get_rect(center=pos) 
        rad = math.radians(angle)
        self.vel = pg.math.Vector2(math.cos(rad), -math.sin(rad)) * 18 

    def update(self):
        self.rect.center += self.vel 
        if self.rect.x < -100 or self.rect.x > 2100 or self.rect.y < -100 or self.rect.y > 1200:
            self.kill()

# --- 플레이어 클래스 ---
class Player(pg.sprite.Sprite):
    def __init__(self, sw=1920, sh=1080):
        super().__init__()
        self.orig = player_image_asset 
        self.image = self.orig
        
        self.pos = pg.math.Vector2(sw/2, sh/2)
        self.rect = self.image.get_rect(center=self.pos)
        
        self.max_hp = 3.0
        self.hp = float(self.max_hp)
        self.current_angle = 0.0 # 이전 각도를 기억할 변수

        # HP BAR 이미지 로드
        self.hp_images = []
        for i in [3, 2, 1]:
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
                s = pg.Surface((409, 70)); s.fill([(250,50,50),(250,200,50),(50,250,50)][i-1])
                self.hp_images.append(s)

    def update(self):
        m_pos = pg.math.Vector2(pg.mouse.get_pos()) 
        self.pos += (m_pos - self.pos) * 0.1 # 관성 이동
        
        rel = m_pos - self.pos
        # 🔴 [팽이 회전 버그 방어막]
        # 마우스 커서와 플레이어의 거리가 10픽셀 이상 멀 때만 각도를 돌립니다.
        # 이 범위 안으로 들어오면 이전 각도(current_angle)를 그대로 유지해서 튕김 현상을 완벽 차단합니다!
        if rel.length() > 10:
            self.current_angle = math.degrees(-math.atan2(rel.y, rel.x))
            
        self.image = pg.transform.rotate(self.orig, self.current_angle)
        self.rect = self.image.get_rect(center=self.pos) 

    def draw_hp_bar(self, surf):
        if self.hp <= 0: return
        img_idx = max(0, min(2, int(self.hp) - 1))
        if 0 <= img_idx < len(self.hp_images):
            surf.blit(self.hp_images[img_idx], (20, 20))