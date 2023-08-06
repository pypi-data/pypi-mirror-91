import pygame
import random

pygame.init()

display_widht = 800
display_height = 600
display = pygame.display.set_mode((display_widht, display_height))
pygame.display.set_caption("Dino Game")

fon_musics = ["data\sounnd\sackground0.mp3", "data\sounnd\sackground1.mp3", "data\sounnd\sackground2.mp3",
              "data\sounnd\sackground3.mp3", "data\sounnd\sackground4.mp3", "data\sounnd\sackground5.mp3",
              "data\sounnd\sackground6.mp3"]
choise_music = random.randrange(0, 7)
pygame.mixer.music.set_volume(0.5)
sound = fon_musics[choise_music]

lose_sound = pygame.mixer.Sound('data\sounnd\wtf.wav')
start_sound = pygame.mixer.Sound('data\sounnd\ok.wav')

cactus_img = [pygame.image.load("data\picture\Cactus0.png"), pygame.image.load("data\picture\Cactus1.png"),
              pygame.image.load("data\picture\Cactus2.png")]
cactus_options = [69, 449, 37, 410, 40, 420]

cloud_img = [pygame.image.load('data\picture\Cloud0.png'), pygame.image.load('data\picture\Cloud1.png')]
dino_skin2 = [pygame.image.load("data\dino\Dino0.png"), pygame.image.load("data\dino\Dino1.png"),
              pygame.image.load("data\dino\Dino2.png"),
              pygame.image.load("data\dino\Dino3.png"), pygame.image.load("data\dino\Dino4.png")]
dino_skin_3 = [pygame.image.load("data\dino\Dino2_0.png"), pygame.image.load("data\dino\Dino2_1.png"),
               pygame.image.load("data\dino\Dino2_2.png"),
               pygame.image.load("data\dino\Dino2_3.png"), pygame.image.load("data\dino\Dino2_4.png")]
dino_skin1 = [pygame.image.load("data\dino\Dino3_0.png"), pygame.image.load("data\dino\Dino3_1.png"),
              pygame.image.load("data\dino\Dino3_2.png"), pygame.image.load("data\dino\Dino3_3.png"),
              pygame.image.load("data\dino\Dino3_4.png")]
dino_draw = ()

dino_draw = dino_skin2

dino_when_jump1 = pygame.image.load('data\dino\Dino_jump3.png')
dino_when_jump2 = pygame.image.load('data\dino\Dino_jump.png')
dino_when_jump3 = pygame.image.load('data\dino\Dino_jump2.png')

dino_colision1 = pygame.image.load('data\dino\Dino_colision1.png')
dino_colision2 = pygame.image.load('data\dino\Dino_colision2.png')
dino_colision3 = pygame.image.load('data\dino\Dino_colision3.png')

dino_jump = ()
dino_jump = dino_when_jump2

dino_colision = ()
dino_colision = dino_colision2

palma = pygame.image.load('data\picture\palma.png')
frog_img = pygame.image.load('data\picture\srog.png')
tick = pygame.image.load('data\picture\sick.png')

land2 = pygame.image.load('data\picture\Land.jpg')
land3 = pygame.image.load('data\picture\Land2.jpg')
land1 = pygame.image.load('data\picture\Land3.jpg')
land = land2

dino_ico = pygame.image.load('data\picture\dino.png')
pygame.display.set_icon(dino_ico)
img_counter = 0


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            # pygame.draw.rect(display, (0, 255, 0), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, widht, image):
        self.x = radius
        self.y = y
        self.widht = widht
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, widht, height, x_init, y_init):
        self.widht = widht
        self.height = height
        self.x_init = x_init
        self.y_init = y_init
        self.inactive_clr = (69, 255, 96)
        self.active_clr = (9, 236, 70)

    def draw(self, x, y, message, action=None, font_size=30, widht_color=100, height_color=10):

        self.widht_color = widht_color
        self.height_color = height_color
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        size_color = 25

        if self.x_init < mouse[0] < self.x_init + self.widht and self.y_init < mouse[1] < self.y_init + self.height:
            pygame.draw.rect(display, self.active_clr,
                             (x, y - size_color, self.widht_color, self.height_color + size_color))
            if click[0] == 1:
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
            else:
                pygame.draw.rect(display, self.inactive_clr, (x, y, self.widht_color, self.height_color))
                print_text(message=message, x=self.x_init + 10, y=self.y_init + 10, font_size=font_size)
        else:
            pygame.draw.rect(display, self.inactive_clr, (x, y, self.widht_color, self.height_color))
            print_text(message=message, x=self.x_init + 10, y=self.y_init + 10, font_size=font_size)


