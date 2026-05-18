import pygame
import math

class Zombie(pygame.sprite.Sprite):
    """
    기획서 [Zombie 클래스] 구현체
    역할: 좀비 생성, 플레이어 추적(AI), 이동 처리, 속도 증가 처리
    """
    def __init__(self, start_x, start_y, base_speed=2.0):
        super().__init__()
        
        # 1. 좀비 생성 (임시 디자인 - 초록색 네모)
        # 나중에 실제 좀비 이미지로 바꿀 때는 self.image = pygame.image.load('zombie.png') 등을 사용
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 200, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        
        # 정밀한 대각선 이동을 위한 float 좌표계 보관
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        # 이동 속도 설정
        self.base_speed = base_speed
        self.current_speed = base_speed
        
        # 속도 증가 한계치 (기본 속도의 3배까지만 빨라지도록 제한)
        self.max_speed = base_speed * 3.0

    def update(self, player_rect, elapsed_time):
        """
        Game Manager의 게임 루프에서 매 프레임 호출될 함수.
        player_rect: 플레이어의 Rect 객체 (위치 파악용)
        elapsed_time: 게임 시작 후 경과 시간(초)
        """
        # 난이도(속도) 업데이트
        self.update_speed(elapsed_time)
        
        # 플레이어 추적 및 이동
        self.track_player(player_rect.centerx, player_rect.centery)

    def track_player(self, target_x, target_y):
        """
        플레이어 위치를 향해 이동하는 추적 AI 및 이동 처리
        """
        # 목표물(플레이어)과의 거리와 방향 계산
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        
        # 거리가 0이 아닐 때만 이동 (0으로 나누기 방지 및 덜덜거림 방지)
        if distance > 1.0:
            # 방향 벡터 정규화(Normalize) 후 현재 속도 적용
            move_x = (dx / distance) * self.current_speed
            move_y = (dy / distance) * self.current_speed
            
            # 실제 float 좌표 업데이트
            self.pos_x += move_x
            self.pos_y += move_y
            
            # 화면 출력을 위해 정수형으로 변환하여 rect에 적용
            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y)

    def update_speed(self, elapsed_time):
        """
        게임 진행 시간에 따른 이동 속도 증가 처리 (난이도 조절)
        """
        # 10초 단위로 난이도(속도) 증가 레벨 계산
        speed_level = int(elapsed_time // 10)
        
        # 새로운 속도 계산 (레벨당 0.5씩 증가)
        new_speed = self.base_speed + (speed_level * 0.5)
        
        # 최대 속도를 넘지 않도록 안전장치 적용
        self.current_speed = min(new_speed, self.max_speed)