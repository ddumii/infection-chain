def handle_collisions(player, bullets_group, zombies_group):
    """
    게임 내 모든 충돌을 처리하는 독립 모듈
    """
    # 1. 총알과 좀비의 충돌 처리 (부딪히면 둘 다 삭제)
    pg.sprite.groupcollide(bullets_group, zombies_group, True, True)

    # 2. 플레이어와 좀비의 충돌 처리
    # 좀비 그룹 내의 객체 중 플레이어와 겹치는 게 있는지 확인 (삭제는 안 함: False)
    zombie_hits = pg.sprite.spritecollide(player, zombies_group, False)
    
    if zombie_hits:
        # 100 FPS 기준, 매 프레임 0.05씩 부드럽게 감소 (약 0.6초간 비벼지면 체력 3 소멸)
        player.hp -= 0.05