class Tick:

    def __init__(self, x, y, dino_draw_1, dino_when_jump, dino_collision, background, widht=20, height=30):

        self.x = x
        self.y = y
        self.dd = dino_draw_1
        self.dj = dino_when_jump
        self.dc = dino_collision
        self.bc = background
        self.widht = widht
        self.height = height

    def draw_tick(self, action2=None):
        global dino_draw, dino_jump, dino_colision, land
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.widht and self.y < mouse[1] < self.y + self.height:
            if click[0] == 1:
                display.blit(tick, (self.x, self.y))
                dino_draw = self.dd
                dino_jump = self.dj
                dino_colision = self.dc
                land = self.bc
                if action2 is not None:
                    action2()
            else:
                display.blit(tick, (self.x, self.y))
        pygame.display.update()


usr_widht = 60
usr_height = 100
usr_x = display_widht // 3
usr_y = display_height - usr_height - 100

cactus_widht = 20
cactus_height = 70
cactus_x = display_widht - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0
speed_object = 5


def show_skins():
    exit_btn = Button(120, 70, 20, 30)
    tick3_btn = Tick(489, 430, dino_skin_3, dino_when_jump3, dino_colision3, land3, 55, 55)
    tick2_btn = Tick(489, 335, dino_skin2, dino_when_jump2, dino_colision2, land2, 55, 55)
    tick1_btn = Tick(489, 240, dino_skin1, dino_when_jump1, dino_colision1, land1, 55, 55)
    show_skin = True
    while show_skin:
        tick1_btn.draw_tick(show_menu)
        tick3_btn.draw_tick(show_menu)
        tick2_btn.draw_tick(show_menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        skins = pygame.image.load('data\picture\skins.png')
        display.blit(skins, (0, 0))
        exit_btn.draw(20, 85, 'Exit', show_menu, 50, 103, 10)


def show_menu():
    global menu_music
    prev_fon = pygame.image.load('data\picture\preview.png')
    start_btn = Button(120, 70, 332, 220)
    quit_btn = Button(120, 70, 325, 420)
    skins_btn = Button(120, 70, 318, 320)
    menu_music = pygame.mixer.music.load('data\sounnd\menu_music.mp3')
    pygame.mixer.music.play(-1)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(prev_fon, (0, 0))
        start_btn.draw(310, 280, 'Run', start_game, 50, 150, 10)
        quit_btn.draw(310, 480, 'Quit', quit, 50, 150, 10)
        skins_btn.draw(310, 380, 'Skins', show_skins, 50, 150, 10)
        pygame.display.update()


def start_game():
    global scores, make_jump, usr_y, jump_counter
    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100


def find_random_music():
    global choise_music
    pygame.mixer.Sound.play(start_sound)
    choise_new_music = random.randrange(0, 7)
    while True:
        if choise_music == choise_new_music:
            choise_music = random.randrange(0, 7)
            break
        else:
            choise_music = choise_new_music
            break
    print_musuic = fon_musics[choise_music]
    pygame.mixer.music.load(print_musuic)
    pygame.mixer.music.play(-1)


def game_cycle():
    global make_jump, game, button
    find_random_music()
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    cloud, palm, frog = open_random_objects()
    game = True
    while game:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            make_jump = True
        if make_jump:
            jump()
        if keys[pygame.K_ESCAPE]:
            pause()
        count_scores(cactus_arr)
        display.blit(land, (0, 0))
        print_text('Scores: ' + str(scores), 630, 10)
        print_text('Max scores: ' + str(max_scores), 10, 10)
        draw_array(cactus_arr)
        move_objects(cloud, palm, frog)
        draw_dino()
        if check_collisoon(cactus_arr):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(lose_sound)
            display.blit(dino_colision, (usr_x, usr_y))
            game = False
            print_text('Game over. Press Enter or Space to play again', 60, 200)
            print_text('Fon music: ' + str(find_music()), 60, 240, (0, 196, 0))
        # pygame.draw.rect(display, (247,240,22), (usr_x, usr_y, usr_widht,usr_height))

        pygame.display.update()
        clock.tick(60)
    return game_over()


def jump():
    global usr_y, make_jump, jump_counter
    if jump_counter >= -30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    widht = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_widht + 20, height, widht, img, speed_object))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    widht = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_widht + 300, height, widht, img, speed_object))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    widht = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_widht + 600, height, widht, img, speed_object))


