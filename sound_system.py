import pygame as pg
import os

class SoundSystem:
    def __init__(self):
        # 오디오 믹서 최적화 초기화 (버퍼를 줄여 총소리 반응 속도를 극대화)
        if not pg.mixer.get_init():
            pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
        base_path = os.path.dirname(__file__)
        self.gunshot = None

        # 1. 효과음 (총소리) 로드
        gunshot_path = os.path.join(base_path, "assets", "gunshot.wav")
        if os.path.exists(gunshot_path):
            try:
                self.gunshot = pg.mixer.Sound(gunshot_path)
                self.gunshot.set_volume(0.15) # 총소리 볼륨 (0.0 ~ 1.0)
                print("[SoundSystem] 성공: gunshot.wav 효과음 로드 완료!")
            except Exception as e:
                print(f"[SoundSystem] 에러: gunshot.wav 로드 실패 -> {e}")
        else:
            print("[SoundSystem] 경고: assets/gunshot.wav 파일이 없습니다.")

        # 2. 배경음악 (BGM) 로드 및 자동 재생
        bgm_path = os.path.join(base_path, "assets", "bgm.wav")
        if os.path.exists(bgm_path):
            try:
                pg.mixer.music.load(bgm_path)
                pg.mixer.music.set_volume(0.3) # BGM은 총소리보다 조금 작게 세팅 (0.3)
                # -1은 무한 반복 스트리밍을 의미함
                pg.mixer.music.play(-1)
                print("[SoundSystem] 성공: bgm.wav 배경음악 무한 재생 시작!")
            except Exception as e:
                print(f"[SoundSystem] 에러: bgm.wav 로드/재생 실패 -> {e}")
        else:
            print("[SoundSystem] 경고: assets/bgm.wav 파일이 없습니다.")

    def play_gunshot(self):
        """마우스 좌클릭 시 호출"""
        if self.gunshot:
            try:
                self.gunshot.play()
            except Exception as e:
                print(f"[SoundSystem] 총소리 재생 중 일시적 오류: {e}")
                
    def stop_bgm(self):
        """게임오버 시 BGM을 끄고 싶다면 호출"""
        try:
            pg.mixer.music.stop()
        except Exception:
            pass

    def restart_bgm(self):
        """게임 재시작 시 BGM을 다시 켜고 싶다면 호출"""
        try:
            pg.mixer.music.play(-1)
        except Exception:
            pass