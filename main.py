import pygame
import random

# Import your custom button class
from buttonWithTextBox import ButtonWithTextBox

# Initialize Pygame
pygame.init()
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Retro Snake')

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
text_col = white

# Clock
clock = pygame.time.Clock()
FPS = 15

# Game state variables
game_state = 'main'
score = 0
play_area_x = 50
play_area_y = 150
play_area_width =500
play_area_height = 500

# Button definitions
# Button definitions
pause_btn = ButtonWithTextBox(350, 15, "Pause", None, 20, text_col, black, white, 10, 2, 70, 30)
mainMenu_button = ButtonWithTextBox(50, 15, "Main", None, 20, text_col, black, white, 10, 2, 70, 30)
start_button = ButtonWithTextBox(50, 480, "Start", "Hokjesgeest-PDGB.ttf", 20, text_col, black, white, 10, 2, hover_scale=1.1)
exit_button = ButtonWithTextBox(200, 480, "Exit", "MinecraftEvenings-lgvPd.ttf", 20, text_col, black, white, 10, 2, hover_scale=1.1)
resume_button = ButtonWithTextBox(200, 280, "Resume", None, 40, text_col, black, white, 10, 2, hover_scale=1.1)
play_again_button = ButtonWithTextBox(50, 480, "Play Again", None, 30, text_col, black, white, 10, 2, hover_scale=1.1)
main_menu_button = ButtonWithTextBox(200, 480, "Main Menu", None, 30, text_col, black, white, 10, 2, hover_scale=1.1)

# Text drawing function with border
def draw_text_with_border(screen, text, font_path, text_col, border_col, x, y, border_thickness):
    font = pygame.font.Font(font_path, 50)  # Adjust font size as needed
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:
                img = font.render(text, True, border_col)
                screen.blit(img, (x + dx, y + dy))
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Player class
class Player:
    def __init__(self):
        self.position = [play_area_x + play_area_width//2, play_area_y + play_area_height//2]#[100, 50]
        self.body = [[play_area_x + play_area_width//2, play_area_y + play_area_height//2],
                           [play_area_x + play_area_width//2 - 10, play_area_y + play_area_height//2],
                           [play_area_x + play_area_width//2 - 20, play_area_y + play_area_height//2]]#[[100, 50], [90, 50], [80, 50], [70, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_dir_to(self, dir):
        if dir == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if dir == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'
        if dir == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if dir == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        if self.direction == 'UP':
            self.position[1] -= 10
        if self.direction == 'DOWN':
            self.position[1] += 10
        if self.direction == 'LEFT':
            self.position[0] -= 10
        if self.direction == 'RIGHT':
            self.position[0] += 10

        self.body.insert(0, list(self.position))
        if self.position[0] == fruit.position[0] and self.position[1] == fruit.position[1]:
            global score
            score += 10
            fruit.spawn()
        else:
            self.body.pop()

    def draw(self, surface):
        for pos in self.body:
            pygame.draw.rect(surface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_collision(self):
        if self.position[0] < 0 or self.position[0] > play_area_width - 10:
            return True
        if self.position[1] < 0 or self.position[1] > play_area_height - 10:
            return True
        for block in self.body[1:]:
            if self.position[0] == block[0] and self.position[1] == block[1]:
                return True
        return False

# Fruit class
class Fruit:
    def __init__(self):
        self.position = [random.randrange(play_area_x//10, (play_area_x + play_area_width)//10) * 10,
                         random.randrange(play_area_y//10, (play_area_y + play_area_height)//10) * 10]
        self.is_spawned = True

    def spawn(self):
        self.position = [random.randrange(play_area_x//10, (play_area_x + play_area_width)//10) * 10,
                         random.randrange(play_area_y//10, (play_area_y + play_area_height)//10) * 10]
        self.is_spawned = True

    def draw(self, surface):
        pygame.draw.rect(surface, white, pygame.Rect(self.position[0], self.position[1], 10, 10))

# Initialize player and fruit
player = Player()
fruit = Fruit()

# Game loop
run = True
while run:
    clock.tick(FPS)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.change_dir_to('UP')
            if event.key == pygame.K_DOWN:
                player.change_dir_to('DOWN')
            if event.key == pygame.K_LEFT:
                player.change_dir_to('LEFT')
            if event.key == pygame.K_RIGHT:
                player.change_dir_to('RIGHT')

    if game_state == 'main':
        draw_text_with_border(screen, "RETRO SNAKE", "MinecraftEvenings-lgvPd.ttf", text_col, green, 70, 250, 3)
        if start_button.draw(screen):
            player = Player()
            fruit = Fruit()
            score = 0
            game_state = 'playtime'
        if exit_button.draw(screen):
            run = False

    elif game_state == 'playtime':
        #creation of border as play area
        pygame.draw.rect(screen, red, pygame.Rect(play_area_x, play_area_y, play_area_width, play_area_height), 5)
        draw_text_with_border(screen, f"Score: {score}", "MinecraftEvenings-lgvPd.ttf", text_col, green, 120, 50, 3)
        player.move()
        player.draw(screen)
        fruit.draw(screen)

 #       if player.check_collision():
 #           game_state = 'wasted'
        if (player.position[0] < play_area_x or player.position[0] >= play_area_x + play_area_width or
            player.position[1] < play_area_y or player.position[1] >= play_area_y + play_area_height):
            game_state = 'wasted'
        for block in player.body[1:]:
            if player.position[0] == block[0] and player.position[1] == block[1]:
                game_state = 'wasted'

        if pause_btn.draw(screen):
            game_state = 'paused'

    elif game_state == 'paused':
        player.draw(screen)
        fruit.draw(screen)
        if resume_button.draw(screen):
            game_state = 'playtime'
        if main_menu_button.draw(screen):
            game_state = 'main'

    elif game_state == 'wasted':
        draw_text_with_border(screen, "WASTED", "MinecraftEvenings-lgvPd.ttf", text_col, red, 70, 250, 3)
        draw_text_with_border(screen, f"Score: {score}", "MinecraftEvenings-lgvPd.ttf", text_col, red, 70, 350, 3)
        if play_again_button.draw(screen):
            player = Player()
            fruit = Fruit()
            score = 0
            game_state = 'playtime'
        if main_menu_button.draw(screen):
            game_state = 'main'

    pygame.display.update()

pygame.quit()
