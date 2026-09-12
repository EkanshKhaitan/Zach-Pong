import pygame
import time
import random

# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()

# GAME VARIABLES
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zach Pong")
clock = pygame.time.Clock()
running = True
dt = 0

random_posy = 0
random_posx = 0
random_pos = 0

level = 1
vx = 400
vy = 400
random_posx = random.randint(0 , WIDTH)
random_posy = random.randint(0, HEIGHT)
random_pos = pygame.Vector2(random_posx , random_posy)

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
paddle_height = 200
left_paddle = pygame.Rect(WIDTH // 5 , HEIGHT // 2, 20 , paddle_height)
playagain_rect_x = 900
playagain_rect_y = 400

score = 0
totalscore = 0

blit_scoremult = False
scorelvl = 1
last_frame_score = False

# IMAGES

zach = pygame.image.load('zach.png').convert_alpha()
zach = pygame.transform.smoothscale(zach, (200, 200))

play_again = pygame.image.load('playagain.png').convert_alpha()

scoremult = pygame.image.load('2xscore.png').convert_alpha()
scoremult = pygame.transform.smoothscale(scoremult, (100, 100))

backgroundColor = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

# SOUNDS

womp = pygame.mixer.Sound('wompwomp.mp3')
bone = pygame.mixer.Sound('bone.mp3')
coin = pygame.mixer.Sound('coin.mp3')
click = pygame.mixer.Sound('mouseclick.mp3')
levelup = pygame.mixer.Sound('levelup.mp3')
levelup.set_volume(0.2)
pygame.mixer.music.load('chillmusic.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.33)
# FONTS

font = pygame.font.Font('pirkkala.ttf', 50)
big_font = pygame.font.Font('Minecraft-Seven_v2.woff2', 200)

realvol = pygame.mixer.music.get_volume()

while running:
    realvol = 1 if realvol > 1 else realvol
    pygame.mixer.music.set_volume(realvol)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_rect = pygame.Rect((pygame.mouse.get_pos()), (1, 1))
    ball_rect = pygame.Rect(ball_pos.x - 40, ball_pos.y - 40, 80, 80)
    scoremult_rect = pygame.Rect(random_posx, random_posy, 100, 100)

    if score >= 5:
        levelup.play()
        level += 1
        score -= 5
        vx += 100
        vy += 100
        paddle_height *= 0.9 
        random_posx = random.randint(0 , WIDTH)
        random_posy = random.randint(0, HEIGHT)
        random_pos = pygame.Vector2(random_posx , random_posy)
        backgroundColor = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        scorelvl = 1
        if random.randint(1, 3) == 1:
            blit_scoremult = True

    if mouse_rect.colliderect(scoremult_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            blit_scoremult = False
            scorelvl = 2
            click.play()


    screen.fill(backgroundColor)

    level_text_surface = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text_surface, (1000, 50))


    # if event.type == pygame.MOUSEBUTTONDOWN:
        # print(pygame.mouse.get_pos())

    pygame.draw.circle(screen, "red", ball_pos, 40)
    left_paddle.h = paddle_height
    pygame.draw.rect(screen , "grey" , left_paddle)


    score_text_surface = font.render(f"Score: {totalscore}", True, (0, 0, 0))
    screen.blit(score_text_surface, (50, 50))

    if blit_scoremult == True:
        screen.blit(scoremult, random_pos)

    if 50 < ball_pos.x < 100:
        womp.play()
    if ball_pos.x > WIDTH - 40:
        vx *= -1
        bone.play()
    if ball_pos.y < 100:
        vy *= -1
        bone.play()
        vy += random.randint(-5,5)
    if ball_pos.y > HEIGHT - 70:
        vy *= -1
        bone.play()
        vy += random.randint(-5,5)

    if ball_rect.colliderect(left_paddle) and not last_frame_score:
        vx *= -1
        coin.play()
        score += scorelvl
        totalscore += scorelvl
        last_frame_score = True
        vy += random.randint(-5,5)
    
    if not ball_rect.colliderect(left_paddle):
        last_frame_score = False

    if ball_pos.x <= 50:
        # LOSING
        realvol = realvol+(0.05*dt)
        print(realvol)
        vx = 0
        vy = 0
        blit_zach = False
        screen.fill("black")
        lose_text_surface = big_font.render('Y  U LOST', True, (255, 0, 0))
        screen.blit(lose_text_surface, (WIDTH / 5, HEIGHT / 5))
        screen.blit(zach, (430 - 100, 215 - 100))
        score_text_surface = font.render(f"Score: {totalscore}", True, (255, 0, 0))
        screen.blit(score_text_surface, (WIDTH/3, HEIGHT / 2))
        loselevel_text_surface = font.render(f"Level: {level}", True, (255, 0, 0))
        screen.blit(loselevel_text_surface, (WIDTH / 3, HEIGHT / 1.5))

        # PLAY AGAIN

        playagain_rect = pygame.Rect(playagain_rect_x, playagain_rect_y, 350, 150)
        screen.blit(pygame.transform.smoothscale(play_again, playagain_rect.size), playagain_rect.topleft)

        if mouse_rect.colliderect(playagain_rect):
            if event.type == pygame.MOUSEBUTTONDOWN:
                realvol = 0.33
                level = 1
                vx = 400
                vy = 400
                click.play()

                ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                paddle_height = 200
                left_paddle = pygame.Rect(WIDTH // 5 , HEIGHT // 2, 20 , paddle_height)
                playagain_rect_x = 900
                playagain_rect_y = 400
                scorelvl = 1
                score = 0
                totalscore = 0

                last_frame_score = False
                
    else:
        blit_zach = True
        
    if blit_zach == True:
        screen.blit(zach, (ball_pos.x -100 , ball_pos.y - 100))

    ball_pos.y += vy * dt
    ball_pos.x += vx * dt

    if left_paddle.y < 0:
        left_paddle.y = 0
    if left_paddle.y > HEIGHT - paddle_height:
        left_paddle.y = HEIGHT - paddle_height

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.y -= 300 * dt
    if keys[pygame.K_s]:
        left_paddle.y += 300 * dt

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()
