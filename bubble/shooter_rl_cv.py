import cv2
import numpy as np
import pyautogui
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import time
import keyboard

class BubbleShooterEnv(gym.Env):
    def __init__(self):
        super(BubbleShooterEnv, self).__init__()
        
        self.action_space = spaces.Discrete(180)  # 0-179도
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)
        
        self.score = 0
        self.moves = 0
        self.max_moves = 50  # 최대 이동 횟수
        self.game_region = None
        
    def select_game_region(self):
        print("게임 화면을 드래그하여 선택하세요. 준비되면 Enter 키를 누르세요. (ESC를 누르면 종료)")
        while True:
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("프로그램을 종료합니다.")
                exit()
            time.sleep(0.1)
        print("이제 게임 화면을 드래그하세요.")
        self.game_region = pyautogui.screenshot(region=pyautogui.dragTo())
        self.game_region = np.array(self.game_region)
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if self.game_region is None:
            self.select_game_region()
        self.score = 0
        self.moves = 0
        time.sleep(1)  # 게임 재시작을 위한 대기 시간
        return self._get_observation(), {}  # 초기 정보 딕셔너리 반환
    
    def step(self, action):
        self._execute_action(action)
        self.moves += 1
        
        observation = self._get_observation()
        reward = self._calculate_reward()
        done = self.moves >= self.max_moves
        terminated = done
        truncated = False
        
        return observation, reward, terminated, truncated, {"score": self.score}
    
    def _get_observation(self):
        screenshot = pyautogui.screenshot(region=pyautogui.dragTo())
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (84, 84))
        return frame
    
    def _execute_action(self, action):
        # 게임 화면의 중앙 하단을 발사 위치로 가정
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        bottom_y = screen_height - 10
        
        # 각도를 라디안으로 변환
        angle_rad = np.radians(action)
        
        # 발사 위치에서 각도에 따라 목표 지점 계산
        target_x = int(center_x + np.cos(angle_rad) * 100)
        target_y = int(bottom_y - np.sin(angle_rad) * 100)
        
        # 마우스 이동 및 클릭
        pyautogui.moveTo(center_x, bottom_y)
        pyautogui.dragTo(target_x, target_y, duration=0.2)
        pyautogui.click()
        
        time.sleep(0.5)  # 액션 후 대기 시간
    
    def _calculate_reward(self):
        # 간단한 색상 분석을 통한 점수 계산 (예시)
        screenshot = pyautogui.screenshot(region=pyautogui.dragTo())
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2HSV)
        
        # 특정 색상 범위의 버블이 제거되었는지 확인
        lower_blue = np.array([100,50,50])
        upper_blue = np.array([130,255,255])
        blue_mask = cv2.inRange(frame, lower_blue, upper_blue)
        blue_count = np.sum(blue_mask > 0)
        
        # 이전 프레임과 비교하여 제거된 버블 수 계산
        if hasattr(self, 'prev_blue_count'):
            removed_bubbles = max(0, self.prev_blue_count - blue_count)
            self.score += removed_bubbles
            reward = removed_bubbles
        else:
            reward = 0
        
        self.prev_blue_count = blue_count
        return reward

# 환경 생성
env = DummyVecEnv([lambda: BubbleShooterEnv()])

# 모델 생성 및 학습
model = PPO("CnnPolicy", env, verbose=1, 
            learning_rate=0.0003, 
            n_steps=2048, 
            batch_size=64, 
            n_epochs=10, 
            gamma=0.99, 
            gae_lambda=0.95, 
            clip_range=0.2, 
            ent_coef=0.0,
            device='cpu')

print("모델 학습을 시작합니다. 게임 화면을 준비한 후 Enter 키를 누르세요. (ESC를 누르면 종료)")
while True:
    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('esc'):
        print("프로그램을 종료합니다.")
        exit()
    time.sleep(0.1)

try:
    model.learn(total_timesteps=100000)
except KeyboardInterrupt:
    print("학습이 중단되었습니다.")

# 학습된 모델 저장
model.save("bubble_shooter_ppo_cv")

print("학습된 모델을 사용합니다. 게임 화면을 준비한 후 Enter 키를 누르세요. (ESC를 누르면 종료)")
while True:
    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('esc'):
        print("프로그램을 종료합니다.")
        exit()
    time.sleep(0.1)

obs, _ = env.reset()
try:
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, _, info = env.step(action)
        if dones:
            obs, _ = env.reset()
        if keyboard.is_pressed('esc'):
            print("프로그램을 종료합니다.")
            break
except KeyboardInterrupt:
    print("프로그램이 중단되었습니다.")

print("프로그램이 종료되었습니다.")
