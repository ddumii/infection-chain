import pygame
import sys
from zombie import Zombie  # 우리가 만든 좀비 설계도 불러오기!

# 1. 파이게임 초기화 및 창 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Zombie AI Test - 마우스를 도망쳐라!")
clock = pygame.time.Clock()

# 2. 좀비 한 마리 소환 (왼쪽 위 구석 100, 100 위치)
test_zombie = Zombie(100, 100)

# 가짜 플레이어 박스 만들기 (마우스 위치를 담을 용도)
dummy_player_rect = pygame.Rect(0, 0, 40, 40)

# 시작 시간 (좀비 속도 증가 테스트용)
start_time = pygame.time.get_ticks()

print("테스트 시작! 마우스를 화면 안에서 요리조리 움직여보세요.")

# 3. 테스트용 무한 루프
running = True
while running:
    # 경과 시간 계산
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 마우스 위치를 가져와서 가짜 플레이어의 위치로 설정
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dummy_player_rect.center = (mouse_x, mouse_y)

    # 좀비 업데이트! (마우스 위치를 넘겨주면서 쫓아오라고 명령)
    test_zombie.update(dummy_player_rect, elapsed_time)

    # --- 화면 그리기 ---
    screen.fill((50, 50, 50)) # 배경을 진한 회색으로 지우기

    # 마우스 위치(가짜 플레이어)에 빨간색 점 그리기
    pygame.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 5)
    
    # 좀비 그리기
    screen.blit(test_zombie.image, test_zombie.rect)

    pygame.display.flip()
    clock.tick(60) # 60 FPS

pygame.quit()
sys.exit()