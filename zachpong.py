import pygame
import time

# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zach Pong")
clock = pygame.time.Clock()
running = True
dt = 0

vx = 300
vy = 300

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
left_paddle = pygame.Rect(WIDTH // 5 , HEIGHT // 2, 20 , 200)

zach = pygame.image.load('zach.png').convert_alpha()
zach = pygame.transform.smoothscale(zach, (200, 200))

bone = pygame.mixer.Sound('bone.mp3')
coin = pygame.mixer.Sound('coin.mp3')
score = 0
font = pygame.font.Font('Minecraft-Seven_v2.woff2', 50)
big_font = pygame.font.Font('Minecraft-Seven_v2.woff2', 200)

last_frame_score = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", ball_pos, 40)
    pygame.draw.rect(screen , "grey" , left_paddle)

    ball_rect = pygame.Rect(ball_pos.x - 40, ball_pos.y - 40, 80, 80)


    score_text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text_surface, (50, 50))

    if ball_pos.x < 100:
        vx *= -1
        bone.play()
    if ball_pos.x > WIDTH - 40:
        vx *= -1
        bone.play()
    if ball_pos.y < 100:
        vy *= -1
        bone.play()
    if ball_pos.y > HEIGHT - 70:
        vy *= -1
        bone.play()

    if ball_rect.colliderect(left_paddle) and not last_frame_score:
        vx *= -1
        coin.play()
        score += 1
        last_frame_score = True
    
    if not ball_rect.colliderect(left_paddle):
        last_frame_score = False

    if ball_pos.x <= 200:
        vx = 0
        vy = 0
        screen.fill("black")
        lose_text_surface = big_font.render('Y  U LOST', True, (255, 0, 0))
        screen.blit(lose_text_surface, (WIDTH / 5, HEIGHT / 5))
        screen.blit(zach, (430 - 100, 215 - 100))
        score_text_surface = font.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_text_surface, (WIDTH/3, HEIGHT / 2))
    else:
        screen.blit(zach, (ball_pos.x -100 , ball_pos.y - 100))

    ball_pos.y += vy * dt
    ball_pos.x += vx * dt

    if left_paddle.y < 0:
        left_paddle.y = 0
    if left_paddle.y > HEIGHT - 200:
        left_paddle.y = HEIGHT - 200

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.y -= 300 * dt
    if keys[pygame.K_s]:
        left_paddle.y += 300 * dt



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
