# Opis gry i zasaad: https://pl.wikipedia.org/wiki/Pong
# Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402
# Instrukcja przygotowania środowiska:
# 1. Upewniamy się, że korzystamy z wersji interpretera wyższej od 3.0 - w przeciwnym razie występują problemy z instalacją biblioteki pygame
# 2. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install pygame
# 3. W razie nieaktualnej wersji pip dokunujemy podwyższenia wersji za pomocą komendy: python -m pip install --upgrade pip
# 4. (Warunkowo) Jeśli wersja pip była nieaktualna, to ponownie używamy komendy pip install pygame, by poprawnie zainstalować biblotekę

import pygame
import sys
import random
import math

pygame.init()

global light_grey, light_green, red, orange, font
light_grey = (200, 200, 200)
light_green = (50, 205, 50)
red = (220, 20, 60)
orange = (255, 140, 0)
font = pygame.font.Font("freesansbold.ttf", 32)
"""
Global variables
"""


class Ball(object):
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        """
        The constructor for Ball class.

        Parameters:
            x (float): x coordinate
            y (float): y coordinate
            width (int): of a ball
            height (int): of a ball
            color (tuple): of a ball
        """
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, board, racketPlayer, racketOpponent):
        """
        The function to move ball in x and y directions

        Parameters:
            board
            racketPlayer
            racketOpponent
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x > board.width:
            self.speed_x *= -1

        if self.rect.y < 0 or self.rect.y > board.height:
            self.speed_y *= -1

        # dla ai
        if self.rect.colliderect(racketPlayer.rect):
            self.speed_x *= -1.2

        if self.rect.colliderect(racketOpponent.rect):
            self.speed_x *= -1.2

    def restart(self, board, current_time, score_time):
        """
        The function to restart the game after winning or losing the match

        Parameters:
            board(Board): board object
            current_time (int): in ticks. Gets the current time
            score_time (int): in ticks. Gets the score time

            Returns:
            score_time (int): in ticks. Gets the score time
            OR:
            None
        """
        self.rect.center = (board.width / 2, board.height / 2)

        if current_time - score_time < 2100:
            self.speed_x, self.speed_y = 0, 0
            return score_time
        else:
            self.speed_y = 7 * random.choice((1, -1))
            self.speed_x = 7 * random.choice((1, -1))
            return None

    def draw(self, board):
        """
        The function to draw the ball on the board

        Parameters:
        board (Board): board object
        """
        pygame.draw.ellipse(board.screen, self.color, self.rect)


class Racket(object):
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        """
        The constructor for Racket class.

        Parameters:
            x and y coordinates
            width (int): of a racket
            height (int): of a racket
            color (tuple): of a racket
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, board):
        """
        The function to draw the racket on the board

        Parameters:
            board (Board): board object
        """
        pygame.draw.rect(board.screen, self.color, self.rect)


class Player(object):
    def __init__(self, racket, speed):
        """
        The constructor for Player class.

        Parameters:
            racket (Racket): racket object
            speed (float): speed of the racket
        """
        self.racket = racket
        self.speed = speed
        self.score = 0


class HumanPlayer(Player):
    def __init__(self, racket, speed):
        """
        The constructor for HumanPlayer class that inheirts from class Player

        Parameters:
            racket (Racket): racket object
            speed (float): speed of the racket
        """
        super(HumanPlayer, self).__init__(racket, speed)

    def move(self, board):
        """
        The function to move HumnanPlayer

        Parameters:
        board (Board): board object
        """
        self.racket.rect.y += self.speed
        if self.racket.rect.top <= 0:
            self.racket.rect.top = 0
        if self.racket.rect.bottom >= board.height:
            self.racket.rect.bottom = board.height


class AiPlayer(Player):
    def __init__(self, racket, speed):
        """
        The constructor for AiPlayer class that inheirts from class Player

        Parameters:
            racket (Racket): racket object
            speed (float): speed of the racket
        """
        super(AiPlayer, self).__init__(racket, speed)

    def move(self, board, ball):
        """
        The function to move AiPlayer racket in x and y directions

        Parameters:
            board (Board): board object
            ball (Ball): ball object
        """
        if self.racket.rect.top < ball.rect.y - 50:
            self.racket.rect.top += self.speed
        if self.racket.rect.bottom > ball.rect.y + 50:
            self.racket.rect.bottom -= self.speed
        if self.racket.rect.top <= 0:
            self.racket.rect.top = 0
        if self.racket.rect.bottom >= board.height:
            self.racket.rect.bottom = board.height


