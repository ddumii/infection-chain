import pygame
import os

class SoundSystem:
    """
    네가 준비한 4가지 사운드에 최적화된 매니저 클래스
    """
    def __init__(self):
        # 1. 믹서 초기화
        pygame.mixer.init()
        self.sounds = {}
        
        # 2. 볼륨 기본값 설정 (배경음은 좀 작게, 효과음은 빵빵하게)
        self.bgm_volume = 0.4
        self.sfx_volume = 0.8

    def load_all_sounds(self):
        """
        게임 시작 전에 한 번에 모든 사운드를 불러오는 함수
        """
        # --- [1] 배경음(BGM) 로드 ---
        # Pygame에서 배경음은 보통 mp3나 ogg 파일을 쓴다.
        bgm_path = 'assets/bgm.wav' # 네 파일 이름에 맞게 수정해!
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(self.bgm_volume)
            print("[SoundSystem] BGM 로드 완료")
        else:
            print("[SoundSystem] 경고: BGM 파일이 없습니다.")

        # --- [2] 효과음(SFX) 로드 ---
        # Pygame에서 효과음은 .wav 확장자가 딜레이 없이 가장 잘 터진다.
        sfx_files = {
            'gunshot': 'assets/gunshot.wav',
            'zombie_spawn': 'assets/zombie_spawn.wav',
            'reload': 'assets/reload.wav'
        }

        for name, path in sfx_files.items():
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
                print(f"[SoundSystem] SFX 로드 완료: {name}")
            else:
                print(f"[SoundSystem] 경고: {name} 파일이 없습니다. 경로: {path}")

    # --- 재생 관련 함수들 ---
    def play_bgm(self):
        """배경음악 무한 반복 재생"""
        try:
            pygame.mixer.music.play(-1) # -1은 무한반복을 의미함
        except:
            pass

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def play_sfx(self, name):
        """이름을 입력하면 해당 효과음을 재생"""
        if name in self.sounds:
            self.sounds[name].play()

# 1. 우리가 만든 사운드 시스템 설계도(Class)를 불러온다.
from sound_system import SoundSystem

# 2. 설계도를 바탕으로 실제 '사운드 기계(객체)'를 하나 제작해서 변수에 담는다. 
# (이때 __init__ 함수가 스르륵 실행되면서 기본 세팅이 됨!)
my_audio = SoundSystem()

# 3. 이제 만들어진 그 기계(my_audio)의 버튼(함수)을 누른다!
my_audio.load_all_sounds()

#사운드 확인
#my_audio.play_bgm()
#my_audio.play_sfx('zombie_spawn')
#my_audio.play_sfx('reload')