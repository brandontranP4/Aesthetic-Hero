import pygame
import sys
import os
import time

# centered
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# constants
MUSIC = ["assets/buttons/simpsonswave.jpg", "assets/buttons/wiisports.jpg"]
TUTORIAL = ["assets/tutorial/keys1.png", "assets/tutorial/keys2.png", "assets/tutorial/keys3.png",
            "assets/tutorial/GUI.png", "assets/tutorial/fin.png"]
BLACK = (0, 0, 0)
DARK_GRAY = (62, 62, 62)
WHITE = (255, 255, 255)
PINK = (250, 128, 255)
MAGENTA = (89, 0, 109)
BLUE = (0, 26, 160)
SCREEN_FILL = PINK
WIN_W = 500
WIN_H = 1000
TIME = 0
SCORE = 0
TOTAL = 0
FPS = 60

# game
clock = pygame.time.Clock()
intro = True
play = False
tutorial = False
outro = False
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)


class Preset:
    def __init__(self, note_group, song, beat_drop, data):
        self.note_group = note_group
        self.note_count = 0
        self.music_count = 0
        self.wait_time = 0
        self.data_count = 0
        self.time_count = 0
        self.x = 0
        self.screen_time = 0
        self.screen_color = ""
        self.beat_drop = beat_drop
        self.song = pygame.mixer.Sound(song)
        self.data = data

    def update(self):
        global TIME, SCREEN_FILL
        data = self.data
        start_time = 45

        if self.x == 0:
            self.get_time()
            self.x = 1

        pink = Note("assets/notes/note1.jpg", 50, "a")
        purple = Note("assets/notes/note2.jpg", 150, "s")
        blue = Note("assets/notes/note3.jpg", 250, "k")
        cyan = Note("assets/notes/note4.jpg", 350, "l")

        if TIME % 225 == 0 and self.music_count == 0:
            self.song.play()
            self.music_count += 1

        if self.data_count <= len(data) - 1:
            m = data[self.data_count]

            # screen color
            if TIME == self.screen_time and self.screen_color == "^":
                SCREEN_FILL = MAGENTA
            elif TIME == self.screen_time and self.screen_color == "&":
                SCREEN_FILL = PINK
            elif TIME == self.screen_time and self.screen_color == "*":
                SCREEN_FILL = BLUE
            elif TIME == self.screen_time and self.screen_color == "(":
                SCREEN_FILL = BLACK

            # read data
            if m == '^':
                self.screen_time = self.wait_time + 40
                self.screen_color = "^"
            elif m == '&':
                self.screen_time = self.wait_time + 40
                self.screen_color = "&"
            elif m == '*':
                self.screen_time = self.wait_time + 40
                self.screen_color = "*"
            elif m == '(':
                self.screen_time = self.wait_time + 40
                self.screen_color = "("

            if TIME == self.wait_time + 1:
                if m == '+':
                    self.wait_time += 10
                elif m == '=':
                    self.wait_time += 5
                elif m == '-':
                    self.wait_time += 1
                elif m == "}":
                    self.wait_time += start_time
                elif m == "@":
                    self.wait_time += 5000
                elif m == '1':
                    self.wait_time += 60
                elif m == '^':
                    self.wait_time += 5
                elif m == '&':
                    self.wait_time += 5
                elif m == '*':
                    self.wait_time += 5
                elif m == '(':
                    self.wait_time += 5

                if m == 'p':
                    self.note_group.add(pink)
                    self.wait_time += 5
                elif m == 'u':
                    self.note_group.add(purple)
                    self.wait_time += 5
                elif m == 'b':
                    self.note_group.add(blue)
                    self.wait_time += 5
                elif m == 'c':
                    self.note_group.add(cyan)
                    self.wait_time += 5
                elif m == 's':
                    self.note_group.add(pink)
                    self.note_group.add(purple)
                    self.note_group.add(blue)
                    self.note_group.add(cyan)
                    self.wait_time += 5
                self.data_count += 1
        elif TIME % self.wait_time == 0:
            global play, outro
            self.song.stop()
            outro = True
            play = False

    def get_count(self):
        for d in self.data:
            if d == "p" or d == "u" or d == "b" or d == "c":
                self.note_count += 1
            elif d == "s":
                self.note_count += 4

    def get_time(self):
        for d in self.data:
            if d == "p" or d == "u" or d == "b" or d == "c" or d == "s":
                self.time_count += 5
            elif d == "=":
                self.time_count += 5
            elif d == "+":
                self.time_count += 10
            elif d == "}":
                self.time_count += 100


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, image, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = xpos
        self.rect.y = ypos

        # hitbox

        self.l_side = self.rect.centerx - self.rect.width / 2
        self.r_side = self.rect.centerx + self.rect.width / 2
        self.top = (self.rect.y - self.rect.height / 2) + 25
        self.bottom = (self.rect.y + self.rect.height / 2) + 25

    def update_image(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

class Note(pygame.sprite.Sprite):
    def __init__(self, image, xpos, note):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5.0
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.xpos = xpos
        self.rect.top = 0 + WIN_H/3
        self.intx = 0
        self.inty = 0
        self.adjust = 100
        self.note = note

    def update_image(self, image):
        self.image = pygame.image.load(image)

    def update_pos(self, xpos, ypos):
        self.rect.centerx = xpos
        self.rect.y = ypos

    def update(self):
        self.intx += 2
        self.inty += 1
        self.adjust -= 1
        self.speed += 0.5

        # size limits
        if self.intx > 100:
            self.intx = 100
        if self.inty > 50:
            self.inty = 50
        if self.adjust < 50:
            self.adjust = 50

        self.image = pygame.transform.scale(self.image, (self.intx, self.inty))
        self.rect.centerx = self.xpos + self.adjust
        self.rect.y += self.speed

        if self.rect.top > WIN_H:
            self.kill()


class Key(pygame.sprite.Sprite):
    def __init__(self, img, img_pressed, xpos, key):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.blit_image = pygame.image.load(self.img)
        self.img_pressed = pygame.image.load(img_pressed)
        self.rect = self.blit_image.get_rect()
        self.rect.x = xpos
        self.rect.y = WIN_H - (self.rect.height * 2)
        self.pressed = False
        self.hit = False
        self.key = key
        self.pressed_time = 0

    def update(self, notes):
        global SCORE, COMMENT

        time_limit = 5

        self.pressed_time += 1
        if not self.pressed:
            self.blit_image = pygame.image.load(self.img)
        elif self.pressed:
            if self.pressed_time < time_limit:
                self.blit_image = self.img_pressed
                keyCollide = pygame.sprite.spritecollide(self, notes, True)
                if keyCollide:
                    self.hit = True
                    SCORE += 1
                else:
                    self.hit = False
            elif self.pressed_time >= time_limit:
                self.blit_image = pygame.image.load(self.img)

    def cheat(self, notes):
        global SCORE

        for note in notes:
            if note.rect.y - 50 < self.rect.y < note.rect.y + 50:
                if self.key == note.note:
                    self.blit_image = self.img_pressed
                    keyCollide = pygame.sprite.spritecollide(self, notes, True)
                    if keyCollide:
                        self.hit = True
                        SCORE += 1
            else:
                self.blit_image = pygame.image.load(self.img)


class Divider(pygame.sprite.Sprite):
    def __init__(self, image, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.imageAlpha = pygame.image.load(image)
        self.xpos = xpos
        self.rect = self.image.get_rect()

    def rotate(self, angle, xoffset):
        self.image = pygame.transform.rotate(self.imageAlpha, angle)

        self.rectAlpha = self.image.get_rect()
        self.rectAlpha.center = self.rect.center
        self.rect.centerx = xoffset


class Text:
    def __init__(self, style, size, text, xpos, ypos, color):
        self.font = pygame.font.SysFont(style, size)
        self.color = color
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)

    def update_text(self, text):
        self.image = self.font.render(text, 1, self.color)

    def update_pos(self, newx, newy):
        self.rect.centerx = newx
        self.rect.y = newy

    def update_time(self):
        if TIME % 60 == 0 and TIME > 40:
            self.image = self.font.render(str((TIME/60) - 1), 1, self.color)

    def update_score(self, key_group):
        for key in key_group:
            if key.hit:
                self.image = self.font.render("Score: " + str(SCORE) + "/" + str(TOTAL), 1, self.color)


def main():
    global SCREEN_FILL, TOTAL
    points = 0
    all_count = 0
    music_read = 0
    slide_read = 0
    outro_count = 0

    # 5 mS delay after note
    # ALWAYS HAVE '}' AT END
    # '@' to extend end time for dev purposes
    # ^ for magenta, & for pink, * for blue
    # have & at the end to reset color
    # always have 3 second start
    simp = "111&p=++p++---p++---u++=u++=b++--p+--u+--b+--c+=-p+=-u+=-b+=-c+=---p++=p++=p+----u++=u++=-p++=p++=p++=p++" \
           "=p++=p++=p++=--u++=u++=---u+=-b+=-b++-c+++c+++c+++c+++c+++c++-p++-p++p+=----u++=u++-p++-p++-p++-p++-p++-p" \
           "+++=s=--s=--s^--p++=p++=p+=-u++=u++=b++=b++=b++=b++=b++=b++=b++=-p++=-p+=p++=u++=u++=p++=p++=p++=p++=p+--" \
           "-s=--s=--s=--s*--p++=---p++=p++=u++=---u++=b++=b++=b++=b++=b++=b++=-p++=-p+=p++=u++=u++=p++=p++=p++=p++=p" \
           "+++=--s=--s=--s(--p=--p=--u=--u=--p=--p=--u=--u=--u=--u=--b=--b=--p+=-u+=-b+=-c+=-p+=-u+=-b+=-c++=-p=--p=" \
           "--u=--u=--p=--p=--u=--u=--u=--u=--b=--b++=-p+=-u+=-b+=-c+=-p+=-u+=-b+=-c+=-c++=-&}"

    wii = "111&p=---u+=-c+=--b+u++--c++++=----p++=u++=b++=p++=u++=b++=p++=p+++++--u+++++=b++=c+---b+---c+=---b+=---u+" \
          "=---p+u+=-b+=-u+b11+++++=p+++++=u+++=p--u--b+=-u+=---b+u++++u--b--c+=--b+=-u+u++=p=---u++--b+b1=--u--b--c+" \
          "=--b+----u+u++=p++=-c++=-c++=-c++=-c&}"
    # groups
    div_group = pygame.sprite.Group()
    note_group = pygame.sprite.Group()
    key_group = pygame.sprite.Group()

    # text
    timer = Text("Britannica Bold", 75, "0", WIN_W - 100, 50, WHITE)
    score = Text("Britannica Bold", 50, "Score: 0", 50, 50, WHITE)

    global intro, play, outro, tutorial

    while intro:
        m_pos = pygame.mouse.get_pos()
        button_group = pygame.sprite.Group()

        # assets
        intro_drop = pygame.image.load("assets/intro.jpg")
        intro_drop = pygame.transform.scale(intro_drop, (WIN_W, WIN_H))
        choice = Note("assets/buttons/simpsonswave.jpg", WIN_W / 2, "a")
        play_button = Button(200, 50, "assets/buttons/p_button.jpg", WIN_W / 2, WIN_H / 4)
        tutorial_button = Button(200, 50, "assets/buttons/tutorial.png", WIN_W / 1.4, WIN_H / 1.1)
        left_button = Button(50, 50, "assets/buttons/l_button.png", WIN_W/2 - 175, WIN_H / 2)
        right_button = Button(50, 50, "assets/buttons/r_button.png", WIN_W/2 + 175, WIN_H / 2)
        button_group.add(play_button, tutorial_button, left_button, right_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                if left_button.l_side < m_pos[0] < left_button.r_side and left_button.top < m_pos[1] < left_button.bottom:
                    music_read += 1
                    if music_read > len(MUSIC) - 1:
                        music_read = 0
                if right_button.l_side < m_pos[0] < right_button.r_side and right_button.top < m_pos[1] < right_button.bottom:
                    music_read += 1
                    if music_read > len(MUSIC) - 1:
                        music_read = 0
                if play_button.l_side < m_pos[0] < play_button.r_side and play_button.top < m_pos[1] < play_button.bottom:
                    play_button.update_image("assets/buttons/p_button_pressed.jpg")
                    play = True
                    intro = False
                if tutorial_button.l_side < m_pos[0] < tutorial_button.r_side and tutorial_button.top < m_pos[1] < tutorial_button.bottom:
                    tutorial_button.update_image("assets/buttons/tutorial_pressed.png")
                    tutorial = True
                    intro = False

        # update
        choice.update_pos(WIN_W/2, WIN_H/2)

        screen.blit(intro_drop, (0, 0))
        screen.blit(pygame.image.load(MUSIC[music_read]), choice.rect)
        for button in button_group:
            screen.blit(button.image, button.rect)
        pygame.display.flip()

    while tutorial:
        global TUTORIAL

        m_pos = pygame.mouse.get_pos()

        left_button = Button(50, 50, "assets/buttons/l_button.png", WIN_W / 2 - 50, WIN_H / 4)
        right_button = Button(50, 50, "assets/buttons/r_button.png", WIN_W / 2 + 50, WIN_H / 4)
        back_button = Button(100, 50, "assets/buttons/back.jpg", WIN_W /2, WIN_H / 6)
        slides = Note("assets/tutorial/keys1.png", WIN_W / 2, "a")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                if left_button.l_side < m_pos[0] < left_button.r_side and left_button.top < m_pos[1] < left_button.bottom:
                    slide_read -= 1
                    if slide_read > len(TUTORIAL) - 1:
                        slide_read = 0
                    if slide_read < -1:
                        slide_read = len(TUTORIAL) - 1
                if right_button.l_side < m_pos[0] < right_button.r_side and right_button.top < m_pos[1] < right_button.bottom:
                    slide_read += 1
                    if slide_read > len(TUTORIAL) - 1:
                        slide_read = 0
                        slides.update_image(TUTORIAL[slide_read])
                if back_button.l_side < m_pos[0] < back_button.r_side and back_button.top < m_pos[1] < back_button.bottom:
                    intro = True
                    tutorial = False
                    main()

        screen.fill(PINK)
        screen.blit(left_button.image, left_button.rect)
        screen.blit(right_button.image, right_button.rect)
        screen.blit(back_button.image, back_button.rect)
        screen.blit(pygame.image.load(TUTORIAL[slide_read]), slides.rect)

        pygame.display.flip()

    while play:
        global TIME, simpsonswave, nightclubjunkie, SCORE, PRESSED_TIME

        TIME += 1

        # assets
        divider = "assets/divider.png"

        if all_count == 0:

            # dividers
            divider1 = Divider(divider, 50)
            divider2 = Divider(divider, 150)
            divider3 = Divider(divider, 250)
            divider4 = Divider(divider, 350)
            divider5 = Divider(divider, 450)
            div_group.add(divider1, divider2, divider3, divider4, divider5)

            # keys
            p_key = Key("assets/keys/key1.jpg", "assets/keys/key1_pressed.png", 50, "a")
            pu_key = Key("assets/keys/key2.jpg", "assets/keys/key2_pressed.png", 150, "s")
            b_key = Key("assets/keys/key3.jpg", "assets/keys/key3_pressed.png", 250, "k")
            c_key = Key("assets/keys/key4.jpg", "assets/keys/key4_pressed.png", 350, "l")
            key_group.add(p_key, pu_key, b_key, c_key)

            # presets
            simpsonswave = Preset(note_group, "assets/music/simpsonswave.ogg", 1320, simp)
            wiisports = Preset(note_group, "assets/music/wiisports.ogg", 1000, wii)

            simpsonswave.get_count()
            wiisports.get_count()

            all_count += 1

        # update groups
        if MUSIC[music_read] == "assets/buttons/simpsonswave.jpg":
            simpsonswave.update()
            TOTAL = simpsonswave.note_count
            if SCORE > simpsonswave.note_count:
                SCORE = simpsonswave.note_count
        elif MUSIC[music_read] == "assets/buttons/wiisports.jpg":
            wiisports.update()
            TOTAL = wiisports.note_count
            if SCORE > wiisports.note_count:
                SCORE = wiisports.note_count
        note_group.update()
        key_group.update(note_group)
        if TIME > 100:
            timer.update_time()
        score.update_score(key_group)

        # blitting
        screen.fill(SCREEN_FILL)
        for note in note_group:
            screen.blit(note.image, note.rect)
        for key in key_group:
            key.cheat(note_group)
            screen.blit(key.blit_image, key.rect)
        for div in div_group:
            screen.blit(div.image, (div.xpos - (div.rect.width/2), 0))
        screen.blit(timer.image, timer.rect)
        screen.blit(score.image, score.rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for key in key_group:
                    key.pressed_time = 0
                if event.key == pygame.K_a:
                    for key in key_group:
                        if key.key == "a":
                           key.pressed = True
                if event.key == pygame.K_s:
                    for key in key_group:
                        if key.key == "s":
                            key.pressed = True
                if event.key == pygame.K_k:
                    for key in key_group:
                        if key.key == "k":
                            key.pressed = True
                if event.key == pygame.K_l:
                    for key in key_group:
                        if key.key == "l":
                            key.pressed = True

                if event.key == pygame.K_SPACE:
                    for key in key_group:
                        key.pressed = True

            else:
                for key in key_group:
                    key.pressed = False

        # clock
        clock.tick(FPS)

    while outro:

        background = pygame.image.load("assets/background3.png")
        background = pygame.transform.scale(background, (WIN_W, WIN_H))

        grade = ""
        sCount = Text("Britannica Bold", 75, "Score", 0, 0, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                intro = True
                outro = False
                TIME = 0
                SCORE = 0
                main()

        if MUSIC[music_read] == "assets/buttons/simpsonswave.jpg":
            if outro_count == 0:
                simpsonswave.get_count()
                points = 200 * (float(SCORE) / float(simpsonswave.note_count))
                points = round(points, 2)
                outro_count += 1
        elif MUSIC[music_read] == "assets/buttons/wiisports.jpg":
            if outro_count == 0:
                wiisports.get_count()
                points = 200*(float(SCORE) / float(wiisports.note_count))
                points = round(points, 2)
                outro_count += 1

        if 100 >= points:
            grade = "A+"
        elif 90 < points < 99.99:
            grade = "A"
        elif 80 < points < 89.99:
            grade = "B"
        elif 70 < points < 79.99:
            grade = "C"
        elif 60 < points < 69.99:
            grade = "D"
        elif 10 < points < 59.99:
            grade = "F"
        elif points < 9.99:
            grade = "L"

        sCount.update_pos(WIN_W/2, WIN_H/2)
        sCount.update_text("Score: " + grade)

        screen.blit(background, (0, 0))
        screen.blit(sCount.image, sCount.rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