def find_radius(array):
    maxinum = max(array[0].x, array[1].x, array[2].x)

    if maxinum < display_widht:
        radius = display_widht
        if radius - maxinum < 50:
            radius += 280
    else:
        radius = maxinum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)
    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)
            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            widht = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]
            cactus.return_self(radius, height, widht, img)


def open_random_objects():
    global cloud, palm, frog
    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    # stone = Object(display_widht, display_height - 20, 20, img_of_stone, speed_object)
    cloud = Object(display_widht, 200, 100, img_of_cloud, 1)
    palm = Object(display_widht, 600 - 150, 700, palma, speed_object)
    frog = Object(display_widht, 600 - 75, 1000, frog_img, speed_object)
    return cloud, palm, frog


def move_objects(cloud, palm, frog):
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_widht, random.randrange(50, 200), cloud.width, img_of_cloud)

    check = palm.move()
    if not check:
        choice = random.randrange(0, 2)
        cor_palm = [random.randrange(135, 155), random.randrange(220, 235)]
        palm.return_self(display_widht, 600 - cor_palm[choice], cloud.width, palma)

    check = frog.move()
    if not check:
        frog.return_self(display_widht, 600 - 75, cloud.width, frog_img)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0
    if jump_counter < 26:
        display.blit(dino_jump, (usr_x, usr_y))
    else:
        display.blit(dino_draw[img_counter // 5], (usr_x, usr_y))
        img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='data\picture\i006.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()
    button1 = Button(110, 50, 20, 80)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused. Press enter to continue', 170, 200)
        print_text('Fon music: ' + str(find_music()), 170, 240, (0, 196, 0))
        button1.draw(20, 130, 'Menu', show_menu, 40, 115, 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            paused = False
        pygame.display.update()
    pygame.mixer.music.unpause()


def check_collisoon(barriers):
    for barrier in barriers:
        if barrier.y == 449:  # little cactus
            if not make_jump:
                if barrier.x < usr_x + usr_widht - 30 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_widht - 35 <= barrier.x + barrier.width:
                        return True

            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x < usr_x + usr_widht <= barrier.x + barrier.width:
                    return True

            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_widht - 5 <= barrier.x + barrier.width:
                        return True

            elif jump_counter >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_widht - 35 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
                        return True

    return False


def count_scores(barriers):
    global scores, max_above
    above_cactus = 0
    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 < barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_widht <= barrier.x + barrier.width:
                    above_cactus += 1
        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores
    button = Button(110, 60, 20, 80)
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button.draw(20, 130, 'Menu', show_menu, 40, 115, 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return True
        pygame.display.update()


def find_music():
    if choise_music == 0:
        music_print = 'Heart shaped box. Nirvana'
        return music_print

    elif choise_music == 1:
        music_print = 'Smells like teen spirit. Nirvana'
        return music_print

    elif choise_music == 2:
        music_print = 'Comatose. Skillet'
        return music_print

    elif choise_music == 3:
        music_print = 'Awake and alive. Skillet'
        return music_print

    elif choise_music == 4:
        music_print = 'Believer. Imagine Dragons'
        return music_print

    elif choise_music == 5:
        music_print = 'Zeig dich. Rammstein'
        return music_print

    else:
        music_print = 'Stressed out. Twenty one pilots'
        return music_print


show_menu()

quit()
