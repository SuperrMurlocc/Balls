import random
from funcs import number
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

MULT = 1.0

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LEVEL_NUM = 0
CURR_LEVEL = LEVEL_NUM

GO_HORIZONTAL = 0
GO_VERTICAL = 0

MOVE_SPEED = 5
CIRCLE_R_SIZE = 25

CIRCLE_POS_X = SCREEN_WIDTH // 2
CIRCLE_POS_Y = SCREEN_HEIGHT // 2

GOOD_DOT_NUM = 0
GOOD_DOT_R_SIZE = 10

BAD_DOT_NUM = 0
BAD_DOT_R_SIZE = 15

PURPLE_DOT_R_SIZE = 10
BIG_ACTION_DOT_ON = 0

CHANGE_EVERY = int(25 * (1 / MULT))
CHANGE_COUNTER = 0

TICK = 1
CURR_TICK = TICK
BIG_ACTION = 0

SHIELD = 0

running = True
running_game = True
running_summ = True

DOTS = []


def distance(p1: (int, int), p2: (int, int)) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5


class Dot:
    """
    Class used to create a dot object.
    """

    def __init__(self, name: str, r_size: int, color: (int, int, int), size_change: int = 0, max_move_speed: int = 5, pos: (int, int) = None):
        """
        Initializes dot object.

        :param name: Name of dot.
        :param r_size: Radius size of dot.
        :param color: Color of dot.
        :param size_change: The amount by which our dot size is changed.
        :param pos: Position of dot.
        """
        self.name = name
        self.r_size = r_size
        self.color = color
        self.size_change = size_change
        if pos:
            self.pos_x = pos[0]
            self.pos_y = pos[1]
        else:
            self.pos_x = random.randint(r_size, SCREEN_WIDTH - r_size)
            self.pos_y = random.randint(r_size, SCREEN_HEIGHT - r_size)

        self.max_move_speed = max_move_speed

        self.move = random.randint(-max_move_speed, max_move_speed)
        self.move_direction = random.randint(0, 1)

    def disp(self) -> None:
        """
        Displays dot on screen.

        :return: None
        """
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.r_size)

    def collision(self, pos_x, pos_y) -> bool:
        """
        Detect collison.

        :return: True/False.
        """
        if distance((self.pos_x, self.pos_y), (pos_x, pos_y)) <= CIRCLE_R_SIZE + self.r_size:
            return True
        else:
            return False

    def determine_move(self):
        self.move = random.randint(-self.max_move_speed, self.max_move_speed) * MULT
        self.move_direction = random.randint(0, 1)

    def move_pos(self):
        if self.move_direction:
            self.pos_x += self.move

            if self.pos_x < self.r_size:
                self.pos_x = self.r_size
            if self.pos_x > SCREEN_WIDTH - self.r_size:
                self.pos_x = SCREEN_WIDTH - self.r_size
        else:
            self.pos_y += self.move

            if self.pos_y < self.r_size:
                self.pos_y = self.r_size
            if self.pos_y > SCREEN_HEIGHT - self.r_size:
                self.pos_y = SCREEN_HEIGHT - self.r_size


def set_starting_conditions() -> None:
    global LEVEL_NUM, GO_HORIZONTAL, GO_VERTICAL, CIRCLE_POS_X, CIRCLE_POS_Y, GOOD_DOT_NUM, BAD_DOT_NUM, \
        BIG_ACTION_DOT_ON, CHANGE_COUNTER, TICK, CURR_LEVEL, CURR_TICK, CIRCLE_R_SIZE, DOTS, BIG_ACTION, SHIELD
    LEVEL_NUM = 0
    CURR_LEVEL = LEVEL_NUM

    GO_HORIZONTAL = 0
    GO_VERTICAL = 0

    CIRCLE_POS_X = SCREEN_WIDTH // 2
    CIRCLE_POS_Y = SCREEN_HEIGHT // 2
    CIRCLE_R_SIZE = 25
    DOTS = []

    GOOD_DOT_NUM = 0
    BAD_DOT_NUM = 0
    BIG_ACTION_DOT_ON = 0

    CHANGE_COUNTER = 0
    BIG_ACTION = 0

    SHIELD = 0

    TICK = 1
    CURR_TICK = TICK


