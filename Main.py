import sys
from data.Levels import *
import pygame
from Settings import *
from random import randint as rint


# Функция выхода из программы
def quit_sys():
    pygame.quit()
    sys.exit()


# Функция обработки уровня и заненсения спрайтов в группы
def make_level(level):
    x = y = 0
    player = None
    boss = None
    for row in level[0]:
        x = 0
        height = 64
        for obj in row:
            width = 64
            if obj in '012[)(]':
                platform = Platform(x, y, obj, True)
                ALL_SPRITES.add(platform)
            if obj in 'CS345678QWETIXП789OEFGHKPYUV':
                platform = Platform(x, y, obj, False)
                ALL_SPRITES.add(platform)
            if obj == '#':
                platform = Stair(x, y - 1)
                ALL_SPRITES.add(platform)
            if obj == '-':
                platform = Stair(x, y - 1, True)
                ALL_SPRITES.add(platform)
            if obj == '^':
                platform = Spike(x, y)
                ALL_SPRITES.add(platform)
            if obj == 'M':
                player = Player(x, y - 100)
            x += width
        y += height
    x = y = 0
    for row in level[1]:
        x = 0
        height = 64
        for obj in row:
            width = 64
            if obj == 'N':
                platform = BossGate(x, y, False)
                ALL_SPRITES.add(platform)
            if obj == 'Р':
                platform = BossGate(x, y, True)
                ALL_SPRITES.add(platform)
            if obj == 'Ъ':
                thing = HealCapsule(x, y, 2, -1)
                ALL_SPRITES.add(thing)
            if obj == '}':
                mob = Blaster(x, y)
            if obj == '{':
                mob = Blaster(x + 4, y, -1)
            if obj == '+':
                mob = OctopusBattery(x, y, 1)
            if obj == '=':
                mob = OctopusBattery(x, y)
            if obj == '@':
                mob = BigEye(x, y)
            if obj == 'Ж':
                mob = Mambu(x, y)
            if obj == 'C':
                boss = CutMan(x, y)
            x += width
        y += height
    for mob in MOBS:
        ALL_SPRITES.add(mob)
    for boss in BOSSES:
        ALL_SPRITES.add(boss)
    ALL_SPRITES.add(player)
    return player, x, y, boss


