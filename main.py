import pygame as pg
import sys
import random
import os
import math
import ctypes # 💡 이거 추가!

# 💡 윈도우 디스플레이 배율(125%, 150%) 강제 무시! (창이 안 커지고 딱 맞게 나옴)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

pg.init()

SW, SH = 1920, 1080
screen = pg.display.set_mode((SW, SH), pg.SCALED)
pg.display.set_caption("Infection Chain")
clock = pg.time.Clock()
pg.mouse.set_visible(False) # 마우스 커서 숨기기

base_path = os.path.dirname(__file__)

# 배경 이미지 로드
try:
    bg_path = os.path.join(base_path, "assets", "background.png")
    background_img = pg.image.load(bg_path).convert()
    background_img = pg.transform.scale(background_img, (SW, SH))
except Exception:
    background_img = None

# 모듈 불러오기
from player import Player, Bullet
from zombie import Zombie
from sound_system import SoundSystem

# 충돌 처리 함수
def handle_collisions(player, bullets_group, zombies_group):
    # 총알과 좀비 충돌
    hits = pg.sprite.groupcollide(bullets_group, zombies_group, True, True)
    added_score = len(hits) * 100

    # 플레이어와 좀비 충돌
    zombie_hits = pg.sprite.spritecollide(player, zombies_group, False)
    if zombie_hits:
        player.hp -= 0.05
        
    return added_score

sound_system = SoundSystem()

# 스프라이트 그룹 세팅
all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
zombies = pg.sprite.Group()

player = Player(SW, SH)
all_sprites.add(player)

start_time = pg.time.get_ticks()
score = 0
zombie_base_speed = 2.5
zombie_spawn_cooldown = 1200
last_spawn_time = pg.time.get_ticks()

font = pg.font.SysFont("malgungothic", 24)
title_font = pg.font.SysFont("malgungothic", 30, bold=True)

def spawn_one_zombie():
    if random.choice([True, False]):
        x = random.choice([10, SW - 10])
        y = random.randint(10, SH - 10)
    else:
        x = random.randint(10, SW - 10)
        y = random.choice([10, SH - 10])
    
    new_zombie = Zombie(x, y, base_speed=zombie_base_speed)
    all_sprites.add(new_zombie)
    zombies.add(new_zombie)

# 최초 좀비 스폰
for _ in range(3): spawn_one_zombie()

running = True
game_over = False

while running:
    current_time = pg.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000 if not game_over else elapsed_time
    current_spawn_cooldown = max(400, zombie_spawn_cooldown - (int(elapsed_time // 10) * 100))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
        elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1: # 왼쪽 클릭 시 총알 발사
                sound_system.play_gunshot()
                m = pg.mouse.get_pos()
                ang = math.degrees(-math.atan2(m[1]-player.pos.y, m[0]-player.pos.x))
                
                new_bullet = Bullet(player.pos, ang)
                all_sprites.add(new_bullet)
                bullets.add(new_bullet)
                
        elif event.type == pg.KEYDOWN:
            if game_over and event.key == pg.K_r: # 재시작
                all_sprites.empty()
                bullets.empty()
                zombies.empty()
                player = Player(SW, SH)
                all_sprites.add(player)
                start_time = pg.time.get_ticks()
                last_spawn_time = pg.time.get_ticks()
                score = 0
                game_over = False
                sound_system.restart_bgm()
                for _ in range(3): spawn_one_zombie()

    # --- 업데이트 루프 ---
    if not game_over:
        # 🔴 [TypeError 에러 완전 해결] 
        # 인자가 필요 없는 플레이어와 총알만 골라서 먼저 업데이트합니다.
        player.update()
        bullets.update()
        
        # 자동 좀비 스폰
        if current_time - last_spawn_time > current_spawn_cooldown:
            spawn_one_zombie()
            last_spawn_time = current_time

        # 좀비는 직접 필요한 재료들을 찔러 넣어주며 업데이트!
        for zombie in zombies:
            zombie.update(player.rect, elapsed_time)

        # 충돌 및 스코어 처리
        score += handle_collisions(player, bullets, zombies)

        # 게임오버 트리거
        if player.hp <= 0:
            player.hp = 0
            game_over = True
            sound_system.stop_bgm()

    # --- 렌더링 영역 ---
    if background_img: screen.blit(background_img, (0, 0))
    else: screen.fill((25, 25, 35))

    all_sprites.draw(screen)
    player.draw_hp_bar(screen)

    ui_width = 340
    ui_x = SW - ui_width - 40  # 화면 우측 끝(SW) 기준 상대 좌표로 변경!
    
    pg.draw.rect(screen, (40, 40, 50), (ui_x, 30, ui_width, 180), border_radius=10)
    screen.blit(title_font.render("[실시간 대시보드]", True, (100, 255, 100)), (ui_x + 25, 45))
    screen.blit(font.render(f"생존 시간: {elapsed_time:.1f}초", True, (255, 255, 255)), (ui_x + 25, 90))
    screen.blit(font.render(f"현재 점수: {score}점", True, (255, 255, 255)), (ui_x + 25, 125))
    screen.blit(font.render(f"좀비 개체: {len(zombies)}마리", True, (255, 150, 150)), (ui_x + 25, 160))

    # 게임오버 화면
    if game_over:
        overlay = pg.Surface((SW, SH), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        pg.draw.rect(screen, (30, 30, 30), (710, 390, 500, 300), border_radius=15)
        screen.blit(title_font.render("GAME OVER", True, (255, 50, 50)), (880, 420))
        screen.blit(font.render(f"최종 생존 시간: {elapsed_time:.1f}초", True, (255, 255, 255)), (850, 490))
        screen.blit(font.render(f"최종 획득 점수: {score}점", True, (255, 255, 255)), (850, 530))
        screen.blit(font.render("다시 시작하려면 [ R ] 입력", True, (100, 255, 100)), (810, 600))

    # 녹색 십자 조준선
    if not game_over:
        m_pos = pg.mouse.get_pos()
        pg.draw.line(screen, (0, 255, 0), (m_pos[0] - 15, m_pos[1]), (m_pos[0] + 15, m_pos[1]), 2)
        pg.draw.line(screen, (0, 255, 0), (m_pos[0], m_pos[1] - 15), (m_pos[0], m_pos[1] + 15), 2)

    pg.display.flip()
    clock.tick(100)

pg.quit()
sys.exit()