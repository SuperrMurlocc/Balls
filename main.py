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

import consts as c
from dot import Dot
from funcs import number

# PYGAME INIT
pygame.init()
fpsClock = pygame.time.Clock()
GAME_FONT = pygame.freetype.Font("PrequelDemo-ShadowItalic.otf", 24)
screen = pygame.display.set_mode([c.SCREEN_WIDTH, c.SCREEN_HEIGHT])
pygame.display.set_caption("Balls")

# STARTING SCREEN
running_intro = True
while running_intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            c.running = False
            running_intro = False

        if event.type == KEYDOWN:
            if event.key == K_s:
                running_intro = False
            if event.key == K_q:
                c.running = False
                running_intro = False

    screen.fill((0, 0, 0))
    GAME_FONT.render_to(screen, (0, 0), f"CYAN DOT UPDATE", (0, 255, 255))
    GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 - 40), f"Balls", (255, 0, 0))
    GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 - 10), f"S - start", (0, 255, 255))
    GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
    pygame.display.flip()

while c.running:

    # MAIN LOOP
    while c.running_game:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.running = False
                c.running_game = False
                c.running_summ = False

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    c.GO_VERTICAL += c.MOVE_SPEED * c.MULT
                if event.key == K_UP:
                    c.GO_VERTICAL -= c.MOVE_SPEED * c.MULT
                if event.key == K_LEFT:
                    c.GO_HORIZONTAL -= c.MOVE_SPEED * c.MULT
                if event.key == K_RIGHT:
                    c.GO_HORIZONTAL += c.MOVE_SPEED * c.MULT

            if event.type == KEYUP:
                if event.key == K_DOWN:
                    c.GO_VERTICAL -= c.MOVE_SPEED * c.MULT
                if event.key == K_UP:
                    c.GO_VERTICAL += c.MOVE_SPEED * c.MULT
                if event.key == K_LEFT:
                    c.GO_HORIZONTAL += c.MOVE_SPEED * c.MULT
                if event.key == K_RIGHT:
                    c.GO_HORIZONTAL -= c.MOVE_SPEED * c.MULT

        # DETERMINE LEVEL
        if c.GOOD_DOT_NUM == 0:
            c.LEVEL_NUM += 1

            c.GOOD_DOT_NUM = c.LEVEL_NUM
            c.BAD_DOT_NUM = (c.LEVEL_NUM - 1) * 2 - sum([int(DOT.name == "BAD") for DOT in c.DOTS])

            c.DOTS += [Dot("GOOD", 10, (0, 255, 0), 5) for _ in range(c.GOOD_DOT_NUM)]

            c.DOTS += [Dot("BAD", 15, (255, 0, 0), -10) for _ in range(c.BAD_DOT_NUM)]

        # CREATE BIG_ACTION DOT
        if c.TICK > c.CURR_TICK + 40 and not c.BIG_ACTION_DOT_ON and c.LEVEL_NUM != c.CURR_LEVEL:
            c.BIG_ACTION_DOT_ON = 1
            r = random.randint(0, 1)
            big_name = ["PURPLE", "CYAN"][r]
            big_color = [(128, 0, 128), (0, 255, 255)][r]
            c.DOTS += [Dot(big_name, 10, big_color, 0, 0)]

        # MOVE MYSELF
        c.CIRCLE_POS_X = c.CIRCLE_POS_X + c.GO_HORIZONTAL
        c.CIRCLE_POS_Y = c.CIRCLE_POS_Y + c.GO_VERTICAL

        if c.CIRCLE_POS_X < c.CIRCLE_R_SIZE:
            c.CIRCLE_POS_X = c.CIRCLE_R_SIZE
        if c.CIRCLE_POS_X > c.SCREEN_WIDTH - c.CIRCLE_R_SIZE:
            c.CIRCLE_POS_X = c.SCREEN_WIDTH - c.CIRCLE_R_SIZE
        if c.CIRCLE_POS_Y < c.CIRCLE_R_SIZE:
            c.CIRCLE_POS_Y = c.CIRCLE_R_SIZE
        if c.CIRCLE_POS_Y > c.SCREEN_HEIGHT - c.CIRCLE_R_SIZE:
            c.CIRCLE_POS_Y = c.SCREEN_HEIGHT - c.CIRCLE_R_SIZE

        # MOVE DOTS
        for DOT in c.DOTS:
            DOT.move_pos()

        # COLLISION ACTIONS
        for DOT in c.DOTS:
            if DOT.collision(c.CIRCLE_POS_X, c.CIRCLE_POS_Y):
                c.CIRCLE_R_SIZE += DOT.size_change

                if DOT.name == "GOOD":
                    c.GOOD_DOT_NUM -= 1

                if DOT.name == "PURPLE":
                    c.BIG_ACTION = 1
                    c.BIG_ACTION_DOT_ON = 0
                    for DOTT in c.DOTS:
                        if DOTT.name == "BAD":
                            if random.randint(0, 1):
                                del c.DOTS[c.DOTS.index(DOTT)]

                if DOT.name == "CYAN":
                    c.BIG_ACTION = 1
                    c.BIG_ACTION_DOT_ON = 0
                    c.SHIELD = 7

                if DOT.name == "BAD" and c.SHIELD:
                    c.SHIELD -= 1
                    c.CIRCLE_R_SIZE -= DOT.size_change

                del c.DOTS[c.DOTS.index(DOT)]

        # c.TICK ACTIONS
        c.CHANGE_COUNTER = c.CHANGE_COUNTER % c.CHANGE_EVERY + 1
        if c.CHANGE_COUNTER == c.CHANGE_EVERY:
            c.TICK += 1
            for DOT in c.DOTS:
                DOT.determine_move()
        if c.BIG_ACTION:
            c.BIG_ACTION = 0
            c.CURR_LEVEL = c.LEVEL_NUM
            c.CURR_TICK = c.TICK

        # DISPLAY
        for DOT in c.DOTS:
            DOT.disp(screen)

        pygame.draw.circle(screen, (0, 0, 255), (c.CIRCLE_POS_X, c.CIRCLE_POS_Y), c.CIRCLE_R_SIZE)
        if c.CIRCLE_R_SIZE <= 10:
            pygame.draw.circle(screen, (255, 255, 255), (c.CIRCLE_POS_X, c.CIRCLE_POS_Y), c.CIRCLE_R_SIZE // 2)
        if c.SHIELD:
            pygame.draw.circle(screen, (0, 255, 255), (c.CIRCLE_POS_X, c.CIRCLE_POS_Y), c.CIRCLE_R_SIZE, width=2)

        pygame.display.flip()
        if c.CIRCLE_R_SIZE <= 0:
            c.running_game = False
            c.running_summ = True
        fpsClock.tick(c.FPS)

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(c.LEVEL_NUM)}", (0, 255, 255))

    # RESTART SCREEN
    while c.running_summ:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.running = False
                c.running_game = False
                c.running_summ = False
            if event.type == KEYDOWN:
                if event.key == K_q:
                    c.running = False
                    c.running_game = False
                    c.running_summ = False
                if event.key == K_r:
                    c.set_starting_conditions()
                    c.running_game = True
                    c.running_summ = False

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(c.LEVEL_NUM)}", (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 - 40), f"GAME OVER", (255, 0, 0))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 - 10), f"R - restart",
                            (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 85, c.SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
        pygame.display.flip()
