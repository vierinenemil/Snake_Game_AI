import pygame
import random

# initialize Pygame
pygame.init()

# define screen size and create a screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set up the clock
clock = pygame.time.Clock()

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# set up the player's car
player_width = 80
player_height = 150
player_x = SCREEN_WIDTH / 2 - player_width / 2
player_y = SCREEN_HEIGHT - player_height - 50
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# set up the enemy cars
enemy_width = 80
enemy_height = 150
enemy_speed = 3
enemies = []
for i in range(3):
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(-SCREEN_HEIGHT, -enemy_height)
    enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append(enemy)

# set up the font
font = pygame.font.SysFont(None, 30)

# set up the score
score = 0

# main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # move the player's car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player_width:
        player.x += player_speed

    # move the enemy cars
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > SCREEN_HEIGHT:
            enemy.x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy.y = random.randint(-SCREEN_HEIGHT, -enemy_height)
            score += 1

        # check for collision with player's car
        if player.colliderect(enemy):
            running = False

    # clear the screen
    screen.fill(WHITE)

    # draw the player's car
    pygame.draw.rect(screen, RED, player)

    # draw the enemy cars
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, enemy)

    # draw the score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # update the screen
    pygame.display.update()

    # limit the frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()
