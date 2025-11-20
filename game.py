import pygame, sys, random
from database import load_or_create_player, update_player_score, get_highest_score

# ------------------------- HÀM CHUNG -------------------------
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return [pipe for pipe in pipes if pipe.right > -50]

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True

def rotate_bird(bird1):
    return pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    # Hiển thị điểm người chơi
    score_surface = game_font.render(f'{player_name}: {int(score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(216, 100))
    screen.blit(score_surface, score_rect)

    # Hiển thị điểm cao nhất tất cả người chơi góc trái
    top_score = get_highest_score()
    top_surface = game_font.render(f'Top: {top_score}', True, (255, 200, 0))
    screen.blit(top_surface, (10, 10))

    if game_state != 'main game':
        # Hiển thị best cá nhân
        high_surface = game_font.render(f'Best: {high_score}', True, (255, 255, 255))
        high_rect = high_surface.get_rect(center=(216, 630))
        screen.blit(high_surface, high_rect)

def update_high_score(current, record):
    return current if current > record else record

# ------------------------- INIT PYGAME -------------------------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 35)

# ------------------------- PLAYER NAME INPUT -------------------------
player_name = ""
input_active = True
font = pygame.font.Font('04B_19.ttf', 40)
input_rect = pygame.Rect(66, 350, 300, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False

while input_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = input_rect.collidepoint(event.pos)
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_RETURN:
                player_name = player_name.strip() or "Player"
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 12:
                    player_name += event.unicode

    screen.fill((0, 0, 0))
    txt_surface = font.render(player_name, True, (255, 255, 255))
    input_rect.w = max(300, txt_surface.get_width() + 10)
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(screen, color, input_rect, 2)
    info_surface = game_font.render("Enter your name:", True, (255,255,255))
    info_rect = info_surface.get_rect(center=(216, 300))
    screen.blit(info_surface, info_rect)
    pygame.display.flip()
    clock.tick(30)

player_data = load_or_create_player(player_name)
high_score = player_data.get("best_score", 0)

# ------------------------- GAME VARIABLES -------------------------
gravity = 0.4
bird_movement = 0
game_active = True
score = 0
passed_pipes = []

bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
floor = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())
floor_x_pos = 0

bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
pipe_list = []
pipe_height = [250, 300, 350, 400]
pipe_gap = 180

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# ------------------------- GAME LOOP -------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                passed_pipes.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        for pipe in pipe_list:
            if pipe.centerx < 100 and pipe not in passed_pipes and pipe.bottom >= 600:
                score += 1
                passed_pipes.append(pipe)
                score_sound.play()

        score_display('main game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_player_score(player_name, score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
