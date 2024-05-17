import pygame
import time
import random
import sys

# Inicializa o Pygame
pygame.init()

# Definindo as cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Definindo o tamanho da tela
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Rodrigo')

clock = pygame.time.Clock()

snake_block = 10
initial_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
small_score_font = pygame.font.SysFont("bahnschrift", 20)  # Fonte menor para a pontuação

top_scores = []

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
    dis.blit(mesg, mesg_rect)

def your_score(score):
    value = small_score_font.render("Your Score: " + str(score), True, black)
    value_rect = value.get_rect(center=(dis_width / 2, 20))  # Centralizado no topo
    dis.blit(value, value_rect)

def get_player_name():
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        dis.fill(white)
        message("Enter your name: " + name, black)
        pygame.display.update()

def show_game_over_screen(score):
    global top_scores
    name = get_player_name()
    top_scores.append((score, name))
    top_scores = sorted(top_scores, key=lambda x: x[0], reverse=True)[:3]

    while True:
        dis.fill(white)
        message("Game Over", red, -50)
        message(f"Final Score: {score}", black, 0)
        message("Top Scores:", black, 50)
        for i, (score, name) in enumerate(top_scores):
            message(f"{i+1}. {name} - {score}", black, 100 + 30 * i)
        message("Press Q-Quit or C-Play Again", red, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    gameLoop()

def gameLoop():  # criando uma função para o jogo principal
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            show_game_over_screen(Length_of_snake - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(initial_speed + Length_of_snake // 5)

    pygame.quit()
    sys.exit()

gameLoop()
