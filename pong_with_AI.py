import pygame
import sys
import random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponentAI():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_y, ball_speed_x, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 700:
        three = font.render("3", False, red)
        screen.blit(three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        two = font.render("2", False, orange)
        screen.blit(two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        one = font.render("1", False, light_green)
        screen.blit(one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AI Pong - Michal Kosinski, Aleksandra Formela')

# ball implementation
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

background_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
light_green = (50, 205, 50)
red = (220, 20, 60)
orange = (255, 140, 0)

# Game objects
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Text objects
player_score = 0
opponent_score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# Timer
score_time = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponentAI()

    screen.fill(background_color)
    pygame.draw.rect(screen, light_green, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_restart()
    player_text = font.render(f"{player_score}", False, light_green)
    screen.blit(player_text, (screen_width / 2 + 8, screen_height - 730))

    opponent_text = font.render(f"{opponent_score}", False, red)
    screen.blit(opponent_text, (screen_width / 2 - 24, screen_height - 730))

    pygame.display.flip()
    clock.tick(60)