# PYGAME INIT
pygame.init()
fpsClock = pygame.time.Clock()
GAME_FONT = pygame.freetype.Font("PrequelDemo-ShadowItalic.otf", 24)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Balls")

# STARTING SCREEN
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
    GAME_FONT.render_to(screen, (0, 0), f"CYAN DOT UPDATE", (128, 0, 128))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 40), f"Balls", (255, 0, 0))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 10), f"S - start", (0, 255, 255))
    GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
    pygame.display.flip()

while running:

    # MAIN LOOP
    while running_game:
        # EVENTS
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

        # DETERMINE LEVEL
        if GOOD_DOT_NUM == 0:
            LEVEL_NUM += 1

            GOOD_DOT_NUM = LEVEL_NUM
            BAD_DOT_NUM = (LEVEL_NUM - 1) * 2

            DOTS = [Dot("GOOD", 10, (0, 255, 0), 5) for _ in range(GOOD_DOT_NUM)]
            DOTS += [Dot("BAD", 15, (255, 0, 0), -10) for _ in range(BAD_DOT_NUM)]

        # CREATE BIG_ACTION DOT
        if TICK > CURR_TICK + 40 and not BIG_ACTION_DOT_ON and LEVEL_NUM != CURR_LEVEL:
            BIG_ACTION_DOT_ON = 1
            r = random.randint(0, 1)
            big_name = ["PURPLE", "CYAN"][r]
            big_color = [(128, 0, 128), (0, 255, 255)][r]
            DOTS += [Dot(big_name, 10, big_color, 0, 0)]

        # MOVE MYSELF
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

        # MOVE DOTS
        for DOT in DOTS:
            DOT.move_pos()

        # COLLISION ACTIONS
        for DOT in DOTS:
            if DOT.collision(CIRCLE_POS_X, CIRCLE_POS_Y):
                CIRCLE_R_SIZE += DOT.size_change

                if DOT.name == "GOOD":
                    GOOD_DOT_NUM -= 1

                if DOT.name == "PURPLE":
                    BIG_ACTION = 1
                    BIG_ACTION_DOT_ON = 0
                    for DOTT in DOTS:
                        if DOTT.name == "BAD":
                            if random.randint(0, 1):
                                del DOTS[DOTS.index(DOTT)]

                if DOT.name == "CYAN":
                    BIG_ACTION = 1
                    BIG_ACTION_DOT_ON = 0
                    SHIELD = 7

                if DOT.name == "BAD" and SHIELD:
                    SHIELD -= 1
                    CIRCLE_R_SIZE -= DOT.size_change

                del DOTS[DOTS.index(DOT)]

        # TICK ACTIONS
        CHANGE_COUNTER = CHANGE_COUNTER % CHANGE_EVERY + 1
        if CHANGE_COUNTER == CHANGE_EVERY:
            TICK += 1
            for DOT in DOTS:
                DOT.determine_move()
        if BIG_ACTION:
            BIG_ACTION = 0
            CURR_LEVEL = LEVEL_NUM
            CURR_TICK = TICK

        # DISPLAY
        for DOT in DOTS:
            DOT.disp()

        pygame.draw.circle(screen, (0, 0, 255), (CIRCLE_POS_X, CIRCLE_POS_Y), CIRCLE_R_SIZE)
        if CIRCLE_R_SIZE <= 10:
            pygame.draw.circle(screen, (255, 255, 255), (CIRCLE_POS_X, CIRCLE_POS_Y), CIRCLE_R_SIZE // 2)
        if SHIELD:
            pygame.draw.circle(screen, (0, 255, 255), (CIRCLE_POS_X, CIRCLE_POS_Y), CIRCLE_R_SIZE, width=2)

        pygame.display.flip()
        if CIRCLE_R_SIZE <= 0:
            running_game = False
            running_summ = True
        fpsClock.tick(FPS)

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(LEVEL_NUM)}", (0, 255, 255))

    # RESTART SCREEN
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
                    set_starting_conditions()
                    running_game = True
                    running_summ = False

        screen.fill((0, 0, 0))
        GAME_FONT.render_to(screen, (0, 0), f"LEVEL {number(LEVEL_NUM)}", (0, 255, 255))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 40), f"GAME OVER", (255, 0, 0))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 10), f"R - restart", (0, 255, 255))
        GAME_FONT.render_to(screen, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 20), f"Q - quit", (0, 255, 255))
        pygame.display.flip()
