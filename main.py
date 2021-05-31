import random

import pygame.freetype
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    KEYUP,
    K_r,
    K_q,
    K_s,
)


def distance(p1: list, p2: list) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5


num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
              10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen',
              17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}
num2words2 = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']


def number(Number):
    if 0 <= Number <= 19:
        return num2words1[Number]
    elif 20 <= Number <= 99:
        tens, remainder = divmod(Number, 10)
        return num2words2[tens - 2] + '-' + num2words1[remainder] if remainder else num2words2[tens - 2]


MULT = 0.85  # GAME SPEED

FPS = 60  # FRAMES PER SECOND SETTING
fpsClock = pygame.time.Clock()


pygame.init()
GAME_FONT = pygame.freetype.Font("PrequelDemo-ShadowItalic.otf", 24)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Balls")

LEVEL_NUM = 1

GO_HORIZONTAL = 0
GO_VERTICAL = 0

MOVE_SPEED = 5
CIRCLE_R_SIZE = 25

CIRCLE_POS_X = SCREEN_WIDTH // 2
CIRCLE_POS_Y = SCREEN_HEIGHT // 2

GOOD_DOT_NUM = 1
GOOD_DOT_R_SIZE = 10
GOOD_DOT_POS = [[random.randint(GOOD_DOT_R_SIZE, SCREEN_WIDTH - GOOD_DOT_R_SIZE),
                 random.randint(GOOD_DOT_R_SIZE, SCREEN_HEIGHT - GOOD_DOT_R_SIZE)] for _ in range(GOOD_DOT_NUM)]
GOOD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5)] for _ in range(GOOD_DOT_NUM)]

BAD_DOT_NUM = 1
BAD_DOT_R_SIZE = 15
BAD_DOT_POS = [[random.randint(BAD_DOT_R_SIZE, SCREEN_WIDTH - BAD_DOT_R_SIZE),
                random.randint(BAD_DOT_R_SIZE, SCREEN_HEIGHT - BAD_DOT_R_SIZE)] for _ in range(BAD_DOT_NUM)]
BAD_DOT_MOVE = [[random.randint(0, 1), random.randint(-7, 7)] for _ in range(BAD_DOT_NUM)]

PURPLE_DOT_R_SIZE = 10
PURPLE_DOT_POS = [random.randint(PURPLE_DOT_R_SIZE, SCREEN_WIDTH - PURPLE_DOT_R_SIZE),
                  random.randint(PURPLE_DOT_R_SIZE, SCREEN_HEIGHT - PURPLE_DOT_R_SIZE)]
PURPLE_DOT_ON = 0

CHANGE_EVERY = int(25 * (1 / MULT))
CHANGE_COUNTER = 0

TICK = 1
CURR_LEVEL = 1
CURR_TICK = TICK

running = True
running_game = True
running_summ = True

running_intro = True
while running_intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            running_intro = False

        if event.type == KEYDOWN:
            if event.key == K_s:
                running_intro = False
            if event.key == K_q:
                running = False
                running_intro = False

    screen.fill((0, 0, 0))
    GAME_FONT.render_to(screen, (0, 0), f"PURPLE DOT UPDATE", (128, 0, 128))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 40), f"Balls", (255, 0, 0))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 10), f"S - start", (0, 255, 255))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
    pygame.display.flip()

