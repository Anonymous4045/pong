import asyncio
import random
import time

import pygame


def beep(x, y):  # dont use out of replit
    return


game_name = "Pong"

WIDTH, HEIGHT = 1000, 500

pygame.init()
pygame.font.init()
display = pygame.display
screen = display.set_mode((WIDTH, HEIGHT))

# assets
PADDLE = pygame.image.load("assets/paddle.png")
BALL = pygame.image.load("assets/ball.png")

display.set_caption(game_name)
display.set_icon(BALL)

# Colors
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

point_in_rect = lambda point, rect: rect.collidepoint(point)


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length
    if x1 == x2:
        y_cords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        x_cords = [x1] * len(y_cords)
    next_cords = list(zip(x_cords[1::2], y_cords[1::2]))
    last_cords = list(zip(x_cords[0::2], y_cords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_cords, last_cords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)


class Button:
    def __init__(self, sprites, name, message, foreground, background, size, x, y):
        sprites.append(self)
        self.name = name
        self.message = message
        self.foreground = foreground
        font = pygame.font.get_default_font()
        self.text = pygame.font.Font(font, size).render(
            message, True, foreground, background
        )
        self.rect = self.text.get_rect()
        self.rect.center = x, y

    def show(self):
        screen.blit(self.text, self.rect)
        pygame.draw.rect(screen, self.foreground, self.rect, 1)


class Text:
    def __init__(self, sprites, name, message, foreground, background, size, x, y):
        sprites.append(self)
        self.name = name
        self.message = message
        self.foreground = foreground
        self.background = background
        self.font = pygame.font.get_default_font()
        self.size = size
        self.text = pygame.font.Font(self.font, size).render(
            self.message, True, foreground, background
        )
        self.rect = self.text.get_rect()
        self.rect.center = x, y

    def set_message(self, message):
        self.message = str(message)
        self.text = pygame.font.Font(self.font, self.size).render(
            self.message, True, self.foreground, self.background
        )
        self.rect = self.text.get_rect(center=self.rect.center)

    show = lambda self: screen.blit(self.text, self.rect)


class Player:
    def __init__(self, sprites, x):
        sprites.append(self)
        self.x = x
        self.y = HEIGHT // 2 - 32
        self.sprite = PADDLE

        self.score = 0

    rect = lambda self: self.sprite.get_rect(topleft=(self.x, self.y))
    center = lambda self: self.y + 32
    show = lambda self: screen.blit(self.sprite, (self.x, self.y))


class Ball:
    def __init__(self, sprites):
        sprites.append(self)
        self.sprite = BALL
        self.x = WIDTH // 2 - 8
        self.y = HEIGHT // 2 - 8
        self.slope = random.randint(0, 20) / 15 * random.choice([1, -1])
        self.direction = random.choice([1, -1])

    rect = lambda self: self.sprite.get_rect(topleft=(self.x, self.y))
    change_slope = (
        lambda self, user, player: (user.center() - self.center())
        / 16
        * (-1 if user == player else 1)
    )
    next = lambda self: round(self.direction * self.slope + self.y)
    center = lambda self: self.y + 8
    show = lambda self: screen.blit(self.sprite, (self.x, self.y))


async def main():
    sprites = []

    title = Text(sprites, "title", game_name, white, black, 100, WIDTH // 2, HEIGHT // 2 - 100)
    single_player = Button(
        sprites, "single_player", "Single Player", white, black, 64, WIDTH // 2, HEIGHT // 2
    )
    two_player = Button(
        sprites, "two_player", "Two Player", white, black, 64, WIDTH // 2, HEIGHT // 2 + 64 + 20
    )

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Menu closed")
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in sprites:
                    if isinstance(sprite, Button):
                        menu = False
                        if sprite.message == "Single Player":
                            if point_in_rect(event.pos, sprite.rect):
                                bot = True
                        else:
                            if point_in_rect(event.pos, sprite.rect):
                                bot = False

        screen.fill(black)

        for sprite in sprites:
            sprite.show()

        pygame.display.update()
        await asyncio.sleep(0)

    w_down = s_down = up_down = down_down = False

    sprites = []

    player = Player(sprites, 25)
    opponent = Player(sprites, WIDTH - 35)
    ball = Ball(sprites)

    size = 100
    p1_score = Text(
        sprites, "p1_score", str(player.score), white, black, size, WIDTH // 2 - size // 2, size // 2
    )
    p2_score = Text(
        sprites,
        "p2_score",
        str(opponent.score),
        white,
        black,
        size,
        WIDTH // 2 + size // 2,
        size // 2,
    )

    game_loop = True
    print(f"Starting {game_name}")
    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"{game_name} closed")
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    w_down = True
                if event.key == pygame.K_s:
                    s_down = True
                if event.key == 1073741906:
                    up_down = True
                if event.key == 1073741905:
                    down_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_down = False
                if event.key == pygame.K_s:
                    s_down = False
                if event.key == 1073741906:
                    up_down = False
                if event.key == 1073741905:
                    down_down = False

        if bot:
            opponent.y = ball.y - 32

        if w_down:
            player.y -= 3
        if s_down:
            player.y += 3
        if up_down:
            opponent.y -= 3
        if down_down:
            opponent.y += 3

        if player.y < 0:
            player.y = 0
        if player.y >= HEIGHT - 64:
            player.y = HEIGHT - 64
        if opponent.y < 0:
            opponent.y = 0
        if opponent.y >= HEIGHT - 64:
            opponent.y = HEIGHT - 64

        # Ball logic
        if ball.rect().colliderect(player.rect()):
            ball.direction *= -1
            ball.slope = ball.change_slope(player, opponent)
            beep(600, 100)
        elif ball.rect().colliderect(opponent.rect()):
            ball.direction *= -1
            ball.slope = ball.change_slope(opponent, player)
            beep(600, 100)
        elif ball.x <= 0:
            opponent.score += 1
            sprites.remove(ball)
            ball = Ball(sprites)
            player.y = opponent.y = HEIGHT // 2
            beep(700, 100)
        elif ball.x >= WIDTH - 16:
            player.score += 1
            sprites.remove(ball)
            ball = Ball(sprites)
            player.y = opponent.y = HEIGHT // 2
            beep(700, 100)
        elif ball.y <= 0:
            ball.slope *= -1
            beep(500, 100)
        elif ball.y >= HEIGHT - 16:
            ball.slope *= -1
            beep(500, 100)

        # Display
        screen.fill(black)
        draw_dashed_line(screen, white, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        for sprite in sprites:
            if isinstance(sprite, Text):
                if sprite == p1_score:
                    message = player.score
                else:
                    message = opponent.score
                sprite.set_message(message)
            sprite.show()

        pygame.display.update()

        time.sleep(0.01)

        # Post-Frame logic
        ball.y = ball.next()
        ball.x += 3 * ball.direction

        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