# Начальный экран
def start_screen():
    start_im = pygame.image.load('data/Sprites/Start screen.png')
    start_im = pygame.transform.scale(start_im, SIZE)
    show_help = True
    while True:
        screen.blit(start_im, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sys()
            if event.type == BLINKING_RECT:
                show_help = not show_help
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        if not show_help:
            pygame.draw.rect(screen, (0, 0, 0), (400, 400, 400, 50))
        pygame.display.flip()
        clock.tick(FPS)


# Выбор уровня
def stage_select():
    font = pygame.font.Font(None, 50)
    bosses = ['CutMan', 'GutsMan', 'IceMan', 'BombMan', 'FireMan', 'ElecMan']
    boss_coords = {'CutMan': [400, 96], 'GutsMan': [670, 100], 'IceMan': [830, 290],
                   'BombMan': [680, 480], 'FireMan': [380, 480], 'ElecMan': [230, 290]}
    boss_reward = [100000, 80000, 90000, 70000, 110000, 120000]
    cut_man_idle = [transform.scale(i, (96, 96)) for i in CUT_MAN_IDLE_W]
    cut_man_jump = transform.scale(CUT_MAN_JUMP_W, (96, 96))
    boss_name = pygame.Surface((400, 32), pygame.SRCALPHA)
    elems_in_name = 5
    clear_points = 0
    iteration = 0
    choice = 0
    boss_chosen = False
    in_jump = True
    anim_count = 0
    y_vel = 0
    STAGE_SELECT.play(-1)
    while True:
        if not boss_chosen:
            screen.blit(transform.scale(STAGE_SELECT_SCREEN[choice], SIZE), (0, 0))
            screen.blit(cut_man_idle[0], boss_coords['CutMan'])
        else:
            screen.blit(transform.scale(STAGE_SELECT_SCREEN[6], SIZE), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sys()
            if event.type == pygame.KEYDOWN and not boss_chosen:
                if event.key == pygame.K_RETURN:
                    if bosses[choice] == 'CutMan':
                        boss_chosen = True
                        y_vel -= 20
                        STAGE_SELECT.stop()
                        STAGE_CHOSEN.play(0)
                        GAME_START.play(0)
                if event.key == pygame.K_RIGHT:
                    if not boss_chosen:
                        choice += 1
                        MENU_SELECT.play(0)
                if event.key == pygame.K_LEFT:
                    if not boss_chosen:
                        choice -= 1
                        MENU_SELECT.play(0)
        if boss_chosen:
            if iteration in [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34]:
                screen.fill((255, 255, 255))
            if boss_coords[bosses[choice]][1] < SIZE[1] // 2.5 and in_jump:
                y_vel += GRAVITY_POWER
            if boss_coords[bosses[choice]][1] >= SIZE[1] // 2.5:
                in_jump = False
                y_vel = 0
            if in_jump:
                screen.blit(cut_man_jump, boss_coords[bosses[choice]])
            else:
                frame = 0
                if anim_count < 50:
                    frame = iteration % 20 // 10
                    anim_count += 1
                name_len = len(bosses[choice]) - elems_in_name
                for x in range(0, name_len * 32, 32):
                    boss_name.blit(FONT[bosses[choice][x // 32].upper()], (x, 0))
                if anim_count % 5 == 0:
                    elems_in_name -= 1 if elems_in_name != 0 else 0
                if anim_count == 50:
                    if clear_points < boss_reward[choice]:
                        clear_points += 1000
                    clear_points_s = font.render(str(clear_points), True, (255, 255, 255))
                    screen.blit(clear_points_s, (SIZE[0] // 2, SIZE[1] // 2))
                screen.blit(cut_man_idle[frame], boss_coords[bosses[choice]])
                screen.blit(boss_name, (SIZE[0] // 2, SIZE[1] // 2.5))
            boss_coords[bosses[choice]][1] += y_vel
            if iteration >= 300:
                return f'{bosses[choice]}'
            iteration += 1
        choice = abs(choice % 6)
        pygame.display.flip()
        clock.tick(FPS)


# Экран выбора действия после смерти
def continue_menu():
    main_font = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 50)
    buttons = ['CONTINUE', 'STAGE SELECT']
    main_text = main_font.render("GAME OVER", True, (255, 255, 255))
    score = main_font.render(f'Очков: {SCORE}', True, (255, 255, 255))
    buttons_text = [font.render(i, True, (255, 255, 255)) for i in buttons]
    coords = {'CONTINUE': (SIZE[0] // 5, SIZE[1] // 2),
              'STAGE SELECT': (SIZE[0] // 5, SIZE[1] // 1.5)}
    curcor_coords = {1: (SIZE[0] // 6, SIZE[1] // 1.97), 0: (SIZE[0] // 6, SIZE[1] // 1.48)}
    choice = 1
    GAME_OVER.play(0)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sys()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GAME_OVER.stop()
                    return choice
                if event.key == pygame.K_UP:
                    choice += 1
                if event.key == pygame.K_DOWN:
                    choice -= 1
        choice = abs(choice % 2)
        screen.blit(main_text, (SIZE[0] // 6, SIZE[1] // 5))
        screen.blit(score, (SIZE[0] // 5, SIZE[1] // 3))
        [screen.blit(buttons_text[i], coords[buttons[i]]) for i in range(len(buttons))]
        screen.blit(MENU_CURSOR, curcor_coords[choice])
        screen.blit(MEGAMAN_HELMET, (SIZE[0] // 1.7, SIZE[1] // 1.7))
        pygame.display.flip()
        clock.tick(FPS)


#  Победный экран
def victory_screen():
    main_font = pygame.font.Font(None, 70)
    background = transform.scale(load('data/Sprites/victory screen.png'), SIZE)
    font = pygame.font.Font(None, 50)
    menu_background = pygame.Surface((500, SIZE[1]), pygame.SRCALPHA)
    menu_background.fill((0, 0, 0, 70))
    buttons = ['OUT THE GAME', 'STAGE SELECT']
    main_text = main_font.render("YOU WIN", True, (255, 255, 255))
    score = main_font.render(f'Очков: {SCORE}', True, (255, 255, 255))
    buttons_text = [font.render(i, True, (255, 255, 255)) for i in buttons]
    coords = {'OUT THE GAME': (SIZE[0] // 5, SIZE[1] // 2),
              'STAGE SELECT': (SIZE[0] // 5, SIZE[1] // 1.5)}
    curcor_coords = {1: (SIZE[0] // 6, SIZE[1] // 1.97), 0: (SIZE[0] // 6, SIZE[1] // 1.48)}
    choice = 1
    iterations = 0
    VICTORY.play(0)
    while True:
        if iterations > 450:
            screen.blit(background, (0, 0))
            screen.blit(menu_background, (SIZE[0] // 8, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_sys()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GAME_OVER.stop()
                        return choice
                    if event.key == pygame.K_UP:
                        choice += 1
                    if event.key == pygame.K_DOWN:
                        choice -= 1
            choice = abs(choice % 2)
            screen.blit(main_text, (SIZE[0] // 6, SIZE[1] // 5))
            screen.blit(score, (SIZE[0] // 5, SIZE[1] // 3))
            [screen.blit(buttons_text[i], coords[buttons[i]]) for i in range(len(buttons))]
            screen.blit(MEGAMAN_STAND_HIS_BACK, (SIZE[0] // 1.7, SIZE[1] // 1.5))
            screen.blit(MENU_CURSOR, curcor_coords[choice])
        else:
            iterations += 1
        pygame.display.flip()
        clock.tick(FPS)


# Экран подготовки перед прохождением уровня
def ready():
    iteration = 0
    text = 'READY'
    font = pygame.font.Font(None, 50)
    text = font.render(text, 1, pygame.Color('white'))
    text_rect = text.get_rect()
    text_rect.center = (SIZE[0] // 2, SIZE[1] // 2)
    while iteration <= 190:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sys()
        screen.fill((0, 0, 0))
        if iteration // 30 in [1, 3, 5]:
            screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)
        iteration += 1
    CUT_MAN_STAGE.play(-1)


# Функция, печатающая количество очков на экране
def print_score():
    font = pygame.font.Font(None, 70)
    text = font.render(str(SCORE), 1, pygame.Color('white'))
    text_rect = text.get_rect()
    text_rect.centerx = SIZE[0] // 2
    screen.blit(text, (text_rect.x, 20))


# Класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image, hardness):
        super().__init__(PLATFORMS)
        self.image = load(f'data/Sprites/Окружение/Cut man stage/{image}.png').convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y)
        self.hardness = hardness


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = MEGAMAN_STAND[0]
        self.rect = self.image.get_rect(x=x, y=y, width=50, height=100)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_vel = self.y_vel = 0
        self.speed = 1
        self.hp = 40
        self.in_stage = False
        self.on_ground = False
        # Переменные, связаные с прыжками
        self.in_jump = False
        self.jump_was = False
        self.jump_was_0 = False
        self.jump_count = 10
        # Переменные, связаные с ходьбой
        self.in_walk = False
        # Переменные, связаные с лестницами
        self.on_stair = False
        self.near_stairs = False
        self.on_hard_stair = False
        self.want_down = False
        self.get_down_stair = False
        # Переменная невосприимчивости к урону
        self.impervious = False
        # Переменные, связаные со смертью персонажа
        self.is_dead = False
        self.death_coords = [self.rect.center for i in range(8)]
        self.death_coeff = [[0, 2], [2, 0], [0, -2], [-2, 0], [2, 2], [-2, -2], [-2, 2], [2, -2]]
        self.death_music = False
        # Переменные, связаные с направлением
        self.right = True
        # Переменные, связанные со стрельбой
        self.shot = False
        # Переменные, связанные с получением урона
        self.received_damage = False
        # Переменная, связанная с нахождением персонажа в комнате босса
        self.in_boss_room = False
        # Переменные - счётчики операций (для анимаций)
        self.anim_count_walk = 0
        self.anim_count_stand = 0
        self.anim_count_shot = 0
        self.anim_count_on_stair = 0
        self.anim_count_damage = 0
        self.death_count = 0
        self.anim_count_impervious = 0

    # Метод анимации героя
    def animation(self):
        if self.in_walk:
            frame = self.anim_count_walk // 7
            if self.right:
                if self.in_jump:
                    if self.shot:
                        self.change_image(MEGAMAN_JUMP_AND_SHOT)
                        self.anim_count_shot += 1.5
                    else:
                        self.change_image(MEGAMAN_JUMP)
                else:
                    if self.shot:
                        self.change_image(MEGAMAN_WALK_AND_SHOT[frame])
                        self.anim_count_shot += 1.5
                    else:
                        self.change_image(MEGAMAN_WALK[frame])
            else:
                if self.in_jump:
                    if self.shot:
                        self.change_image(pygame.transform.flip(MEGAMAN_JUMP_AND_SHOT, True, False))
                        self.anim_count_shot += 2
                    else:
                        self.change_image(pygame.transform.flip(MEGAMAN_JUMP, True, False))
                else:
                    if self.shot:
                        self.change_image(pygame.transform.flip(MEGAMAN_WALK_AND_SHOT[frame], True, False))
                        self.anim_count_shot += 1.5
                    else:
                        self.change_image(pygame.transform.flip(MEGAMAN_WALK[frame], True, False))
            self.anim_count_walk = self.anim_count_walk + 1 if self.anim_count_walk < 27 else 0
        elif self.received_damage:
            if self.anim_count_damage > 39:
                self.anim_count_damage = 0
                self.received_damage = False
            frame = self.anim_count_damage // 20
            if frame == 1:
                self.x_vel = 0
            if self.right:
                self.change_image(MEGAMAN_GET_DAMAGE[frame])
            else:
                self.change_image(pygame.transform.flip(MEGAMAN_GET_DAMAGE[frame], True, False))
            self.anim_count_damage += 1
        else:
            if self.on_stair:
                self.anim_count_on_stair = self.anim_count_on_stair if self.anim_count_on_stair < 19 else 0
                frame = self.anim_count_on_stair // 10
                self.change_image(MEGAMAN_ON_STAIR[frame])
                if self.get_down_stair:
                    self.change_image(MEGAMAN_GET_DOWN_STAIR)
                if self.shot:
                    if self.right:
                        self.change_image(MEGAMAN_SHOT_ON_STAIR)
                    else:
                        self.change_image(pygame.transform.flip(MEGAMAN_SHOT_ON_STAIR, True, False))
                    self.anim_count_shot += 1
            else:
                frame = self.anim_count_stand // 180
                if self.right:
                    if self.in_jump:
                        if self.shot:
                            self.change_image(MEGAMAN_JUMP_AND_SHOT)
                            self.anim_count_shot += 1.5
                        else:
                            self.change_image(MEGAMAN_JUMP)
                    elif self.shot:
                        self.change_image(MEGAMAN_SHOOT)
                        self.anim_count_shot += 1.5
                    else:
                        self.change_image(MEGAMAN_STAND[frame])
                else:
                    if self.in_jump:
                        if self.shot:
                            self.change_image(pygame.transform.flip(MEGAMAN_JUMP_AND_SHOT, True, False))
                            self.anim_count_shot += 1.5
                        else:
                            self.change_image(pygame.transform.flip(MEGAMAN_JUMP, True, False))
                    elif self.shot:
                        self.change_image(pygame.transform.flip(MEGAMAN_SHOOT, True, False))
                        self.anim_count_shot += 1.5
                    else:
                        self.change_image(pygame.transform.flip(MEGAMAN_STAND[frame], True, False))
                self.anim_count_stand = 0 if self.anim_count_stand > 200 else self.anim_count_stand + 1
        if not self.in_stage:
            self.change_image(MEGAMAN_TELEPORT_1)
        if self.anim_count_shot > 30:
            self.anim_count_shot = 0
            self.shot = False
        if self.impervious:
            if self.anim_count_impervious % 8 == 0:
                self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.anim_count_impervious += 1
            if self.anim_count_impervious > 100:
                self.impervious = False
                self.anim_count_impervious = 0

    # Метод для обнаружения столкновений
    def collides_detect(self, x_vel, y_vel):
        # Проверка на столкновения персонажа с вражескими пулями
        if pygame.sprite.spritecollide(self, ENEMY_BULLETS, False):
            for sprite in ENEMY_BULLETS:
                if pygame.sprite.collide_rect(self, sprite):
                    self.get_damage(sprite.damage)
                    if sprite.__class__ != RollingCutter:
                        sprite.kill()
        # Проверка на столкновения персонажа с врагами
        if pygame.sprite.spritecollide(self, MOBS, False):
            for sprite in MOBS:
                if pygame.sprite.collide_rect(self, sprite) and sprite.danger:
                    self.get_damage(sprite.damage)
        # Проверка столкновения персонажа с боссом
        if pygame.sprite.spritecollide(self, BOSSES, False):
            for sprite in BOSSES:
                if pygame.sprite.collide_rect(self, sprite) and sprite.danger:
                    self.get_damage(sprite.damage)
        # Проверка на столкновения персонажа с шипами
        if pygame.sprite.spritecollide(self, SPIKES, False):
            for sprite in SPIKES:
                if pygame.sprite.collide_mask(self, sprite):
                    if x_vel > 0:
                        self.x_vel = 0
                        self.rect.right = sprite.rect.left
                    if x_vel < 0:
                        self.x_vel = 0
                        self.rect.left = sprite.rect.right
                    if y_vel > 0:
                        self.rect.y = 0
                        self.rect.bottom = sprite.rect.top
                    self.hp = 0
        # Проверка столкновения персонажа с платформами
        for sprite in PLATFORMS:
            if sprite.__class__ == BossGate:
                if self.rect.x > sprite.rect.right and not sprite.is_close_always:
                    self.in_boss_room = sprite.before_boss
                    sprite.closed = True
                    sprite.is_close_always = True
            if pygame.sprite.collide_rect(self, sprite) and sprite.hardness:
                if x_vel > 0:
                    if sprite.__class__ == BossGate:
                        sprite.opened = True
                    self.x_vel = 0
                    self.rect.right = sprite.rect.left
                if x_vel < 0:
                    self.x_vel = 0
                    self.rect.left = sprite.rect.right
                if y_vel > 0:
                    self.y_vel = 0
                    self.jump_count = 10
                    if self.in_jump or not self.in_stage:
                        MEGAMAN_LAND.play(0)
                    self.on_ground = True
                    self.in_jump = False
                    self.on_stair = False
                    self.in_stage = True
                    self.rect.bottom = sprite.rect.top
                if y_vel < 0:
                    self.y_vel = 0
                    self.jump_was = False
                    self.rect.top = sprite.rect.bottom
        # Проверка столкновения персонажа с лестницами
        if pygame.sprite.spritecollide(self, STAIRS, False):
            self.near_stairs = True
            for sprite in STAIRS:
                if pygame.sprite.collide_rect(self, sprite):
                    if self.on_stair:
                        self.rect.centerx = sprite.rect.centerx
                        if sprite.hardness:
                            if abs(self.rect.bottom - sprite.rect.top) <= 15:
                                self.get_down_stair = True
                            else:
                                self.get_down_stair = False
                    if y_vel > 0 and sprite.hardness and not self.want_down and self.in_stage:
                        if abs(self.rect.bottom - sprite.rect.top) <= 20:
                            self.y_vel = 0
                            if self.in_jump or not self.in_stage:
                                MEGAMAN_LAND.play(0)
                            self.on_ground = True
                            self.in_jump = False
                            self.on_stair = False
                            self.jump_count = 10
                            self.on_hard_stair = True
                            self.rect.bottom = sprite.rect.top
                    else:
                        self.on_hard_stair = False
        else:
            self.get_down_stair = False
            self.near_stairs = False
            self.on_stair = False

    # Метод обновления персонажа
    def update(self, jump, up, left, right, down):
        self.animation()
        if right and self.in_stage:
            self.right = True
            if not self.on_stair and not self.received_damage:
                if self.on_ground:
                    self.in_walk = True
                if self.x_vel <= 6:
                    self.x_vel += self.speed
        if left and self.in_stage:
            self.right = False
            if not self.on_stair and not self.received_damage:
                if self.on_ground:
                    self.in_walk = True
                if self.x_vel >= -6:
                    self.x_vel += -self.speed
        if jump and not self.received_damage:
            if self.on_ground and not self.jump_was and not self.on_stair and not self.jump_was_0:
                self.in_jump = True
                self.in_walk = False
                self.jump_was = True
                self.jump_was_0 = True
                self.y_vel -= JUMP_POWER
            if self.on_stair:
                self.on_stair = False
                self.in_jump = True
                self.jump_was = False
            if self.in_jump and self.jump_was:
                if self.jump_count > 0:
                    if self.y_vel > -15:
                        self.y_vel -= JUMP_POWER
                    self.jump_count -= 1
        else:
            self.jump_was = False
            self.jump_was_0 = False
        if up and not self.received_damage:
            if self.near_stairs and not self.on_hard_stair:
                self.on_stair = True
                self.y_vel = 0
                self.in_jump = False
                self.in_walk = False
            if self.on_stair:
                self.y_vel = -1.2
                if self.shot:
                    self.y_vel = 0
                self.anim_count_on_stair += 1
        if down and not self.received_damage:
            if self.near_stairs:
                if not self.on_hard_stair and not self.on_ground:
                    self.on_stair = True
                    self.in_walk = False
                else:
                    self.want_down = True
            if self.on_stair:
                self.y_vel = 2
                if self.shot:
                    self.y_vel = 0
                self.anim_count_on_stair += 1
        if not (up or down):
            if self.on_stair:
                self.y_vel = 0
            self.want_down = False
        if not (left or right):
            if not self.received_damage:
                self.x_vel = 0
            self.in_walk = False
            self.anim_count_walk = 0
        if not self.on_ground:
            if not self.on_stair:
                self.y_vel += GRAVITY_POWER
        self.on_ground = False
        self.rect.x += self.x_vel
        self.collides_detect(self.x_vel, 0)
        self.rect.y += self.y_vel
        self.collides_detect(0, self.y_vel)
        if self.rect.y > SIZE[1] and self.in_stage:
            self.hp = 0

    # Метод стрельбы
    def shoot(self):
        if len(BULLETS) < 3 and self.in_stage and not self.received_damage:
            self.shot = True
            if self.right:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self, -1)
            ALL_SPRITES.add(bullet)
            self.anim_count_shot = 0
            MEGA_BUSTER.play(0)

    # Метод получения урона
    def get_damage(self, damage):
        if not self.received_damage and not self.impervious:
            self.received_damage = True
            self.impervious = True
            self.in_walk = False
            self.on_stair = False
            self.shot = False
            if self.right:
                self.x_vel = -3
            else:
                self.x_vel = 3
            self.anim_count_damage = 0
            self.y_vel = 0
            self.hp = self.hp - damage if self.hp - damage >= 0 else 0
            if self.hp > 0:
                MEGAMAN_GET_DAMAGE_S.play(0)

    # Метод получения хп (жизнинной энергии)
    def get_hp(self, hp):
        self.hp = self.hp + hp if self.hp + hp <= 40 else 40

    # Метод смены спрайта
    def change_image(self, image):
        self.image = image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)


# Классы врагов

# Класс висящих на стенах бластеров
class Blaster(pygame.sprite.Sprite):
    def __init__(self, x, y, r=1):
        super(Blaster, self).__init__(MOBS)
        self.spawn_coords = [x, y]
        self.image = BLASTER[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.right = r
        self.damage = 1
        self.bullet_damage = 2
        self.removal_from_center = 30 if r == 1 else 40
        self.danger = True
        self.active = False
        self.in_attack = False
        self.attack = 0
        self.is_show = False
        self.anim_count = 0
        self.dead_anim_count = 0
        self.in_attack_anim_count = 0
        self.directtions = {0: [1, -0.8], 1: [1, -0.2], 2: [1, 0.2], 3: [1, 0.8]}
        if r == -1:
            self.directtions = {0: [-1, -0.8], 1: [-1, -0.2], 2: [-1, 0.2], 3: [-1, 0.8]}
        self.hitbox = self.rect.copy()
        self.hitbox.width = 36
        if r == -1:
            self.hitbox.x = self.rect.x + 24
        self.initialized = True

    # Метод анимации
    def animation(self):
        if self.danger:
            if not self.is_show:
                if self.anim_count > 128:
                    self.is_show = True
                self.anim_count += 1
            else:
                if self.anim_count < -70:
                    self.is_show = False
                    self.attack = 0
                self.anim_count -= 1
            frame = 0
            self.in_attack = False
            if 10 <= self.anim_count < 20:
                frame = 1
            elif 20 <= self.anim_count < 30:
                frame = 2
                self.in_attack = True
            elif 30 <= self.anim_count <= 130:
                frame = 3
                self.in_attack = True
            if self.right == 1:
                self.image = BLASTER[frame].convert_alpha()
            else:
                self.image = transform.flip(BLASTER[frame], True, False)
        else:
            if self.dead_anim_count < 27:
                frame = self.dead_anim_count // 7
                self.image = ENEMIES_DESTROY[frame]
                self.dead_anim_count += 1
            else:
                self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]

    # Метод обнаружения столкновений
    def collide_detect(self):
        global SCORE
        if pygame.sprite.spritecollide(self, BULLETS, False):
            for sprite in BULLETS:
                if pygame.Rect.colliderect(self.hitbox, sprite.rect) and self.danger:
                    if self.in_attack:
                        self.drop()
                        ENEMY_DAMAGE_S.play(0)
                        self.danger = False
                        SCORE += 200
                    else:
                        EMPTY_SHOT.play(0)
                    sprite.kill()

    # Метод обновления
    def update(self, hero):
        if -100 < self.spawn_coords[0] < SIZE[0] + 100 and -100 < self.spawn_coords[1] < SIZE[1] + 100 \
                or (-100 < self.rect.x < SIZE[0] + 100 and -100 < self.rect.y < SIZE[1] + 100):
            self.active = True
            self.initialized = False
        else:
            if not self.initialized:
                self.danger = True
                self.in_attack = False
                self.attack = 0
                self.is_show = False
                self.anim_count = 0
                self.dead_anim_count = 0
                self.in_attack_anim_count = 0
                self.initialized = True
                self.active = False
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]
        if self.active:
            self.animation()
            self.hitbox_update()
            self.collide_detect()
            if self.in_attack:
                if self.anim_count in [30, 60, 90, 120] and self.attack < 4:
                    self.shoot(self.attack)
                    self.attack += 1

    # Метод стрельбы
    def shoot(self, attack):
        bullet = EnemiesBullet(self.rect.centerx + self.removal_from_center * self.right,
                               self.rect.centery - 5, self.bullet_damage, self.directtions[attack], 7)
        ALL_SPRITES.add(bullet)
        ENEMY_SHOOT_S.play(0)

    # Метод обновления хитбокса (области, при поподании в которую объект получает урон)
    def hitbox_update(self):
        self.hitbox.x = self.rect.x
        if self.right == -1:
            self.hitbox.x = self.rect.x + 24
        self.hitbox.y = self.rect.y

    # Метод выпадения предмета после уничтожения
    def drop(self):
        chance = rint(1, 100)
        if chance in range(10, 50):
            drop = BonusBall(*self.rect.center)
            ALL_SPRITES.add(drop)
        elif chance in range(70, 90):
            if chance in range(70, 81):
                drop = HealCapsule(*self.rect.center, 1, 0)
            else:
                drop = HealCapsule(*self.rect.center, 2, 0)
            ALL_SPRITES.add(drop)


# Класс робота-присоски
class OctopusBattery(pygame.sprite.Sprite):
    def __init__(self, x, y, direct=0):
        super(OctopusBattery, self).__init__(MOBS)
        self.spawn_coords = [x, y]
        self.image = OCTOPUS_BATTERY[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.damage = 4
        self.danger = True
        self.active = False
        self.direction = [0, 5] if direct else [5, 0]
        self.open_eye = False
        self.movement = True
        self.anim_count = 0
        self.dead_anim_count = 0
        self.inactivity_count = 0
        self.hp = 40
        self.initialized = False

    # Метод анимации
    def animation(self):
        if self.danger:
            if not self.movement:
                if not self.open_eye:
                    if self.anim_count < 60:
                        self.anim_count += 1
                else:
                    if self.anim_count > 0:
                        self.anim_count -= 1
                if self.anim_count == 60:
                    self.open_eye = True
                    self.movement = True
                if self.anim_count == 0:
                    self.open_eye = False
            if self.open_eye:
                if 40 <= self.anim_count < 50:
                    self.image = OCTOPUS_BATTERY[0]
                if 50 <= self.anim_count < 60:
                    self.image = OCTOPUS_BATTERY[1]
            else:
                if 20 <= self.anim_count < 30:
                    self.image = OCTOPUS_BATTERY[0]
                elif 30 <= self.anim_count < 40:
                    self.image = OCTOPUS_BATTERY[1]
                elif 40 <= self.anim_count < 50:
                    self.image = OCTOPUS_BATTERY[2]
        else:
            if self.dead_anim_count < 27:
                frame = self.dead_anim_count // 7
                self.image = ENEMIES_DESTROY[frame]
                self.dead_anim_count += 1
            else:
                self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]

    # Метод обнаружения столкновений
    def collide_detect(self):
        if pygame.sprite.spritecollide(self, BULLETS, False):
            for sprite in BULLETS:
                if pygame.Rect.colliderect(self.rect, sprite.rect) and self.danger:
                    ENEMY_DAMAGE_S.play(0)
                    self.get_damage(sprite.damage)
                    sprite.kill()
        if pygame.sprite.spritecollide(self, PLATFORMS, False):
            for sprite in PLATFORMS:
                if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.hardness:
                    if self.direction[0] < 0:
                        self.direction[0] = -self.direction[0]
                        self.rect.left = sprite.rect.right
                        self.movement = False
                    elif self.direction[0] > 0:
                        self.rect.right = sprite.rect.left
                        self.direction[0] = -self.direction[0]
                        self.movement = False
                    if self.direction[1] < 0:
                        self.direction[1] = -self.direction[1]
                        self.rect.top = sprite.rect.bottom
                        self.movement = False
                    elif self.direction[1] > 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction[1] = -self.direction[1]
                        self.movement = False

    # Метод обновления
    def update(self, hero):
        global SCORE
        if -100 < self.spawn_coords[0] < SIZE[0] + 100 and -100 < self.spawn_coords[1] < SIZE[1] + 100 \
                or (-100 < self.rect.x < SIZE[0] + 100 and -100 < self.rect.y < SIZE[1] + 100):
            self.active = True
            self.initialized = False
        else:
            if not self.initialized:
                self.danger = True
                self.anim_count = 0
                self.dead_anim_count = 0
                self.hp = 40
                self.active = False
                self.initialized = True
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]
        if self.active:
            self.animation()
            if self.hp == 0 and self.danger:
                self.drop()
                self.danger = False
                self.movement = False
                SCORE += 300
            self.collide_detect()
            if self.movement:
                self.rect.x += self.direction[0]
                self.rect.y += self.direction[1]

    # Метод получения урона
    def get_damage(self, dam):
        self.hp = self.hp - dam if self.hp - dam > 0 else 0

    # Метод выпадения предмета после уничтожения
    def drop(self):
        chance = rint(1, 100)
        if chance in range(10, 50):
            drop = BonusBall(*self.rect.center)
            ALL_SPRITES.add(drop)
        elif chance in range(70, 90):
            if chance in range(70, 81):
                drop = HealCapsule(*self.rect.center, 1, 0)
            else:
                drop = HealCapsule(*self.rect.center, 2, 0)
            ALL_SPRITES.add(drop)


# Класс большого прыгающего одноглазого робота
class BigEye(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BigEye, self).__init__(MOBS)
        self.spawn_coords = [x, y]
        self.image = BIG_EYE[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.rect.width = 90
        self.x_vel = 0
        self.y_vel = 0
        self.damage = 10
        self.danger = True
        self.active = False
        self.right = True
        self.on_ground = False
        self.jump_powers = [15, 25]
        self.on_ground_anim_count = 0
        self.anim_count = 0
        self.dead_anim_count = 0
        self.inactivity_count = 0
        self.hp = 100
        self.initialized = False

    # Метод анимации
    def animation(self):
        if self.danger:
            if self.on_ground_anim_count == 0:
                if self.right:
                    self.image = BIG_EYE[1]
                else:
                    self.image = transform.flip(BIG_EYE[1], True, False)
            else:
                if self.right:
                    self.image = BIG_EYE[0]
                else:
                    self.image = transform.flip(BIG_EYE[0], True, False)
        else:
            if self.dead_anim_count < 27:
                frame = self.dead_anim_count // 7
                self.image = ENEMIES_DESTROY[frame]
                self.dead_anim_count += 1
            else:
                self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]

    # Метод обнаружения столкновений
    def collide_detect(self, x_vel, y_vel):
        if pygame.sprite.spritecollide(self, PLATFORMS, False):
            for sprite in PLATFORMS:
                if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.hardness:
                    if x_vel > 0:
                        self.x_vel = 0
                        self.rect.right = sprite.rect.left
                    if x_vel < 0:
                        self.x_vel = 0
                        self.rect.left = sprite.rect.right
                    if y_vel > 0:
                        self.y_vel = 0
                        self.on_ground = True
                        self.rect.bottom = sprite.rect.top
                    if y_vel < 0:
                        self.y_vel = 0
                        self.rect.top = sprite.rect.bottom
        if pygame.sprite.spritecollide(self, BULLETS, False):
            for sprite in BULLETS:
                if pygame.sprite.collide_rect(self, sprite) and self.danger:
                    ENEMY_DAMAGE_S.play(0)
                    self.get_damage(sprite.damage)
                    sprite.kill()

    # Метод обновления
    def update(self, hero):
        global SCORE
        if -100 < self.spawn_coords[0] < SIZE[0] + 100 and -100 < self.spawn_coords[1] < SIZE[1] + 100 \
                or (-100 < self.rect.x < SIZE[0] + 100 and -100 < self.rect.y < SIZE[1] + 100):
            self.active = True
            self.initialized = False
        else:
            if not self.initialized:
                self.danger = True
                self.anim_count = 0
                self.dead_anim_count = 0
                self.hp = 60
                self.active = False
                self.initialized = True
                self.rect.x, self.rect.y = self.spawn_coords[0], self.spawn_coords[1]
        if self.active:
            self.animation()
            if self.danger:
                if not self.on_ground:
                    self.y_vel += GRAVITY_POWER
                else:
                    self.on_ground_anim_count += 1
                    self.x_vel = 0
                    if hero.rect.centerx < self.rect.centerx:
                        self.right = False
                    else:
                        self.right = True
                self.on_ground = False
                if self.hp == 0:
                    self.drop()
                    self.danger = False
                    SCORE += 9000
                self.rect.x += self.x_vel
                self.collide_detect(self.x_vel, 0)
                self.rect.y += self.y_vel
                self.collide_detect(0, self.y_vel)
                if self.on_ground_anim_count > 40:
                    jump_power = rint(0, 5)
                    if jump_power > 3:
                        self.y_vel -= self.jump_powers[1]
                    else:
                        self.y_vel -= self.jump_powers[0]
                    BIG_EYE_S.play(0)
                    self.on_ground_anim_count = 0
                if self.on_ground_anim_count == 0:
                    if not self.right:
                        self.x_vel = -5
                    else:
                        self.x_vel = 5

    # Метод получения урона
    def get_damage(self, dam):
        self.hp = self.hp - dam if self.hp - dam > 0 else 0

    # Метод выпадения предмета после уничтожения
    def drop(self):
        chance = rint(1, 100)
        if chance in range(10, 50):
            drop = BonusBall(*self.rect.center)
            ALL_SPRITES.add(drop)
        elif chance in range(70, 90):
            if chance in range(70, 81):
                drop = HealCapsule(*self.rect.center, 1, 0)
            else:
                drop = HealCapsule(*self.rect.center, 2, 0)
            ALL_SPRITES.add(drop)


# Класс бронированного шарика, стреляющего в 8 напрвлениях
class Mambu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Mambu, self).__init__(MOBS)
        self.spawn_coords = [x, y]
        self.image = MAMBU[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.damage = 4
        self.danger = True
        self.active = False
        self.open_shell = False
        self.directions = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
        self.anim_count = 0
        self.showed = False
        self.dead_anim_count = 0
        self.inactivity_count = 0
        self.initialized = False

    # Метод анимации
    def animation(self):
        if self.danger:
            if self.open_shell:
                self.image = transform.flip(MAMBU[1], True, False)
                if self.anim_count > 40:
                    self.anim_count = 0
                    self.open_shell = False
                self.anim_count += 1
            else:
                self.image = transform.flip(MAMBU[0], True, False)
        else:
            if self.dead_anim_count < 27:
                frame = self.dead_anim_count // 7
                self.image = ENEMIES_DESTROY[frame]
                self.dead_anim_count += 1
            else:
                self.rect.x, self.rect.y = self.spawn_coords
                self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
                self.danger = True
                self.showed = False

    # Метод обнаружения столкновений
    def collide_detect(self):
        global SCORE
        if pygame.sprite.spritecollide(self, BULLETS, False):
            for sprite in BULLETS:
                if pygame.Rect.colliderect(self.rect, sprite.rect) and self.danger:
                    if self.open_shell:
                        self.drop()
                        ENEMY_DAMAGE_S.play(0)
                        self.danger = False
                        self.dead_anim_count = 0
                        SCORE += 800
                    else:
                        EMPTY_SHOT.play(0)
                    sprite.kill()

    # Метод обновления
    def update(self, hero):
        if -100 < self.rect.x < SIZE[0] * 2 and -100 < self.rect.y < SIZE[1] + 100:
            self.active = True
            self.initialized = False
        else:
            if not self.initialized:
                self.rect.x, self.rect.y = self.spawn_coords
                self.danger = True
                self.active = False
                self.inactivity_count = 0
                self.initialized = True
        if 0 < self.spawn_coords[0] < SIZE[0] and 0 < self.spawn_coords[1] < SIZE[1]:
            if not self.active:
                self.showed = False
                self.inactivity_count = 0
        else:
            self.showed = True
        if self.active and self.showed:
            self.animation()
            self.collide_detect()
            if self.inactivity_count > 120:
                self.open_shell = True
                self.shoot()
                self.inactivity_count = 0
            self.inactivity_count += 1
            if not self.open_shell:
                self.rect.x -= 3
        else:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.rect.x, self.rect.y = self.spawn_coords

    # Метод выпадения предмета после уничтожения
    def drop(self):
        chance = rint(1, 100)
        if chance in range(10, 50):
            drop = BonusBall(*self.rect.center)
            ALL_SPRITES.add(drop)
        elif chance in range(70, 90):
            if chance in range(70, 81):
                drop = HealCapsule(*self.rect.center, 1, 0)
            else:
                drop = HealCapsule(*self.rect.center, 2, 0)
            ALL_SPRITES.add(drop)

    # Метод стрельбы
    def shoot(self):
        bullet_positions = [[*self.rect.topleft], [self.rect.centerx, self.rect.top],
                            [*self.rect.topright], [self.rect.right, self.rect.centery],
                            [*self.rect.bottomright], [self.rect.centerx, self.rect.bottom],
                            [*self.rect.bottomleft], [self.rect.left, self.rect.centery]]
        for i in range(8):
            bullet = EnemiesBullet(*bullet_positions[i], 5, self.directions[i], 6)
            ALL_SPRITES.add(bullet)


# Класс босса "Кат Мен"
class CutMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(CutMan, self).__init__(BOSSES)
        self.image = CUT_MAN_IDLE_W[0]
        self.rect = self.image.get_rect(x=x, y=y, width=70, height=110)
        self.x_vel = self.y_vel = 0
        self.hp = 40
        self.damage = 5
        self.damage_cutter = 6
        self.speed = 3
        self.jumps_power = 25
        self.death_coords = [list(self.rect.center) for i in range(8)]
        self.death_coeff = [[0, 2], [2, 0], [0, -2], [-2, 0], [2, 2], [-2, -2], [-2, 2], [2, -2]]
        self.ready_attack = False
        self.in_stage = False
        self.on_ground = False
        self.right = False
        self.with_cutter = True
        self.active = False
        self.danger = True
        self.in_jump = False
        self.in_walk = True
        self.damage_was = False
        self.impervious = False
        self.dead = False
        self.impervious_count = 0
        self.anim_count_walk = 0
        self.on_ground_count = 0
        self.ready_attack_count = 0
        self.death_count = 0

    # Метод анимации
    def animation(self, hero):
        if self.danger:
            if self.in_jump:
                if self.right:
                    if self.with_cutter:
                        self.image = CUT_MAN_JUMP_W
                    else:
                        self.image = CUT_MAN_JUMP
                else:
                    if self.with_cutter:
                        self.image = transform.flip(CUT_MAN_JUMP_W, True, False)
                    else:
                        self.image = transform.flip(CUT_MAN_JUMP, True, False)
            if self.on_ground:
                if self.in_walk:
                    if self.anim_count_walk > 8:
                        self.anim_count_walk = 0
                    frame = self.anim_count_walk // 3
                    if self.right:
                        if self.with_cutter:
                            self.image = CUT_MAN_WALK_W[frame]
                        else:
                            self.image = CUT_MAN_WALK[frame]
                    else:
                        if self.with_cutter:
                            self.image = transform.flip(CUT_MAN_WALK_W[frame], True, False)
                        else:
                            self.image = transform.flip(CUT_MAN_WALK[frame], True, False)
                    self.anim_count_walk += 1
                else:
                    if self.right:
                        if self.with_cutter:
                            self.image = CUT_MAN_IDLE_W[0]
                        else:
                            self.image = CUT_MAN_IDLE
                    else:
                        if self.with_cutter:
                            self.image = transform.flip(CUT_MAN_IDLE_W[0], True, False)
                        else:
                            self.image = transform.flip(CUT_MAN_IDLE, True, False)
            if self.impervious:
                if self.impervious_count % 10 == 0:
                    self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                if self.impervious_count >= 100:
                    self.impervious = False
                    self.impervious_count = 0
                if self.impervious_count == 40:
                    self.damage_was = False
                    self.x_vel = 0
                self.impervious_count += 1
            if self.ready_attack and not self.damage_was and self.with_cutter:
                if self.ready_attack_count > 25:
                    self.ready_attack_count = 0
                    self.ready_attack = False
                    self.attack(hero)
                    self.with_cutter = False
                self.ready_attack_count += 1
                frame = self.ready_attack_count // 20
                if self.right:
                    self.image = CUT_MAN_TOSS[frame]
                else:
                    self.image = transform.flip(CUT_MAN_TOSS[frame], True, False)
        else:
            if not self.dead:
                self.death_coords = [list(self.rect.center) for i in range(8)]
                self.dead = True
                self.drop()
                self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
                BOSS_BATTLE.stop()
                MEGAMAN_DEATH_S.play(0)
                self.active = False

    # Метод обновления
    def update(self, hero):
        if hero.in_boss_room and not self.dead and not self.in_stage:
            self.active = True
            self.in_stage = True
            CUT_MAN_STAGE.stop()
            BOSS_BATTLE.play(-1)
        if self.active:
            self.animation(hero)
            distance = hero.rect.x - self.rect.x
            if distance > 100:
                self.right = True
            elif distance < -100:
                self.right = False
            if distance <= 400:
                if self.on_ground and not self.damage_was:
                    if self.on_ground_count >= 10:
                        self.jump()
                    self.on_ground_count += 1
            if not self.on_ground:
                self.y_vel += GRAVITY_POWER // 1.1
            if self.on_ground and not self.damage_was and not self.ready_attack:
                if self.right:
                    self.x_vel = 5
                    self.in_walk = True
                else:
                    self.x_vel = -5
                    self.in_walk = True
            if self.in_jump:
                if self.x_vel == 0:
                    if self.right:
                        self.x_vel = 3
                    else:
                        self.x_vel = -3
            if self.hp == 0 and not self.dead:
                self.danger = False
            self.on_ground = False
            self.rect.x += self.x_vel
            self.collide_detect(self.x_vel, 0)
            self.rect.y += self.y_vel
            self.collide_detect(0, self.y_vel)

    # Метод обнаружения столкновений
    def collide_detect(self, x_vel, y_vel):
        if pygame.sprite.spritecollide(self, PLATFORMS, False):
            for sprite in PLATFORMS:
                if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.hardness:
                    if x_vel > 0:
                        self.x_vel = 0
                        self.rect.right = sprite.rect.left
                    if x_vel < 0:
                        self.x_vel = 0
                        self.rect.left = sprite.rect.right
                    if y_vel > 0:
                        self.y_vel = 0
                        self.on_ground = True
                        self.in_jump = False
                        self.rect.bottom = sprite.rect.top
                    if y_vel < 0:
                        self.y_vel = 0
                        self.rect.top = sprite.rect.bottom
        if pygame.sprite.spritecollide(self, BULLETS, False):
            for sprite in BULLETS:
                if pygame.sprite.collide_rect(self, sprite) and self.danger:
                    self.get_damage(sprite.damage)
                    sprite.kill()
        if pygame.sprite.spritecollide(self, ENEMY_BULLETS, False):
            for sprite in ENEMY_BULLETS:
                if pygame.sprite.collide_rect(self, sprite):
                    if sprite.__class__ == RollingCutter:
                        if sprite.return_to_enemy:
                            self.with_cutter = True
                            ROLLING_CUTTER_S.stop()
                            sprite.kill()

    # Метод получения урона
    def get_damage(self, dam):
        if not self.impervious and not self.damage_was:
            if self.right:
                self.x_vel = -1
            else:
                self.x_vel = 1
            self.damage_was = True
            self.impervious = True
            self.in_walk = False
            if self.with_cutter:
                self.ready_attack = True
            self.hp = self.hp - (dam - 1) if self.hp - (dam - 1) >= 0 else 0
            if self.hp > 0:
                ENEMY_DAMAGE_S.play(0)

    # Метод прыжка
    def jump(self):
        self.in_jump = True
        self.in_walk = False
        self.y_vel -= self.jumps_power
        self.on_ground_count = 0

    # Метод выпадения предмета после уничтожения
    def drop(self):
        drop = MegaBall(*self.rect.center)
        ALL_SPRITES.add(drop)

    # Метод атаки
    def attack(self, hero):
        cutter = RollingCutter(self.rect.centerx, self.rect.top, hero.rect.x,
                               hero.rect.y, self.damage_cutter)
        ALL_SPRITES.add(cutter)


# Класс ножниц-бумеранга
class RollingCutter(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, dam):
        super(RollingCutter, self).__init__(ENEMY_BULLETS)
        self.image = ROLLING_CUTTER_IMAGE[0]
        self.rect = self.image.get_rect(x=x, y=y)
        self.return_to_enemy = False
        self.damage = dam
        self.anim_count = 0
        vector = pygame.math.Vector2
        self.direction = vector(x1, y1) - vector(x, y)
        self.way = 0
        self.distance = int(self.direction.length()) // 2
        ROLLING_CUTTER_S.play(-1)

    # Метод анимации
    def animation(self):
        if self.anim_count > 27:
            self.anim_count = 0
        frame = self.anim_count // 7
        self.image = ROLLING_CUTTER_IMAGE[frame]

    # Метод обновления
    def update(self):
        self.animation()
        if [i.hp for i in BOSSES][0] == 0:
            ROLLING_CUTTER_S.stop()
            self.kill()
        if not self.return_to_enemy:
            self.rect.x += self.direction.x // 50
            self.rect.y += self.direction.y // 50
            if self.way >= self.distance or self.rect.x not in range(-100, SIZE[0] + 100) \
                    or self.rect.y not in range(-100, SIZE[1] + 100):
                self.return_to_enemy = True
            self.way += 2
        else:
            x = [i.rect.x for i in BOSSES][0]
            y = [i.rect.y for i in BOSSES][0]
            if self.rect.x < x:
                self.rect.x += 10
            elif self.rect.x > x:
                self.rect.x -= 10
            if self.rect.y < y:
                self.rect.y += 10
            elif self.rect.y > y:
                self.rect.y -= 10
        self.anim_count += 1


# Класс врат босса
class BossGate(pygame.sprite.Sprite):
    def __init__(self, x, y, before_boss):
        super(BossGate, self).__init__(PLATFORMS)
        self.elems = 3
        self.image = pygame.Surface((64, 64 * self.elems), pygame.SRCALPHA)
        for i in range(0, 64 * self.elems + 1, 64):
            self.image.blit(BOSS_GATE_IMAGE, (0, i))
        self.rect = self.image.get_rect(x=x, y=y)
        self.anim_count = 0
        self.before_boss = before_boss
        self.opened = False
        self.hardness = True
        self.is_open = False
        self.closed = False
        self.is_close_always = False

    # Метод обновления
    def update(self):
        if self.opened:
            self.anim_count += 1
            if self.anim_count in [20, 40, 60]:
                self.elems -= 1
                self.update_image()
                BOSS_GATE_S.play(0)
            if self.anim_count > 60:
                self.elems = 0
                self.opened = False
                self.is_open = True
                self.anim_count = 0
        if self.closed:
            self.is_open = False
            self.anim_count += 1
            if self.anim_count in [20, 40, 60]:
                self.elems += 1
                self.update_image()
                BOSS_GATE_S.play(0)
            if self.anim_count >= 60:
                self.closed = False
                self.anim_count = 0
        self.hardness = not self.is_open

    # Метод смены спрайта
    def update_image(self):
        self.image = pygame.Surface((64, 64 * 3), pygame.SRCALPHA)
        if self.elems > 0:
            for i in range(0, 64 * self.elems, 64):
                self.image.blit(BOSS_GATE_IMAGE, (0, i))
        self.rect = self.image.get_rect(x=self.rect.x, y=self.rect.y)


# Класс бонусных шаров
class BonusBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BonusBall, self).__init__(BONUS_BALLS)
        self.image = BONUS_BALL
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.on_ground = False
        self.life_time = 0
        self.cost = 1000

    # Метод обнаружения столкновений
    def collide_detect(self, hero):
        global SCORE
        if pygame.sprite.collide_rect(self, hero):
            SCORE += self.cost
            BONUS_BALL_S.play(0)
            self.kill()
        if not self.on_ground:
            if pygame.sprite.spritecollide(self, PLATFORMS, False):
                for sprite in PLATFORMS:
                    if pygame.sprite.collide_rect(self, sprite) and sprite.hardness:
                        self.on_ground = True
                        self.rect.bottom = sprite.rect.top

    # Метод обновления
    def update(self, hero):
        self.collide_detect(hero)
        if not self.on_ground:
            self.rect.y += GRAVITY_POWER * 10
        if self.on_ground:
            self.life_time += 1
        if self.life_time >= 300:
            self.kill()


# Класс бонусных шаров
class MegaBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(MegaBall, self).__init__(BONUS_BALLS)
        self.image = MEGA_BALL
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.on_ground = False
        self.cost = 100000

    # Метод обнаружения столкновений
    def collide_detect(self, hero):
        global SCORE, BOSSES
        if pygame.sprite.collide_rect(self, hero):
            SCORE += self.cost
            BOSSES = Group()
            BONUS_BALL_S.play(0)
            self.kill()
        if not self.on_ground:
            if pygame.sprite.spritecollide(self, PLATFORMS, False):
                for sprite in PLATFORMS:
                    if pygame.sprite.collide_rect(self, sprite) and sprite.hardness:
                        self.on_ground = True
                        self.rect.bottom = sprite.rect.top

    # Метод обновления
    def update(self, hero):
        self.collide_detect(hero)
        if not self.on_ground:
            self.rect.y += GRAVITY_POWER * 10


# Класс капсул со здоровьем
class HealCapsule(pygame.sprite.Sprite):
    def __init__(self, x, y, size, life_time):
        super(HealCapsule, self).__init__(HEAL_CUPSULES)
        self.image = HEAL_CAPSULE_MINI if size == 1 else HEAL_CAPSULE[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.on_ground = False
        self.life_time = life_time
        self.cost = 5 if size == 1 else 10
        self.size = size
        self.hitbox = None

    # Метод обнаружения столкновений
    def collide_detect(self, hero):
        if pygame.Rect.colliderect(self.hitbox, hero.rect):
            hero.get_hp(self.cost)
            self.kill()
        if not self.on_ground:
            if pygame.sprite.spritecollide(self, PLATFORMS, False):
                for sprite in PLATFORMS:
                    if pygame.Rect.colliderect(self.hitbox, sprite.rect) and sprite.hardness:
                        self.on_ground = True
                        self.rect.bottom = sprite.rect.top
                        if self.size == 1:
                            self.rect.bottom = sprite.rect.top + 16

    # Метод обновления
    def update(self, hero):
        self.update_hitbox()
        self.collide_detect(hero)
        if not self.on_ground:
            self.rect.y += GRAVITY_POWER * 10
        if self.on_ground and self.life_time != -1:
            self.life_time += 1
        if self.life_time >= 200:
            self.kill()

    # Метод обновления хитбоксов
    def update_hitbox(self):
        if self.size == 1:
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 20, 10)
        else:
            self.hitbox = self.rect.copy()


# Класс шипов
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(SPIKES)
        self.image = load('data/Sprites/Окружение/Cut man stage/^.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


# Класс лестниц
class Stair(pygame.sprite.Sprite):
    def __init__(self, x, y, hardness=False):
        super().__init__(STAIRS)
        self.image = load('data/Sprites/Окружение/stair.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hardness = hardness


# Класс камеры
class Camera:
    # Зададим начальный сдвиг камеры
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 1
        self.right = field_size[0]
        self.bottom = field_size[1]
        self.l_limit = 0
        self.r_limit = SIZE[0]
        self.b_limit = SIZE[1]
        self.t_limit = 0
        self.left = 0
        self.top = 0

    # Сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if self.left < 0 and self.right > self.r_limit:
            obj.rect.x += self.dx // 2
            if obj.__class__ in [OctopusBattery, Blaster, BigEye, Mambu]:
                obj.spawn_coords[0] += self.dx // 2
        if self.bottom > self.b_limit:
            obj.rect.y += self.dy // 2
            if obj.__class__ in [OctopusBattery, Blaster, BigEye, Mambu]:
                obj.spawn_coords[1] += self.dy // 2
        return obj.rect.x, obj.rect.y

    # Позиционировать камеру на объекте target
    def update(self, target):
        self.dx = (-target.rect.centerx + SIZE[0] // 2)
        self.dy = (-target.rect.centery + SIZE[1] // 2)
        self.left += self.dx // 2
        if self.left > 0:
            self.left = 0
            self.dx = 0
        self.right += self.dx // 2
        self.bottom += self.dy // 2
        self.top += self.dy // 2
        if self.bottom < self.b_limit:
            self.bottom = self.b_limit
            self.dy = 0
        if self.right < self.r_limit:
            self.right = self.r_limit
        if self.top < 0:
            self.top = 0


# Класс пуль персонажа
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, hero, right=1):
        super().__init__(BULLETS)
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        if right == -1:
            self.rect.x = x - 50
        self.rect.y = y - 3
        self.damage = 4
        if hero.in_jump:
            self.rect.y = y - 30
        elif hero.on_stair:
            self.rect.y = y - 25
        self.speed = 20 * right

    def update(self):
        if self.rect.x > SIZE[0] or self.rect.x < 0:
            self.kill()
        self.rect.x += self.speed


# Класс вражеских пуль
class EnemiesBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dam, direct, speed):
        super().__init__(ENEMY_BULLETS)
        self.image = ENEMY_BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.damage = dam
        self.direction = direct
        self.speed = speed

    def update(self):
        if self.rect.x > SIZE[0] or self.rect.x < 0:
            self.kill()
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]


# Класс Хэлбара
class HealBar:
    def __init__(self, type):
        self.x = self.y = 40
        self.width = 26
        self.height = 237
        self.image = pygame.Surface((self.width, self.height + 4))
        self.hp_count = 0
        self.feature_hp = 0
        self.curent_hp = 0
        if type == 1:
            self.color = (200, 200, 0)
            self.color_1 = (255, 255, 0)
            self.x = self.y = 40
        else:
            self.x = 70
            self.y = 40
            self.color = (180, 0, 0)
            self.color_1 = (255, 0, 0)
        self.type = type

    def update(self, hero, screen):
        if not hero.in_stage:
            if self.type == 1:
                self.feature_hp = self.hp_count = hero.hp
            else:
                self.feature_hp = self.hp_count = 0
        else:
            if self.hp_count < self.feature_hp:
                self.hp_count += 1
                if self.hp_count % 4 == 0:
                    ENERGY_FILL.play(0)
            if self.feature_hp < self.hp_count:
                self.hp_count = self.feature_hp
            if self.curent_hp != self.hp_count:
                self.draw()
                if self.hp_count == self.feature_hp:
                    self.curent_hp = self.hp_count
            self.feature_hp = hero.hp
            screen.blit(self.image, (self.x, self.y))

    def draw(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.width, self.height + 4))
        y = self.height - 2
        x = 0
        width = self.width - 4
        for i in range(self.hp_count):
            pygame.draw.rect(self.image, self.color, (x + 2, y, width, 5))
            pygame.draw.rect(self.image, self.color_1, (int(x + width / 2.5), y, width // 2, 5))
            y -= 6


# Функция, начинающая новую игру
def new_game(level):
    global ALL_SPRITES, BULLETS, MOBS, PLATFORMS, STAIRS, SPIKES, ENEMY_BULLETS, \
        BONUS_BALLS, HEAL_CUPSULES, SCORE, BOSSES
    ALL_SPRITES = Group()
    BULLETS = Group()
    ENEMY_BULLETS = Group()
    MOBS = Group()
    PLATFORMS = Group()
    STAIRS = Group()
    SPIKES = Group()
    BONUS_BALLS = Group()
    HEAL_CUPSULES = Group()
    BOSSES = Group()
    SCORE = 0
    megaman, level_x, level_y, boss = make_level(level)
    up = jump = left = right = down = False
    camera = Camera((level_x, level_y))
    megaman_heal_bar = HealBar(1)
    boss_heal_bar = HealBar(2)
    PAUSE = False
    run = True  # Переменная регулирования игрового цикла

    ready()

    # Игровой цикл
    while run:
        screen.fill((0, 232, 216))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    megaman.shoot()
                if event.key == pygame.K_SPACE:
                    if not PAUSE:
                        PAUSE_S.play(0)
                        CUT_MAN_STAGE.stop()
                    else:
                        CUT_MAN_STAGE.play(-1)
                    PAUSE = not PAUSE
                if event.key == pygame.K_z:
                    jump = True
                if event.key == pygame.K_UP:
                    up = True
                    down = False
                if event.key == pygame.K_RIGHT:
                    right = True
                    left = False
                if event.key == pygame.K_LEFT:
                    left = True
                    right = False
                if event.key == pygame.K_DOWN:
                    down = True
                    up = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    jump = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_DOWN:
                    down = False
        if not PAUSE:
            camera.update(megaman)
            if megaman.in_stage:
                ENEMY_BULLETS.update()
                BULLETS.update()
                MOBS.update(megaman)
                BONUS_BALLS.update(megaman)
                HEAL_CUPSULES.update(megaman)
                BOSSES.update(megaman)
                PLATFORMS.update()
            for sprite in ALL_SPRITES:
                sprite.rect.x, sprite.rect.y = camera.apply(sprite)
                if (0 < sprite.rect.left < SIZE[0] or 0 < sprite.rect.top < SIZE[1]) \
                        or (0 < sprite.rect.right < SIZE[0] or 0 < sprite.rect.bottom < SIZE[1]):
                    if sprite.__class__ in [BigEye, CutMan, Player]:
                        rect = sprite.image.get_rect()
                        rect.bottom = sprite.rect.bottom
                        rect.centerx = sprite.rect.centerx
                        screen.blit(sprite.image, rect)
                    else:
                        screen.blit(sprite.image, sprite.rect)
            megaman_heal_bar.update(megaman, screen)
            boss_heal_bar.update(boss, screen)
            if megaman.hp > 0:
                megaman.update(jump, up, left, right, down)
            else:
                if not megaman.death_music:
                    megaman.death_music = True
                    megaman.death_coords = [list(megaman.rect.center) for i in range(8)]
                    MEGAMAN_DEATH_S.play(0)
                    CUT_MAN_STAGE.stop()
                    BOSS_BATTLE.stop()
                if megaman.death_count < 150:
                    frame = megaman.death_count % 40 // 10
                    elem = MEGAMAN_DEATH[frame]
                    for i in range(len(megaman.death_coords)):
                        screen.blit(elem, megaman.death_coords[i])
                        megaman.death_coords[i][0] += megaman.death_coeff[i][0]
                        megaman.death_coords[i][1] += megaman.death_coeff[i][1]
                    megaman.image = pygame.Surface((62, 60), pygame.SRCALPHA)
                if megaman.death_count > 300:
                    megaman.is_dead = True
                    return 'game over'
                if not megaman.is_dead:
                    megaman.death_count += 1
            if boss.hp == 0:
                if boss.death_count < 150:
                    frame = boss.death_count % 40 // 10
                    elem = ENEMIES_DESTROY[frame]
                    for i in range(len(boss.death_coords)):
                        screen.blit(elem, boss.death_coords[i])
                        boss.death_coords[i][0] += boss.death_coeff[i][0]
                        boss.death_coords[i][1] += boss.death_coeff[i][1]
                boss.death_count += 1
            if len(BOSSES) == 0:
                return 'victory'
        else:
            ALL_SPRITES.draw(screen)
            megaman.in_stage = False
        print_score()
        pygame.display.flip()
        clock.tick(FPS)
    quit_sys()


pygame.init()  # Инициализируем pygame

flags = pygame.DOUBLEBUF  # <-- В интернете говорят, что это увеличит производительность
# Создаём окно с заданным размером
screen = pygame.display.set_mode(SIZE, flags=flags)
screen.set_alpha(None)  # Убираем альфа-канал у главного окна
# Даём программе имя
pygame.display.set_caption('Megaman')
clock = pygame.time.Clock()  # Счётчик кадров в секунду
level = []

start_screen()

# Главный цикл
while True:
    if not level:
        level = Levels[stage_select()]
    result = new_game(level)
    if result == 'game over':
        res = continue_menu()
        if not res:
            level = []
    if result == 'victory':
        res = victory_screen()
        if not res:
            level = []
        else:
            quit_sys()
