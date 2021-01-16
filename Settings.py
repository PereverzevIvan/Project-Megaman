from pygame.image import load
from pygame import USEREVENT
from pygame.sprite import Group
from pygame.time import set_timer
from pygame import transform
from pygame import mixer

mixer.pre_init(44100, -16, 3, 512)
mixer.init()

# Параметры экрана
SIZE = [1200, 720]
FPS = 65
GRAVITY_POWER = 1.5
SCORE = 0

# Таймеры
BLINKING_RECT = USEREVENT + 1
set_timer(BLINKING_RECT, 10 * 80)

# Параметры спрайтов
ALL_SPRITES = Group()  # Все спрайты
BULLETS = Group()  # Спрайты пуль
ENEMY_BULLETS = Group()  # Спрайты вражеских пуль
MOBS = Group()  # Спрайты мобов
PLATFORMS = Group()  # Спрайты плаформ
STAIRS = Group()  # Спрайты лестниц
SPIKES = Group()  # Спрайты шипов
BONUS_BALLS = Group()  # Спрайты бонусных шаров
HEAL_CUPSULES = Group()  # Спрайты банок со здоровьем
BOSSES = Group()  # Спрайты боссов

# Пареметры и спрайты игрока
JUMP_POWER = 4
MEGAMAN_STAND = [load(f'data/Sprites/Megaman sprites/{i}.png') for i in ['standing', 'blink']]
MEGAMAN_WALK = [load(f'data/Sprites/Megaman sprites/walk {i}.png') for i in [2, 3, 2, 4]]
MEGAMAN_JUMP = load('data/Sprites/Megaman sprites/jump.png')
MEGAMAN_ON_STAIR = [load(f'data/Sprites/Megaman sprites/on stairs {i}.png') for i in [1, 2]]
MEGAMAN_GET_DOWN_STAIR = load('data/Sprites/Megaman sprites/get down stairs.png')
MEGAMAN_SHOOT = load('data/Sprites/Megaman sprites/shot.png')
BULLET_IMAGE = transform.scale(load('data/Sprites/Megaman sprites/bullet.png'), (15, 15))
MEGAMAN_TELEPORT_1 = load('data/Sprites/Megaman sprites/teleport 1.png')
MEGAMAN_WALK_AND_SHOT = [load(f'data/Sprites/Megaman sprites/walk and shot {i}.png') for i in [1, 2, 3, 2]]
MEGAMAN_JUMP_AND_SHOT = load('data/Sprites/Megaman sprites/jump and shot.png')
MEGAMAN_SHOT_ON_STAIR = load('data/Sprites/Megaman sprites/shot on stair.png')
MEGAMAN_GET_DAMAGE = [load(f'data/Sprites/Megaman sprites/get damage {i}.png') for i in [1, 2]]
MEGAMAN_STAND_HIS_BACK = load('data/Sprites/Megaman sprites/stands with his back.png')
MEGAMAN_DEATH = [load(f'data/Sprites/Megaman sprites/Death {i}.png') for i in [1, 2, 3, 4]]
MEGAMAN_HELMET = load('data/Sprites/megaman helmet.png')

# Дополнительные спрайты
MENU_CURSOR = transform.scale(load('data/Sprites/menu curcor.png'), (20, 20))
BONUS_BALL = transform.scale(load('data/Sprites/bonus ball.png'), (20, 20))
MEGA_BALL = load('data/Sprites/mega ball.png')
HEAL_CAPSULE_MINI = load('data/Sprites/heal capsule mini.png')
HEAL_CAPSULE = [load(f'data/Sprites/heal capsule {i}.png') for i in [1, 2]]
STAGE_SELECT_SCREEN = [load(f'data/Sprites/Stage select/stage select {i}.png') for i in [1, 2, 3, 4, 5, 6, 7]]
BOSS_GATE_IMAGE = load('data/Sprites/Окружение/N.png')
FONT = {
    'C': load('data/Sprites/Font/C.png'),
    'U': load('data/Sprites/Font/U.png'),
    'T': load('data/Sprites/Font/T.png'),
    'M': load('data/Sprites/Font/M.png'),
    'A': load('data/Sprites/Font/A.png'),
    'N': load('data/Sprites/Font/N.png'),

}

# Спрайты врагов
BLADER = [load(f'data/Sprites/Mobs/blader {i}.png') for i in [1, 2]]
SNIPER_JOE = [load(f'data/Sprites/Mobs/sniper joe {i}.png') for i in [1, 2, 3]] + \
             [load('data/Sprites/Mobs/sniper joe jump.png')]
