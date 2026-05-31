import pygame as pg
import math
import os

class Zombie(pg.sprite.Sprite):
    def __init__(self, start_x, start_y, base_speed=2.0):
        super().__init__()
        
        base_path = os.path.dirname(__file__)
        loaded = False
        
        # 🔴 [오타 전면 수정] 기존 pg.load -> pg.image.load로 철자 정상 교체 완료!
        for name in ["zombie.png", "ZOMBIE.PNG"]:
            try:
                path = os.path.join(base_path, "assets", name)
                if os.path.exists(path):
                    self.image = pg.image.load(path).convert_alpha() # <- 여기서 오타가 났었습니다!
                    self.image = pg.transform.scale(self.image, (120, 120)) # 플레이어 비율 맞춤
                    loaded = True
                    break
            except Exception as e:
                print(f"[Zombie] 에셋 로드 중 미세 오류 패스: {e}")
                continue
                
        if not loaded:
            # 최종 실패 시 방어용 사각형
            self.image = pg.Surface((50, 50))
            self.image.fill((255, 50, 50)) 

        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        self.base_speed = base_speed
        self.current_speed = base_speed
        self.max_speed = base_speed * 3.0

    def update(self, player_rect, elapsed_time):
        self.update_speed(elapsed_time)
        self.track_player(player_rect.centerx, player_rect.centery)

    def track_player(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance > 1.0:
            move_x = (dx / distance) * self.current_speed
            move_y = (dy / distance) * self.current_speed
            
            self.pos_x += move_x
            self.pos_y += move_y
            
            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y)

    def update_speed(self, elapsed_time):
        speed_level = int(elapsed_time // 10)
        new_speed = self.base_speed + (speed_level * 0.4)
        self.current_speed = min(new_speed, self.max_speed)