class PongGame(object):
    """
    Pong window mode game with AI opponent based on Two Players Game from pyGame Python library
    """

    def __init__(self, width, height):
        """
        The constructor for PongGame class.

        Parameters:
            widht (int): of the game window
            height (int): of the game window
        """

        self.board = Board(width, height)
        self.ball = Ball(width / 2 - 15, height / 2 - 15, 30, 30, light_grey)
        self.player = HumanPlayer(Racket(width - 20, height / 2 - 70, 10, 140, light_green), 0)
        self.aiPlayer = AiPlayer(Racket(10, height / 2 - 70, 10, 140, red), 7)
        self.clock = pygame.time.Clock()
        self.score_time = None

    def run(self):
        """
        The function to run the program
        """
        light_green = (50, 205, 50)
        red = (220, 20, 60)

        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player.speed += 7
                    if event.key == pygame.K_UP:
                        self.player.speed -= 7
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player.speed -= 7
                    if event.key == pygame.K_UP:
                        self.player.speed += 7
            self.board.fill()

            self.aiPlayer.move(self.board, self.ball)
            self.aiPlayer.racket.draw(self.board)

            self.player.move(self.board)
            self.player.racket.draw(self.board)

            self.ball.move(self.board, self.player.racket, self.aiPlayer.racket)
            self.ball.draw(self.board)

            if self.ball.rect.x < 0:
                self.player.score += 1
                self.score_time = pygame.time.get_ticks()

            if self.ball.rect.x > self.board.width:
                self.aiPlayer.score += 1
                self.score_time = pygame.time.get_ticks()

            if 5 <= self.player.score > self.aiPlayer.score:
                win_text = font.render("You won!", False, light_green)
                self.board.screen.blit(win_text, (self.board.width / 2, self.board.height / 2 + 30))
                self.ball.speed_x, self.ball.speed_y = 0, 0
                self.ball.rect.center = (self.board.width / 2, self.board.height / 2)
                self.score_time = False
            elif self.player.score < self.aiPlayer.score >= 5:
                win_text = font.render("You lost!", False, red)
                self.board.screen.blit(win_text, (self.board.width / 2, self.board.height / 2 + 30))
                self.ball.speed_x, self.ball.speed_y = 0, 0
                self.ball.rect.center = (self.board.width / 2, self.board.height / 2)
                self.score_time = False

            if self.score_time:
                current_time = pygame.time.get_ticks()
                self.score_time = self.ball.restart(self.board, current_time, self.score_time)
            if self.score_time:
                self.board.restart(current_time, self.score_time)

            player_text = font.render(f"{self.player.score}", False, light_green)
            self.board.screen.blit(player_text, (self.board.width / 2 + 8, self.board.height - 730))

            opponent_text = font.render(f"{self.aiPlayer.score}", False, red)
            self.board.screen.blit(opponent_text, (self.board.width / 2 - 24, self.board.height - 730))

            pygame.display.flip()
            self.clock.tick(60)


class Board(object):
    def __init__(self, width, height):
        """
        The constructor for Board class.

        Parameters:
            width(int): of the window with game board
            height(int): of the window with game board
        """
        self.background_color = pygame.Color('grey12')
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

        pygame.draw.aaline(self.screen, light_grey, (width / 2, 0), (width / 2, height))
        self.screen.fill(self.background_color)
        pygame.display.set_caption('AI Pong - Michal Kosinski, Aleksandra Formela')

    def fill(self):
        """
        The function to draw the board
        """
        self.screen.fill(self.background_color)

    def restart(self, current_time, score_time):
        """
        The function to restart the board

        Parameters:
            current_time (int): in ticks. Gets the current time
            score_time (int): in ticks. Gets the score time
        """
        if current_time - score_time < 700:
            three = font.render("3", False, red)
            self.screen.blit(three, (self.width / 2 - 10, self.height / 2 + 20))
        if 700 < current_time - score_time < 1400:
            two = font.render("2", False, orange)
            self.screen.blit(two, (self.width / 2 - 10, self.height / 2 + 20))
        if 1400 < current_time - score_time < 2100:
            one = font.render("1", False, light_green)
            self.screen.blit(one, (self.width / 2 - 10, self.height / 2 + 20))


if __name__ == "__main__":
    PongGame(1280, 750).run()
