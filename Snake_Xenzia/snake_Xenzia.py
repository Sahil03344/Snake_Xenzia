import pygame
import sys
import random

# Initialize pygame
pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snake Xenzia')
background = pygame.image.load('Snake_Xenzia\\background.jpg')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load all images
apple_img = pygame.image.load("Snake_Xenzia\\Graphics\\apple.png")

head_imgs = {
    (0, -1): pygame.image.load("Snake_Xenzia\\Graphics\\head_up.png"),
    (0, 1): pygame.image.load("Snake_Xenzia\\Graphics\\head_down.png"),
    (-1, 0): pygame.image.load("Snake_Xenzia\\Graphics\\head_left.png"),
    (1, 0): pygame.image.load("Snake_Xenzia\\Graphics\\head_right.png"),
}

tail_imgs = {
    (0, -1): pygame.image.load("Snake_Xenzia\\Graphics\\tail_up.png"),
    (0, 1): pygame.image.load("Snake_Xenzia\\Graphics\\tail_down.png"),
    (-1, 0): pygame.image.load("Snake_Xenzia\\Graphics\\tail_left.png"),
    (1, 0): pygame.image.load("Snake_Xenzia\\Graphics\\tail_right.png"),
}

body_imgs = {
    "horizontal": pygame.image.load("Snake_Xenzia\\Graphics\\body_horizontal.png"),
    "vertical": pygame.image.load("Snake_Xenzia\\Graphics\\body_vertical.png"),
    "tl": pygame.image.load("Snake_Xenzia\\Graphics\\body_tl.png"),
    "tr": pygame.image.load("Snake_Xenzia\\Graphics\\body_tr.png"),
    "bl": pygame.image.load("Snake_Xenzia\\Graphics\\body_bl.png"),
    "br": pygame.image.load("Snake_Xenzia\\Graphics\\body_br.png"),
}

# Snake and fruit initialization
snake = [(5, 10), (4, 10), (3, 10)]
direction = (1, 0)

# FIX: fruit not on snake
while True:
    fruit = (random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
    if fruit not in snake:
        break

# Load high score
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# NEW: pause variable
paused = False

# Helper functions
def get_direction(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])

def draw_snake():
    for i, block in enumerate(snake):
        x, y = block[0] * cell_size, block[1] * cell_size
        if i == 0:
            dir_head = get_direction(snake[0], snake[1])
            screen.blit(head_imgs[dir_head], (x, y))
        elif i == len(snake) - 1:
            dir_tail = get_direction(snake[-1], snake[-2])
            screen.blit(tail_imgs[dir_tail], (x, y))
        else:
            prev = snake[i - 1]
            next = snake[i + 1]
            dir_prev = get_direction(prev, block)
            dir_next = get_direction(next, block)

            if dir_prev[0] == dir_next[0]:
                screen.blit(body_imgs["vertical"], (x, y))
            elif dir_prev[1] == dir_next[1]:
                screen.blit(body_imgs["horizontal"], (x, y))
            else:
                if (dir_prev == (-1, 0) and dir_next == (0, -1)) or (dir_prev == (0, -1) and dir_next == (-1, 0)):
                    screen.blit(body_imgs["tl"], (x, y))
                elif (dir_prev == (1, 0) and dir_next == (0, -1)) or (dir_prev == (0, -1) and dir_next == (1, 0)):
                    screen.blit(body_imgs["tr"], (x, y))
                elif (dir_prev == (-1, 0) and dir_next == (0, 1)) or (dir_prev == (0, 1) and dir_next == (-1, 0)):
                    screen.blit(body_imgs["bl"], (x, y))
                elif (dir_prev == (1, 0) and dir_next == (0, 1)) or (dir_prev == (0, 1) and dir_next == (1, 0)):
                    screen.blit(body_imgs["br"], (x, y))

game_over = False

def draw_game_over():
    text = font.render('Game Over! Press Enter To Restart The Game', True, 'Black')
    text_rect = text.get_rect(center=((cell_number * cell_size) / 2, (cell_number * cell_size) / 2))
    screen.blit(text, text_rect)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

            # NEW: pause toggle
            if event.key == pygame.K_p:
                paused = not paused

            if game_over and event.key == pygame.K_RETURN:
                with open("high_score.txt", "w") as f:
                    f.write(str(high_score))
                snake = [(5, 10), (4, 10), (3, 10)]
                direction = (1, 0)
                while True:
                    fruit = (random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
                    if fruit not in snake:
                        break
                game_over = False

    # UPDATED: pause check added
    if not game_over and not paused:
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        if new_head == fruit:
            while True:
                fruit = (random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
                if fruit not in snake:
                    break
            if len(snake) - 3 > high_score:
                high_score = len(snake) - 3
                # NEW: save immediately
                with open("high_score.txt", "w") as f:
                    f.write(str(high_score))
        else:
            snake.pop()

        if (
            new_head in snake[1:] or
            not 0 <= new_head[0] < cell_number or
            not 0 <= new_head[1] < cell_number
        ):
            game_over = True

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(apple_img, (fruit[0] * cell_size, fruit[1] * cell_size))
    draw_snake()

    # Score display
    score = len(snake) - 3
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    pause_text = font.render("Press P to Pause", True, (0, 0, 0))

    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(pause_text, (10, 70))

    # NEW: paused screen
    if paused:
        text = font.render("Paused - Press P to Resume", True, (0, 0, 0))
        text_rect = text.get_rect(center=((cell_number * cell_size)//2, (cell_number * cell_size)//2))
        screen.blit(text, text_rect)

    if game_over:
        draw_game_over()

    pygame.display.update()

    # UPDATED: dynamic speed
    clock.tick(5 + (len(snake) // 5))
 