BLASTER = [load(f'data/Sprites/Mobs/sucker gun {i}.png') for i in [1, 2, 3, 4]]
MAMBU = [load(f'data/Sprites/Mobs/armored ball {i}.png') for i in [1, 2]]
BIG_EYE = [load(f'data/Sprites/Mobs/big eye jump-bot {i}.png') for i in [1, 2]]
OCTOPUS_BATTERY = [load(f'data/Sprites/Mobs/eye-sucker {i}.png') for i in [1, 2, 3]]
FLEA = [load(f'data/Sprites/Mobs/eye-sucker {i}.png') for i in [1, 2]]
ENEMIES_DESTROY = [load(f'data/Sprites/Mobs/destroyed {i}.png') for i in [1, 2, 3, 4]]
ENEMY_BULLET_IMAGE = load('data/Sprites/Mobs/bullet.png')

# Спрайты боссов
CUT_MAN_IDLE_W = [load(f'data/Sprites/Bosses/CutMan/idle {i}.png') for i in [1, 2]]
CUT_MAN_WALK_W = [load(f'data/Sprites/Bosses/CutMan/walk {i}.png') for i in [1, 2, 3]]
CUT_MAN_JUMP_W = load('data/Sprites/Bosses/CutMan/jump.png')
CUT_MAN_WALK = [load(f'data/Sprites/Bosses/CutMan/walk {i} n.png') for i in [1, 2, 3]]
CUT_MAN_JUMP = load('data/Sprites/Bosses/CutMan/jump n.png')
CUT_MAN_TOSS = [load(f'data/Sprites/Bosses/CutMan/cutter toss {i}.png') for i in [1, 2]]
CUT_MAN_IDLE = load('data/Sprites/Bosses/CutMan/idle 1 n.png')
ROLLING_CUTTER_IMAGE = [load(f'data/Sprites/Bosses/CutMan/rolling cutter {i}.png') for i in [0, 1, 2, 3]]


# Звуковые эффекты
MENU_SELECT = mixer.Sound('data/Sounds/03 - MenuSelect.ogg')  # Выбор в меню
MEGAMAN_DEATH_S = mixer.Sound('data/Sounds/08_-_MegamanDefeat.ogg')  # Смерть Мегамена
MEGAMAN_GET_DAMAGE_S = mixer.Sound('data/Sounds/07_-_MegamanDamage.ogg')  # Получение урона Мегаменом
STAGE_CHOSEN = mixer.Sound('data/Sounds/02_Enemy_Chosen.ogg')  # Звук после выбора уровня
GAME_START = mixer.Sound('data/Sounds/01 - GameStart.ogg')
MEGA_BUSTER = mixer.Sound('data/Sounds/05_-_MegaBuster.ogg')  # Звук стрельбы
MEGAMAN_LAND = mixer.Sound('data/Sounds/06_-_MegamanLand.ogg')  # Звук приземления
EMPTY_SHOT = mixer.Sound('data/Sounds/11_-_Dink.ogg')  # Звук пустого выстрела
PAUSE_S = mixer.Sound('data/Sounds/02 - PauseMenu.ogg')  # Звук паузы
ENEMY_SHOOT_S = mixer.Sound('data/Sounds/10_-_EnemyShoot.ogg')  # Звук вражеского выстрела
ENEMY_DAMAGE_S = mixer.Sound('data/Sounds/09_-_EnemyDamage.ogg')  # Звук получения урона врагом
BONUS_BALL_S = mixer.Sound('data/Sounds/26_-_BonusBall.ogg')  # Звук подбора бонусного шара
ENERGY_FILL = mixer.Sound('data/Sounds/24_-_EnergyFill.ogg')  # Звук заполнения хэлбара
BIG_EYE_S = mixer.Sound('data/Sounds/12_-_BigEye.ogg')  # Звук большого глаза
ROLLING_CUTTER_S = mixer.Sound('data/Sounds/18_-_RollingCutter.ogg')  # Звук ножниц-бумеранга
BOSS_GATE_S = mixer.Sound('data/Sounds/30-BossGate.ogg')  # Звук врат, ведущих к боссу
POINT_TALLY = mixer.Sound('data/Sounds/34-PiPiPi.ogg')  # Звук подсчёта очков
VICTORY = mixer.Sound('data/Sounds/10_Victory_.ogg')  # Звук победного экрана


# Музыка
CUT_MAN_STAGE = mixer.Sound('data/Sounds/07_Cut_Man.ogg')  # Музыка уровня Катмена
STAGE_SELECT = mixer.Sound('data/Sounds/01_Stage_Select.ogg')  # Музыка при выборе уровня
GAME_OVER = mixer.Sound('data/Sounds/11_-_game_over.ogg')  # Музыка экрана смерти [не синего :-)]
BOSS_BATTLE = mixer.Sound('data/Sounds/09_Boss-Battle.ogg')  # Музыка при битве с боссом
