import random

import pygame.freetype
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    K_r,
    K_q,
    K_s,
    K_p,
)

import dependencies.consts as c
from dependencies.dot import Dot
from dependencies.funcs import number
from dependencies.stats import save_level, check_highscore


# PAUSE SCREEN
def pause_screen():
    while True:
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 200, c.SCREEN_HEIGHT // 2 - 40),
                            f"Game paused, P to unpause", (255, 0, 0))
        pygame.display.flip()
        p = 0
        for event_p in pygame.event.get():
            if event_p.type == pygame.QUIT:
                if event_p.type == pygame.QUIT:
                    c.running = False
                    c.running_game = False
                    c.running_summ = False
                    p = 1
                    break
            if event_p.type == KEYDOWN:
                if event_p.key == K_p:
                    p = 1
                    break
        if p:
            break


# PYGAME INIT
pygame.init()
fpsClock = pygame.time.Clock()
GAME_FONT = pygame.freetype.Font("dependencies/PrequelDemo-ShadowItalic.otf", 24)
GAME_SMALL_FONT = pygame.freetype.Font("dependencies/PrequelDemo-ShadowItalic.otf", 18)
screen = pygame.display.set_mode([c.SCREEN_WIDTH, c.SCREEN_HEIGHT])
pygame.display.set_caption("Balls")
HIGH, AVG = 0, 0
programIcon = pygame.image.load('dependencies/icon.png')
pygame.display.set_icon(programIcon)

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
    GAME_FONT.render_to(screen, (0, 0), f"WHITE STRIPE UPDATE", (255, 255, 255))
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
                if event.key == K_p:
                    pause_screen()
                if event.key == K_q:
                    c.running = False
                    c.running_game = False
                    c.running_summ = False
                if event.key == K_r:
                    c.set_starting_conditions()

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and keys[K_UP]:
            c.GO_VERTICAL = 0
        elif keys[K_DOWN]:
            c.GO_VERTICAL = c.MOVE_SPEED * c.MULT * c.INVERT
        elif keys[K_UP]:
            c.GO_VERTICAL = - c.MOVE_SPEED * c.MULT * c.INVERT
        else:
            c.GO_VERTICAL = 0
        if keys[K_LEFT] and keys[K_RIGHT]:
            c.GO_HORIZONTAL = 0
        elif keys[K_LEFT]:
            c.GO_HORIZONTAL = - c.MOVE_SPEED * c.MULT * c.INVERT
        elif keys[K_RIGHT]:
            c.GO_HORIZONTAL = c.MOVE_SPEED * c.MULT * c.INVERT
        else:
            c.GO_HORIZONTAL = 0

        RANDOM_GOD = random.randint(1, 100)

        # DETERMINE LEVEL
        if c.GOOD_DOT_NUM == 0:
            c.LEVEL_NUM += 1

            c.GOOD_DOT_NUM = c.LEVEL_NUM
            c.BAD_DOT_NUM = (c.LEVEL_NUM - 1) * 2 - sum([int(DOT.name == "BAD") for DOT in c.DOTS]) - int(c.LEVEL_NUM**.5)

            c.DOTS += [Dot("GOOD", 10, (0, 255, 0), 5) for _ in range(c.GOOD_DOT_NUM)]

            c.DOTS += [Dot("BAD", 15, (255, 0, 0), -10) for _ in range(c.BAD_DOT_NUM)]
            if c.LEVEL_NUM >= 9 and not RANDOM_GOD % 3:
                c.DOTS += [Dot("ORANGE", 10, (255, 165, 0), 0, 5)]
            if c.LEVEL_NUM >= 14 and not RANDOM_GOD % 3:
                c.DOTS += [Dot("PINK", 10, (236, 93, 183), 30, 15)]


        # CREATE BIG_ACTION DOT
        if c.TICK > c.CURR_TICK + 40 and not c.BIG_ACTION_DOT_ON and c.LEVEL_NUM != c.CURR_LEVEL:
            c.BIG_ACTION_DOT_ON = 1
            r = random.randint(0, 2)
            big_name = ["PURPLE", "CYAN", "YELLOW"][r]
            big_color = [(128, 0, 128), (0, 255, 255), (255, 255, 0)][r]
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
                    c.SHIELD += 6

                if DOT.name == "YELLOW":
                    c.BIG_ACTION = 1
                    c.BIG_ACTION_DOT_ON = 0
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(c.CIRCLE_POS_X - 5, 0, 20, c.SCREEN_HEIGHT))
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, c.CIRCLE_POS_Y - 5, c.SCREEN_WIDTH, 20))
                    pygame.display.flip()
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(c.CIRCLE_POS_X - 5, 0, 20, c.SCREEN_HEIGHT))
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, c.CIRCLE_POS_Y - 5, c.SCREEN_WIDTH, 20))
                    for DOTT in c.DOTS:
                        if DOTT.name != "YELLOW":
                            if abs(DOTT.pos_x - c.CIRCLE_POS_X) <= 100:
                                if DOTT.name == "GOOD":
                                    c.GOOD_DOT_NUM -= 1
                                del c.DOTS[c.DOTS.index(DOTT)]
                            elif abs(DOTT.pos_y - c.CIRCLE_POS_Y) <= 100:
                                if DOTT.name == "GOOD":
                                    c.GOOD_DOT_NUM -= 1
                                del c.DOTS[c.DOTS.index(DOTT)]

                if DOT.name == "BAD" and c.SHIELD:
                    c.SHIELD -= 1
                    c.CIRCLE_R_SIZE -= DOT.size_change

                if DOT.name == "ORANGE":
                    c.INVERT_STATE = 1

                del c.DOTS[c.DOTS.index(DOT)]

        if c.INVERT_STATE:
            c.INVERT = -1
            c.INVERT_STATE = (c.INVERT_STATE + 1) % 155
            if not c.INVERT_STATE:
                c.INVERT = 1

        if c.WHITE_STATUS > 0:
            if c.WHITE_STATUS == 1:
                c.WHITE_AXIS = RANDOM_GOD % 2
                if c.WHITE_AXIS:
                    r = random.randint(50, c.SCREEN_WIDTH - 50)
                    c.WHITE_POS = [r, 0, 20, c.SCREEN_HEIGHT]
                else:
                    r = random.randint(50, c.SCREEN_HEIGHT - 50)
                    c.WHITE_POS = [0, r, c.SCREEN_WIDTH, 20]
            c.WHITE_STATUS = (c.WHITE_STATUS + 1) % int(c.CHANGE_EVERY * 1.5)
            if c.WHITE_STATUS % 3:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(*c.WHITE_POS))
            if c.WHITE_STATUS == 0:
                if c.WHITE_AXIS:
                    c.WHITE_POS[0] -= 30
                    c.WHITE_POS[2] += 80
                else:
                    c.WHITE_POS[1] -= 30
                    c.WHITE_POS[3] += 80

                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(*c.WHITE_POS))
                pygame.display.flip()
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(*c.WHITE_POS))
                if c.WHITE_AXIS:
                    if abs(c.CIRCLE_POS_X - c.WHITE_POS[0] - 50) <= 50 + c.CIRCLE_R_SIZE:
                        c.CIRCLE_R_SIZE -= 25
                    for DOT in c.DOTS:
                        if abs(DOT.pos_x - c.WHITE_POS[0] - 50) <= 50 + DOT.r_size:
                            if DOT.name == "GOOD":
                                c.GOOD_DOT_NUM -= 1
                            elif DOT.name in ["PURPLE", "YELLOW", "CYAN"]:
                                c.BIG_ACTION_DOT_ON = 0
                                c.BIG_ACTION = 1
                            del c.DOTS[c.DOTS.index(DOT)]
                else:
                    if abs(c.CIRCLE_POS_Y - c.WHITE_POS[1] - 50) <= 50 + c.CIRCLE_R_SIZE:
                        c.CIRCLE_R_SIZE -= 25
                    for DOT in c.DOTS:
                        if abs(DOT.pos_y - c.WHITE_POS[1] - 50) <= 50 + DOT.r_size:
                            if DOT.name == "GOOD":
                                c.GOOD_DOT_NUM -= 1
                            elif DOT.name in ["PURPLE", "YELLOW", "CYAN"]:
                                c.BIG_ACTION_DOT_ON = 0
                                c.BIG_ACTION = 1
                            del c.DOTS[c.DOTS.index(DOT)]

        # c.TICK ACTIONS
        c.CHANGE_COUNTER += 1
        if c.CHANGE_COUNTER % c.CHANGE_EVERY == 0:
            c.TICK += 1
            for DOT in c.DOTS:
                DOT.determine_move()
        if c.CHANGE_COUNTER % c.WHITE_EVERY == 0:
            c.WHITE_STATUS = 1
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
            save_level(c.LEVEL_NUM)
            HIGH, AVG = check_highscore()
        fpsClock.tick(c.FPS)

        screen.fill((0, 0, 0))
        GAME_SMALL_FONT.render_to(screen, (0, 0), f"LEVEL {number(c.LEVEL_NUM)}", (0, 255, 255))
        GAME_SMALL_FONT.render_to(screen, (c.SCREEN_WIDTH - 273, 0), f"P PAUSE    Q QUIT    R RESET", (0, 255, 255))

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
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 100, c.SCREEN_HEIGHT // 2 - 60), f"GAME OVER", (255, 0, 0))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 200, c.SCREEN_HEIGHT // 2 - 30),
                            f"YOU GOT TO LEVEL {number(c.LEVEL_NUM)}", (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 100, c.SCREEN_HEIGHT // 2 + 0), f"R - restart",
                            (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 80, c.SCREEN_HEIGHT // 2 + 30), f"Q - quit", (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 200, c.SCREEN_HEIGHT // 2 + 60), f"HIGHSCORE : {number(HIGH)}", (0, 255, 255))
        GAME_FONT.render_to(screen, (c.SCREEN_WIDTH // 2 - 210, c.SCREEN_HEIGHT // 2 + 90), f"AVERAGE SCORE : {number(AVG)}", (0, 255, 255))
        pygame.display.flip()
