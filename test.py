import pygame
import random
import math

# --- 1. Pygame 초기화 및 기본 설정 ---
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("클래스 기반 슈팅 게임")

# 색상 정의 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- 2. Enemy 클래스 정의 (적군) ---
class Enemy:
    """적군 객체의 데이터와 동작을 캡슐화한 클래스"""
    def __init__(self, color, speed_multiplier):
        # 데이터 초기화
        self.color = color 
        self.radius = 15
        self.speed = 2 * speed_multiplier

        # 초기 위치는 화면 위쪽 랜덤 위치
        self.reset_position()

    def reset_position(self):
        """적군이 화면 밖으로 나갔을 때 위치를 재설정"""
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        # 화면 위쪽 -200 ~ 0 사이에서 시작하여 적군이 화면으로 내려오는 것을 보이게 함
        self.y = random.randint(-200, 0) - self.radius

    def update(self):
        """적군의 위치를 업데이트하고 화면에 그리기"""
        self.y += self.speed

        # 화면 밖으로 나가면 위치 리셋
        if self.y > SCREEN_HEIGHT + self.radius:
            self.reset_position()

        # 화면에 그리기
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# --- 3. Player 클래스 정의 (아군 우주선) ---
class Player:
    """아군 우주선 객체의 데이터와 동작을 캡슐화한 클래스"""
    def __init__(self):
        self.color = BLUE
        self.radius = 20
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 5

    def move(self, direction):
        """키 입력에 따라 좌우로 이동"""
        if direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed

        # 화면 경계 제한
        if self.x < self.radius:
            self.x = self.radius
        elif self.x > SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius

    def draw(self):
        """우주선을 화면에 그리기"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# --- 4. 객체 생성 및 초기화 ---

# 4-1. 아군 우주선 생성
player = Player()

# 4-2. 적군 생성 (빨간색 4개, 녹색 4개)
enemies = []

# 빨간 적군 10개 (기본 속도)
for _ in range(10):
    enemies.append(Enemy(RED, random.uniform(1, 1.5))) # speed_multiplier = 1.0

# 녹색 적군 10개 (조금 더 빠른 속도)
for _ in range(10):
    enemies.append(Enemy(GREEN, random.uniform(1, 1.5))) # speed_multiplier = 1.5

# --- 5. 게임 루프 ---
running = True
clock = pygame.time.Clock() # 프레임 속도 제어를 위해

while running:
    # 5-1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 5-2. 키 입력 처리 (아군 이동)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("LEFT")
    if keys[pygame.K_RIGHT]:
        player.move("RIGHT")

    # 5-3. 화면 업데이트 (그리기)
    screen.fill(BLACK) # 배경을 검정색으로 지우기

    # 아군 그리기
    player.draw()

    # 적군 업데이트 및 그리기 (클래스 덕분에 간단하게 반복문 처리)
    for enemy in enemies:
        enemy.update()

    # 5-4. 화면 버퍼 교체 및 프레임 속도 제어
    pygame.display.flip()
    clock.tick(60) # 60 FPS로 제한

pygame.quit()