while running:

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_game = False
                running_summ = False

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    GO_VERTICAL += MOVE_SPEED * MULT
                if event.key == K_UP:
                    GO_VERTICAL -= MOVE_SPEED * MULT
                if event.key == K_LEFT:
                    GO_HORIZONTAL -= MOVE_SPEED * MULT
                if event.key == K_RIGHT:
                    GO_HORIZONTAL += MOVE_SPEED * MULT

            if event.type == KEYUP:
                if event.key == K_DOWN:
                    GO_VERTICAL -= MOVE_SPEED * MULT
                if event.key == K_UP:
                    GO_VERTICAL += MOVE_SPEED * MULT
                if event.key == K_LEFT:
                    GO_HORIZONTAL += MOVE_SPEED * MULT
                if event.key == K_RIGHT:
                    GO_HORIZONTAL -= MOVE_SPEED * MULT

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(LEVEL_NUM)}", (0, 255, 255))

        CIRCLE_POS_X = CIRCLE_POS_X + GO_HORIZONTAL
        CIRCLE_POS_Y = CIRCLE_POS_Y + GO_VERTICAL

        if CIRCLE_POS_X < CIRCLE_R_SIZE:
            CIRCLE_POS_X = CIRCLE_R_SIZE
        if CIRCLE_POS_X > SCREEN_WIDTH - CIRCLE_R_SIZE:
            CIRCLE_POS_X = SCREEN_WIDTH - CIRCLE_R_SIZE
        if CIRCLE_POS_Y < CIRCLE_R_SIZE:
            CIRCLE_POS_Y = CIRCLE_R_SIZE
        if CIRCLE_POS_Y > SCREEN_HEIGHT - CIRCLE_R_SIZE:
            CIRCLE_POS_Y = SCREEN_HEIGHT - CIRCLE_R_SIZE

        for i in range(len(GOOD_DOT_POS)):
            GOOD_DOT_POS[i][GOOD_DOT_MOVE[i][0]] += GOOD_DOT_MOVE[i][1]

        for i in range(len(BAD_DOT_POS)):
            BAD_DOT_POS[i][BAD_DOT_MOVE[i][0]] += BAD_DOT_MOVE[i][1]

        for POS in GOOD_DOT_POS:
            if POS[0] < GOOD_DOT_R_SIZE:
                POS[0] = GOOD_DOT_R_SIZE
            if POS[0] > SCREEN_WIDTH - GOOD_DOT_R_SIZE:
                POS[0] = SCREEN_WIDTH - GOOD_DOT_R_SIZE
            if POS[1] < GOOD_DOT_R_SIZE:
                POS[1] = GOOD_DOT_R_SIZE
            if POS[1] > SCREEN_HEIGHT - GOOD_DOT_R_SIZE:
                POS[1] = SCREEN_HEIGHT - GOOD_DOT_R_SIZE

            if distance(POS, [CIRCLE_POS_X, CIRCLE_POS_Y]) <= CIRCLE_R_SIZE + GOOD_DOT_R_SIZE:
                del GOOD_DOT_POS[GOOD_DOT_POS.index(POS)]
                CIRCLE_R_SIZE = CIRCLE_R_SIZE + 5

        for POS in BAD_DOT_POS:
            if POS[0] < BAD_DOT_R_SIZE:
                POS[0] = BAD_DOT_R_SIZE
            if POS[0] > SCREEN_WIDTH - BAD_DOT_R_SIZE:
                POS[0] = SCREEN_WIDTH - BAD_DOT_R_SIZE
            if POS[1] < BAD_DOT_R_SIZE:
                POS[1] = BAD_DOT_R_SIZE
            if POS[1] > SCREEN_HEIGHT - BAD_DOT_R_SIZE:
                POS[1] = SCREEN_HEIGHT - BAD_DOT_R_SIZE

            if distance(POS, [CIRCLE_POS_X, CIRCLE_POS_Y]) <= CIRCLE_R_SIZE + BAD_DOT_R_SIZE:
                del BAD_DOT_POS[BAD_DOT_POS.index(POS)]
                CIRCLE_R_SIZE = CIRCLE_R_SIZE - 10

        if len(GOOD_DOT_POS) == 0:
            LEVEL_NUM += 1

            GOOD_DOT_NUM = GOOD_DOT_NUM + 1
            GOOD_DOT_POS = [[random.randint(GOOD_DOT_R_SIZE, SCREEN_WIDTH - GOOD_DOT_R_SIZE),
                             random.randint(GOOD_DOT_R_SIZE, SCREEN_HEIGHT - GOOD_DOT_R_SIZE)] for _ in
                            range(GOOD_DOT_NUM)]
            GOOD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5) * MULT] for _ in range(GOOD_DOT_NUM)]

            BAD_DOT_NUM = BAD_DOT_NUM + 2
            BAD_DOT_POS = [[random.randint(BAD_DOT_R_SIZE, SCREEN_WIDTH - BAD_DOT_R_SIZE),
                            random.randint(BAD_DOT_R_SIZE, SCREEN_HEIGHT - BAD_DOT_R_SIZE)] for _ in
                           range(BAD_DOT_NUM)]
            BAD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5) * MULT] for _ in range(BAD_DOT_NUM)]

        if distance(PURPLE_DOT_POS, [CIRCLE_POS_X, CIRCLE_POS_Y]) <= PURPLE_DOT_R_SIZE + CIRCLE_R_SIZE and PURPLE_DOT_ON == 1:
            PURPLE_DOT_ON = 0
            for POS in BAD_DOT_POS:
                if random.randint(0, 1):
                    del BAD_DOT_POS[BAD_DOT_POS.index(POS)]

        if CHANGE_COUNTER == CHANGE_EVERY:
            GOOD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5) * MULT] for _ in range(GOOD_DOT_NUM)]
            BAD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5) * MULT] for _ in range(BAD_DOT_NUM)]
            TICK += 1
        CHANGE_COUNTER = CHANGE_COUNTER % CHANGE_EVERY + 1

        if TICK > CURR_TICK + 40 and PURPLE_DOT_ON == 0 and LEVEL_NUM != CURR_LEVEL:
            PURPLE_DOT_POS = [random.randint(PURPLE_DOT_R_SIZE, SCREEN_WIDTH - PURPLE_DOT_R_SIZE),
                              random.randint(PURPLE_DOT_R_SIZE, SCREEN_HEIGHT - PURPLE_DOT_R_SIZE)]
            PURPLE_DOT_ON = 1
            CURR_TICK = TICK
            CURR_LEVEL = LEVEL_NUM

        for POS in GOOD_DOT_POS:
            pygame.draw.circle(screen, (0, 255, 0), POS, GOOD_DOT_R_SIZE)

        for POS in BAD_DOT_POS:
            pygame.draw.circle(screen, (255, 0, 0), POS, BAD_DOT_R_SIZE)

        if PURPLE_DOT_ON:
            pygame.draw.circle(screen, (128, 0, 128), PURPLE_DOT_POS, PURPLE_DOT_R_SIZE)

        pygame.draw.circle(screen, (0, 0, 255), (CIRCLE_POS_X, CIRCLE_POS_Y), CIRCLE_R_SIZE)
        if CIRCLE_R_SIZE <= 10:
            pygame.draw.circle(screen, (255, 255, 255), (CIRCLE_POS_X, CIRCLE_POS_Y), CIRCLE_R_SIZE//2)

        pygame.display.flip()
        if CIRCLE_R_SIZE <= 0:
            running_game = False
            running_summ = True
        fpsClock.tick(FPS)

    while running_summ:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_game = False
                running_summ = False
            if event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                    running_game = False
                    running_summ = False
                if event.key == K_r:
                    LEVEL_NUM = 1

                    GO_HORIZONTAL = 0
                    GO_VERTICAL = 0

                    CIRCLE_R_SIZE = 25

                    CIRCLE_POS_X = SCREEN_WIDTH // 2
                    CIRCLE_POS_Y = SCREEN_HEIGHT // 2

                    GOOD_DOT_NUM = 1
                    GOOD_DOT_POS = [[random.randint(GOOD_DOT_R_SIZE, SCREEN_WIDTH - GOOD_DOT_R_SIZE),
                                     random.randint(GOOD_DOT_R_SIZE, SCREEN_HEIGHT - GOOD_DOT_R_SIZE)] for _ in
                                    range(GOOD_DOT_NUM)]
                    GOOD_DOT_MOVE = [[random.randint(0, 1), random.randint(-5, 5)] for _ in range(GOOD_DOT_NUM)]

                    BAD_DOT_NUM = 1
                    BAD_DOT_POS = [[random.randint(BAD_DOT_R_SIZE, SCREEN_WIDTH - BAD_DOT_R_SIZE),
                                    random.randint(BAD_DOT_R_SIZE, SCREEN_HEIGHT - BAD_DOT_R_SIZE)] for _ in
                                   range(BAD_DOT_NUM)]
                    BAD_DOT_MOVE = [[random.randint(0, 1), random.randint(-7, 7)] for _ in range(BAD_DOT_NUM)]

                    CHANGE_COUNTER = 0
                    PURPLE_DOT_ON = 0
                    running_summ = False
                    running_game = True

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(LEVEL_NUM)}", (0, 255, 255))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 40), f"GAME OVER", (255, 0, 0))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 10), f"R - restart", (0, 255, 255))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
        pygame.display.flip()
