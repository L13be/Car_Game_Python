import pygame
import pygame_menu
import random
import pygame.mixer

from pygame import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_y, K_n, K_p, K_ESCAPE, K_t

pygame.init()

main_music = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\меню.mp3')
main_music.set_volume(0.08)
click = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\нажатие-кнопок.mp3')
click.set_volume(0.5)
gameor_sound = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\gameover.mp3')
gameor_sound.set_volume(0.2)

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
beige = (245, 245, 220)
black = (0, 0, 0)

road_width = 300
marker_width = 10
marker_height = 50

left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

lane_marker_move_y = 0

player_x = 250
player_y = 400

clock = pygame.time.Clock()
fps = 120

gameover = False
speed = 2
score = 0

playing = False
paused = False

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)


player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

player = PlayerVehicle(player_x, player_y)
player_group.add(player)

image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

def start_game():
    global playing
    playing = True
    menu.disable()
    click.play()
    main_music.stop()
    print('Game started!')

def quit_game():
    global playing, running
    click.play()
    playing = False
    running = False
    menu.disable()
    print('Game quit!')

def pause_game():
    global paused
    paused = not paused
    if paused:
        print('Game paused!')
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                        print('Game resumed!')


            pygame.draw.rect(screen, black, (width / 2 - 100, height / 2 - 50, 200, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text = font.render('Пауза игры', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, height / 2)
            screen.blit(text, text_rect)

            pygame.display.update()
            clock.tick(fps)
    else:
        print('Game resumed!')

def save_score(score):
    with open('scores.txt', 'a') as file:
        file.write(str(score) + '\n')


def get_top_scores():
    scores = []
    with open('scores.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            scores.append(int(line.strip()))

    # Сортировка по убыванию и выбор трех лучших
    top_scores = sorted(scores, reverse=True)[:3]
    return top_scores

def show_top_scores():
    top_scores = get_top_scores()
    click.play()
    running = True
    while running:
        screen.fill(beige)


        font = pygame.font.Font(None, 36)
        text_y = height // 2 - 100  # Центрирование таблицы по вертикали
        title_text = font.render("TOP Score   Result", True, black)
        title_rect = title_text.get_rect(center=(width // 2, text_y))
        screen.blit(title_text, title_rect)
        text_y += 40

        for index, score in enumerate(top_scores):
            text = font.render(f"   [{index + 1}]           {score}", True, black)
            text_rect = text.get_rect(center=(width // 2, text_y))
            screen.blit(text, text_rect)
            text_y += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False


running = True
def show_game_over_menu():
    global running, gameover, menu, playing, score, speed, vehicle_group, player
    gameover = True
    gameor_sound.play()
    menu = pygame_menu.Menu('Game Over', 500, 500, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.enable()

    def start_game_over():
        global gameover, score, speed
        click.play()
        gameover = False
        score = 0
        speed = 2
        vehicle_group.empty()
        player.rect.center = [player_x, player_y]

    def back_to_main_menu():
        global gameover, running, menu, playing, score, speed, vehicle_group, player
        click.play()
        gameover = False
        menu = create_main_menu()
        playing = False
        score = 0
        speed = 2
        vehicle_group.empty()
        player.rect.center = [player_x, player_y]


    menu.add.button('Начать заново', start_game_over)
    menu.add.button('Вернуться в меню', back_to_main_menu)

    while gameover:

        menu.update(pygame.event.get())
        menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selected = menu.get_selected_widget()
                    print(f"Выбрана кнопка: {selected.get_title()}")
                    if selected.get_title() == 'Начать заново':
                        start_game_over()
                        gameover = False
                    elif selected.get_title() == 'Вернуться в меню':
                        back_to_main_menu()
                        gameover = False


        pygame.display.update()
        clock.tick(fps)

    return running

# CARS OPENED

car_descriptions = {
    'car.png': 'Основная машина',
    'lambo.png': 'Lamborghini',
    'greeny.png': 'Greeny Car',
    'bmw.png': 'BMW Car'
}

unlocked_cars = ['car.png']

def check_unlocked_cars(score):
    if score >= 5 and 'lambo.png' not in unlocked_cars:
        unlocked_cars.append('lambo.png')
        print('Lambo разблокирована!')

    if score >= 10 and 'greeny.png' not in unlocked_cars:
        unlocked_cars.append('greeny.png')
        print('Greeny разблокирован!')

    if score >= 20 and 'bmw.png' not in unlocked_cars:
        unlocked_cars.append('bmw.png')
        print('BMW разблокирован!')

def change_player_car():
    global current_player_car
    print('Доступные машины:', unlocked_cars)

    menu.clear()

    menu.add.button('Назад', menu_previous)
    click.play()

    for index, car in enumerate(unlocked_cars):
        menu.add.button(car_descriptions[car], select_car, car)

    print('Меню с доступными машинами')


def select_car(selected_car):
    click.play()
    global current_player_car
    current_player_car = selected_car
    update_player_car(selected_car)
    print('Машинка изменена!')


def menu_previous():
    click.play()
    menu.clear()
    menu.add.button('Начать', start_game)
    menu.add.button('Топ-3 результата', show_top_scores)
    menu.add.button('Изменить машинку', change_player_car)
    menu.add.button('Выход', quit_game)

def update_player_car(selected_car):
    global player, player_group
    image = pygame.image.load('images/' + selected_car)
    player = PlayerVehicle(player.rect.center[0], player.rect.center[1])
    player.image = pygame.transform.scale(image, (player.rect.width, player.rect.height))
    player_group.empty()
    player_group.add(player)


# ALL FUNCTION ARE UP
def create_main_menu():
    global menu
    menu = pygame_menu.Menu('Car Racing', 500, 500, theme=pygame_menu.themes.THEME_SOLARIZED)
    main_music.play()
    menu.add.button('Начать', start_game)
    menu.add.button('Топ-3 результата', show_top_scores)
    menu.add.button('Изменить машинку', change_player_car)
    menu.add.button('Выход', quit_game)
    return menu


create_main_menu()


# game loop
running = True
paused = False
playing = False
gameover = False
while running:

    clock.tick(fps)

    if playing:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:

                if event.key == K_LEFT and player.rect.center[0] > left_lane:
                    player.rect.x -= 100
                elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                    player.rect.x += 100

                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):

                        gameover = True

                        if event.key == K_LEFT:
                            player.rect.left = vehicle.rect.right
                            crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        elif event.key == K_RIGHT:
                            player.rect.right = vehicle.rect.left
                            crash_rect.center = [player.rect.right,
                                                 (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    if event.key == K_p:
                        pause_game()

        screen.fill(green)

        pygame.draw.rect(screen, gray, road)

        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)

        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

        player_group.draw(screen)

        if len(vehicle_group) < 2:

            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False

            if add_vehicle:

                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)

        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            if vehicle.rect.top >= height:
                vehicle.kill()

                score += 1
                check_unlocked_cars(score)

                # speed up the game after passing 10 vehicles
                if score > 0 and score % 10 == 0:
                    speed += 1

        vehicle_group.draw(screen)

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Score: ' + str(score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 400)
        screen.blit(text, text_rect)

        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

        pygame.display.update()

        while gameover:

            clock.tick(fps)
            save_score(score)
            show_game_over_menu()

    else:
        menu.mainloop(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause_game()
                elif event.key == K_t:
                    show_top_scores()

pygame.quit()

