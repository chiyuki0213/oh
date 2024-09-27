import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up window size
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG Adventure")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up fonts
font = pygame.font.Font(None, 36)

# Load background image
background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game states
START_STATE, STORY_STATE1, STORY_STATE2, STORY_STATE3, BATTLE_STATE, WIN_STATE, LOSE_STATE = range(7)
game_state = START_STATE

# Function to calculate damage with a possible critical hit
def get_hurt(attacker_name, attack, defense, critical_hit_chance):
    critical_random = random.randint(1, 100)
    damage = attack
    if critical_random <= critical_hit_chance:
        print(f"{attacker_name} landed a CRITICAL HIT!")
        damage *= 2
    return max(0, damage - defense)

# Character class to represent player and boss
class Character:
    def __init__(self, name, hp, attack, defense, critical_hit_chance):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.critical_hit_chance = critical_hit_chance

    def is_alive(self):
        return self.hp > 0
    
    def hurt(self, value):
        self.hp -= max(0, value)
        self.hp = max(0, self.hp)

    def print_status(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp}, Atk: {self.attack}, Def: {self.defense})"

# Function to draw text on screen
def draw_text(text, x, y, color):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        img = font.render(line, True, color)
        screen.blit(img, (x, y + i * 40))

# Function to draw health bar
def draw_health_bar(character, x, y):
    bar_width = 300
    bar_height = 30
    fill = (character.hp / character.max_hp) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, fill, bar_height))

# Function to get player name from input box
def input_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30, 300, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(background_img, (0, 0))
        txt_surface = font.render(text, True, color)
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text("Enter your name and press Enter:", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, WHITE)
        pygame.display.flip()

# Get player name from input
player_name = input_name()
player = Character(player_name, 300, 60, 25, 20)
boss = Character("Boss", 700, 40, 35, 10)

# Different player attacks with varying damage and flavor text
player_attacks = [
    {"name": "Sword Slash", "damage": 50},
    {"name": "Fireball", "damage": 40},
    {"name": "Lightning Strike", "damage": 60},
]
boss_attacks = [
    {"name": "Claw Swipe", "damage": 30},
    {"name": "Tail Whip", "damage": 25},
    {"name": "Fire Breath", "damage": 50},
]

# Main game loop
turn = "player"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handling transitions between story states
            if game_state in [START_STATE, STORY_STATE1, STORY_STATE2, STORY_STATE3] and event.key == pygame.K_SPACE:
                if game_state == START_STATE:
                    game_state = STORY_STATE1
                elif game_state == STORY_STATE1:
                    game_state = STORY_STATE2
                elif game_state == STORY_STATE2:
                    game_state = STORY_STATE3
                elif game_state == STORY_STATE3:
                    game_state = BATTLE_STATE
            # Handling battle state
            elif game_state == BATTLE_STATE and event.key in [pygame.K_SPACE, pygame.K_a, pygame.K_b, pygame.K_c]:
                if turn == "player":
                    attack = random.choice(player_attacks)
                    damage = get_hurt(player.name, attack["damage"], boss.defense, player.critical_hit_chance)
                    boss.hurt(damage)
                    print(f"{player.name} used {attack['name']}! It dealt {damage} damage.")
                    turn = "boss"
                if turn == "boss" and boss.is_alive():
                    attack = random.choice(boss_attacks)
                    damage = get_hurt(boss.name, attack["damage"], player.defense, boss.critical_hit_chance)
                    player.hurt(damage)
                    print(f"{boss.name} used {attack['name']}! It dealt {damage} damage.")
                    turn = "player"
                if not player.is_alive():
                    game_state = LOSE_STATE
                if not boss.is_alive():
                    game_state = WIN_STATE
            # Handling end game states
            elif game_state in [WIN_STATE, LOSE_STATE] and event.key == pygame.K_SPACE:
                running = False

    screen.blit(background_img, (0, 0))

    if game_state == START_STATE:
        draw_text("Press SPACE to start the game", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, WHITE)
    elif game_state == STORY_STATE1:
        draw_text("You are a brave adventurer seeking fame and fortune.", 20, 50, WHITE)
        draw_text("After hearing rumors of a mysterious cave, you decide to explore it.", 20, 100, WHITE)
        draw_text("Press SPACE to continue...", 20, 150, WHITE)
    elif game_state == STORY_STATE2:
        draw_text("Deep in the cave, you find ancient writings hinting at a hidden treasure.", 20, 50, WHITE)
        draw_text("Suddenly, a loud roar echoes through the cave. You ready your weapon.", 20, 100, WHITE)
        draw_text("Press SPACE to continue...", 20, 150, WHITE)
    elif game_state == STORY_STATE3:
        draw_text("A monstrous creature emerges from the shadows, blocking your path.", 20, 50, WHITE)
        draw_text("You must defeat the monster to reach the treasure.", 20, 100, WHITE)
        draw_text("Press SPACE to battle...", 20, 150, WHITE)
    elif game_state == BATTLE_STATE:
        draw_text(player.print_status(), 20, 20, WHITE)
        draw_health_bar(player, 20, 60)
    
        draw_text(boss.print_status(), 500, 20, WHITE)
        draw_health_bar(boss, 500, 60)
    
        if turn == "player":
            draw_text("Player's Turn: Press SPACE to attack", 20, 200, WHITE)
        else:
            draw_text("Monster's Turn: Press SPACE to defend yourself", 20, 200, WHITE)
    elif game_state == WIN_STATE:
        draw_text("Victory! You defeated the monster and claimed the treasure!", SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 20, GREEN)
    elif game_state == LOSE_STATE:
        draw_text("Game Over! The monster defeated you.", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, RED)

    pygame.display.flip()

pygame.quit()
sys.exit()
