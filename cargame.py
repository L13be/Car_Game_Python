import pygame
import pygame_menu
import random
import pygame.mixer

from pygame import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_y, K_n, K_p, K_ESCAPE, K_t

class CarGame:
    def __init__(self):
        pygame.init()

        self.main_music = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\меню.mp3')
        self.main_music.set_volume(0.08)
        self.click = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\нажатие-кнопок.mp3')
        self.click.set_volume(0.5)
        self.gameor_sound = pygame.mixer.Sound('E:\Учёба\Питон практики\CarGame\gameover.mp3')
        self.gameor_sound.set_volume(0.2)

        self.width = 500
        self.height = 500
        self.screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Car Game')


        self.gray = (100, 100, 100)
        self.green = (76, 208, 56)
        self.red = (200, 0, 0)
        self.white = (255, 255, 255)
        self.yellow = (255, 232, 0)
        self.beige = (245, 245, 220)
        self.black = (0, 0, 0)

        self.road_width = 300
        self.marker_width = 10
        self.marker_height = 50

        self.left_lane = 150
        self.center_lane = 250
        self.right_lane = 350
        self.lanes = [self.left_lane, self.center_lane, self.right_lane]

        self.road = (100, 0, self.road_width, self.height)
        self.left_edge_marker = (95, 0, self.marker_width, self.height)
        self.right_edge_marker = (395, 0, self.marker_width, self.height)

        self.lane_marker_move_y = 0

        self.player_x = 250
        self.player_y = 400

        self.clock = pygame.time.Clock()
        self.fps = 120

        self.gameover = False
        self.speed = 2
        self.score = 0

        self.playing = False
        self.paused = False

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


        self.player_group = pygame.sprite.Group()
        self.vehicle_group = pygame.sprite.Group()

        self.player = PlayerVehicle(self.player_x, self.player_y)
        self.player_group.add(self.player)

        self.image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
        self.vehicle_images = []
        for self.image_filename in self.image_filenames:
            self.image = pygame.image.load('images/' + self.image_filename)
            self.vehicle_images.append(self.image)

        self.crash = pygame.image.load('images/crash.png')
        self.crash_rect = self.crash.get_rect()

        def start_game():
            self.playing = True
            self.menu.disable()
            self.click.play()
            self.main_music.stop()
            print('Game started!')

        def quit_game():
            self.click.play()
            self.playing = False
            self.running = False
            self.menu.disable()
            print('Game quit!')

        def pause_game():
            self.paused = not self.paused
            if self.paused:
                print('Game paused!')
                while self.paused:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.paused = False
                                print('Game resumed!')


                    pygame.draw.rect(self.screen, self.black, (self.width / 2 - 100, self.height / 2 - 50, 200, 100))
                    font = pygame.font.Font(pygame.font.get_default_font(), 24)
                    text = font.render('Пауза игры', True, self.white)
                    text_rect = text.get_rect()
                    text_rect.center = (self.width / 2, self.height / 2)
                    self.screen.blit(text, text_rect)

                    pygame.display.update()
                    self.clock.tick(self.fps)
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
            self.click.play()
            running = True
            while running:
                self.screen.fill(self.beige)


                font = pygame.font.Font(None, 36)
                text_y = self.height // 2 - 100  # Центрирование таблицы по вертикали
                title_text = font.render("TOP Score   Result", True, self.black)
                title_rect = title_text.get_rect(center=(self.width // 2, text_y))
                self.screen.blit(title_text, title_rect)
                text_y += 40

                for index, score in enumerate(top_scores):
                    text = font.render(f"   [{index + 1}]           {score}", True, self.black)
                    text_rect = text.get_rect(center=(self.width // 2, text_y))
                    self.screen.blit(text, text_rect)
                    text_y += 40

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        running = False


        self.running = True
        def show_game_over_menu():
            self.gameover = True
            self.gameor_sound.play()
            self.menu = pygame_menu.Menu('Game Over', 500, 500, theme=pygame_menu.themes.THEME_SOLARIZED)
            self.menu.enable()

            def start_game_over():
                self.click.play()
                self.gameover = False
                self.score = 0
                self.speed = 2
                self.vehicle_group.empty()
                self.player.rect.center = [self.player_x, self.player_y]

            def back_to_main_menu():
                self.click.play()
                self.gameover = False
                self.menu = create_main_menu()
                self.playing = False
                self.score = 0
                self.speed = 2
                self.vehicle_group.empty()
                self.player.rect.center = [self.player_x, self.player_y]


            self.menu.add.button('Начать заново', start_game_over)
            self.menu.add.button('Вернуться в меню', back_to_main_menu)

            while self.gameover:

                self.menu.update(pygame.event.get())
                self.menu.draw(self.screen)

                for self.event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameover = False
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            selected = self.menu.get_selected_widget()
                            print(f"Выбрана кнопка: {selected.get_title()}")
                            if selected.get_title() == 'Начать заново':
                                start_game_over()
                                self.gameover = False
                            elif selected.get_title() == 'Вернуться в меню':
                                back_to_main_menu()
                                self.gameover = False


                pygame.display.update()
                self.clock.tick(self.fps)

            return self.running

        # CARS OPENED

        self.car_descriptions = {
            'car.png': 'Основная машина',
            'lambo.png': 'Lamborghini',
            'greeny.png': 'Greeny Car',
            'bmw.png': 'BMW Car'
        }

        self.unlocked_cars = ['car.png']

        def check_unlocked_cars(score):
            if score >= 5 and 'lambo.png' not in self.unlocked_cars:
                self.unlocked_cars.append('lambo.png')
                print('Lambo разблокирована!')

            if score >= 10 and 'greeny.png' not in self.unlocked_cars:
                self.unlocked_cars.append('greeny.png')
                print('Greeny разблокирован!')

            if score >= 20 and 'bmw.png' not in self.unlocked_cars:
                self.unlocked_cars.append('bmw.png')
                print('BMW разблокирован!')

        def change_player_car():
            print('Доступные машины:', self.unlocked_cars)

            self.menu.clear()

            self.menu.add.button('Назад', menu_previous)
            self.click.play()

            for index, car in enumerate(self.unlocked_cars):
                self.menu.add.button(self.car_descriptions[car], select_car, car)

            print('Меню с доступными машинами')


        def select_car(selected_car):
            self.click.play()
            self.current_player_car = selected_car
            update_player_car(selected_car)
            print('Машинка изменена!')


        def menu_previous():
            self.click.play()
            self.menu.clear()
            self.menu.add.button('Начать', start_game)
            self.menu.add.button('Топ-3 результата', show_top_scores)
            self.menu.add.button('Изменить машинку', change_player_car)
            self.menu.add.button('Выход', quit_game)

        def update_player_car(selected_car):
            image = pygame.image.load('images/' + selected_car)
            self.player = PlayerVehicle(self.player.rect.center[0], self.player.rect.center[1])
            self.player.image = pygame.transform.scale(image, (self.player.rect.width, self.player.rect.height))
            self.player_group.empty()
            self.player_group.add(self.player)


        # ALL FUNCTION ARE UP
        def create_main_menu():
            self.menu = pygame_menu.Menu('Car Racing', 500, 500, theme=pygame_menu.themes.THEME_SOLARIZED)
            self.main_music.play()
            self.menu.add.button('Начать', start_game)
            self.menu.add.button('Топ-3 результата', show_top_scores)
            self.menu.add.button('Изменить машинку', change_player_car)
            self.menu.add.button('Выход', quit_game)
            return self.menu


        create_main_menu()


        # game loop
        self.running = True
        self.paused = False
        self.playing = False
        self.gameover = False
        while self.running:

            self.clock.tick(self.fps)

            if self.playing:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False

                    if event.type == KEYDOWN:

                        if event.key == K_LEFT and self.player.rect.center[0] > self.left_lane:
                            self.player.rect.x -= 100
                        elif event.key == K_RIGHT and self.player.rect.center[0] < self.right_lane:
                            self.player.rect.x += 100

                        for self.vehicle in self.vehicle_group:
                            if pygame.sprite.collide_rect(self.player, self.vehicle):

                                self.gameover = True

                                if event.key == K_LEFT:
                                    self.player.rect.left = self.vehicle.rect.right
                                    self.crash_rect.center = [self.player.rect.left, (self.player.rect.center[1] + self.vehicle.rect.center[1]) / 2]
                                elif event.key == K_RIGHT:
                                    self.player.rect.right = self.vehicle.rect.left
                                    self.crash_rect.center = [self.player.rect.right,(self.player.rect.center[1] + self.vehicle.rect.center[1]) / 2]
                            if event.key == K_p:
                                pause_game()

                self.screen.fill(self.green)

                pygame.draw.rect(self.screen, self.gray,self.road)

                pygame.draw.rect( self.screen, self.yellow, self.left_edge_marker)
                pygame.draw.rect(self.screen, self.yellow, self.right_edge_marker)

                self.lane_marker_move_y += self.speed * 2
                if self.lane_marker_move_y >= self.marker_height * 2:
                    self.lane_marker_move_y = 0
                for y in range(self.marker_height * -2, self.height, self.marker_height * 2):
                    pygame.draw.rect(self.screen, self.white, (self.left_lane + 45, y + self.lane_marker_move_y, self.marker_width, self.marker_height))
                    pygame.draw.rect(self.screen, self.white, (self.center_lane + 45, y + self.lane_marker_move_y, self.marker_width, self.marker_height))

                self.player_group.draw(self.screen)

                if len(self.vehicle_group) < 2:

                    self.add_vehicle = True
                    for self.vehicle in self.vehicle_group:
                        if self.vehicle.rect.top < self.vehicle.rect.height * 1.5:
                            self.add_vehicle = False

                    if self.add_vehicle:

                        self.lane = random.choice(self.lanes)
                        self.image = random.choice(self.vehicle_images)
                        self.vehicle = Vehicle(self.image, self.lane, self.height / -2)
                        self.vehicle_group.add(self.vehicle)

                for self.vehicle in self.vehicle_group:
                    self.vehicle.rect.y += self.speed

                    if self.vehicle.rect.top >= self.height:
                        self.vehicle.kill()

                        self.score += 1
                        check_unlocked_cars(self.score)

                        # speed up the game after passing 10 vehicles
                        if self.score > 0 and self.score % 10 == 0:
                            self.speed += 1

                self.vehicle_group.draw(self.screen)

                self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
                self.text = self.font.render('Score: ' + str(self.score), True, self.white)
                self.text_rect = self.text.get_rect()
                self.text_rect.center = (50, 400)
                self.screen.blit(self.text, self.text_rect)

                if pygame.sprite.spritecollide(self.player, self.vehicle_group, True):
                    self.gameover = True
                    self.crash_rect.center = [self.player.rect.center[0], self.player.rect.top]

                pygame.display.update()

                while self.gameover:

                    self.clock.tick(self.fps)
                    save_score(self.score)
                    show_game_over_menu()

            else:
                self.menu.mainloop(self.screen)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                    if event.type == KEYDOWN:
                        if event.key == K_p:
                            pause_game()
                        elif event.key == K_t:
                            show_top_scores()

        pygame.quit()

if __name__ == '__main__':
    car_game = CarGame()

