import pygame
import sys
import os

# centered
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# constants
BLACK = (0, 0, 0)
DARK_GRAY = (62, 62, 62)
WHITE = (255, 255, 255)
WIN_W = 500
WIN_H = 1000
TIME = 0
SCORE = 0
FPS = 60

# game
clock = pygame.time.Clock()
intro = True
play = False
outro = False
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)


class Preset:
    def __init__(self, note_group, song):
        self.note_group = note_group
        self.count = 0
        self.music_count = 0
        self.wait_time = 0
        self.data_count = 0
        self.song = pygame.mixer.Sound(song)

    def update(self, data):
        global TIME

        pink = Note("assets/notes/note1.jpg", 50)
        purple = Note("assets/notes/note2.jpg", 150)
        blue = Note("assets/notes/note3.jpg", 250)
        cyan = Note("assets/notes/note4.jpg", 350)

        if TIME % 100 == 0 and self.music_count == 0:
            self.song.play()
            self.music_count += 1

        if self.data_count <= len(data) - 1:
            m = data[self.data_count]
            if TIME == self.wait_time + 1:
                if m == '+':
                    self.wait_time += 10
                elif m == '=':
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
        elif self.data_count > len(data):
            self.song.stop()


class Note(pygame.sprite.Sprite):
    def __init__(self, image, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.xpos = xpos
        self.rect.top = 0 - self.rect.height

    def update(self):
        self.rect.x = self.xpos
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

    def update(self, notes):
        global SCORE, COMMENT
        if not self.pressed:
            self.blit_image = pygame.image.load(self.img)
        elif self.pressed:
            self.blit_image = self.img_pressed
            keyCollide = pygame.sprite.spritecollide(self, notes, True)
            if keyCollide:
                self.hit = True
                for note in notes:
                    if note.rect.bottom < self.rect.centerx:
                        SCORE += 1
            else:
                self.hit = False


class Divider(pygame.sprite.Sprite):
    def __init__(self, image, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.xpos = xpos
        self.rect = self.image.get_rect()


class Text:
    def __init__(self, style, size, text, xpos, ypos, color):
        self.font = pygame.font.SysFont(style, size)
        self.color = color
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)

    def update_time(self):
        if TIME % 60 == 0:
            self.image = self.font.render(str((TIME/60)-2), 1, self.color)

    def update_score(self, key_group):
        for key in key_group:
            if key.hit:
                self.image = self.font.render("Score: " + str(SCORE), 1, self.color)


def main():
    all_count = 0

    # 5 mS delay after note
    res = "+p++p++p+=u+=b++c++c++c++c++c++c++u++u++u+=b++u++p++p++p++p++p++p++u++u++u+=b+=b++c++c++c++c++c++c" \
          "++c++p++p++p+=u+=b++p++p++p++p++p++p++p++p=u=b=c++++=p++u=b=c+=c++c++c++c++c++u++u++u++p=u=b=c=p=u=b=c=" \
          "p=u=b=c=p=u=b=c=p=u=b=c++p=u=p=u=p+=b+++p=u=b=c+=c+=c+=c+=c+=c+=c"

    ncjd = "+++++b++p=u=b=u=p=p+=u++p=u=b=c=c=b=c+++p=p=u=b=b+=u+++u=u=u=p=c=c=c"

    # groups
    div_group = pygame.sprite.Group()
    note_group = pygame.sprite.Group()
    key_group = pygame.sprite.Group()

    # text
    timer = Text("Britannica Bold", 75, "0", WIN_W - 100, 50, WHITE)
    score = Text("Britannica Bold", 50, "Score: 0", 50, 50, WHITE)

    global intro, play, outro
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                play = True
                intro = False

    screen.fill(WHITE)
    pygame.display.flip()

    while play:
        global TIME, resonance

        TIME += 1

        # assets
        background = pygame.image.load("assets/background.jpg")
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
            p_key = Key("assets/keys/key1.png", "assets/keys/key1_pressed.png", 50, "a")
            pu_key = Key("assets/keys/key2.png", "assets/keys/key2_pressed.png", 150, "s")
            b_key = Key("assets/keys/key3.png", "assets/keys/key3_pressed.png", 250, "k")
            c_key = Key("assets/keys/key4.png", "assets/keys/key4_pressed.png", 350, "l")
            key_group.add(p_key, pu_key, b_key, c_key)

            # presets
            resonance = Preset(note_group, "assets/music/resonance.ogg")
            ncj = Preset(note_group, "assets/music/Night_Club_Junkie.ogg")

            all_count += 1

        # update groups
        ncj.update(ncjd)
        note_group.update()
        key_group.update(note_group)
        if TIME > 100:
            timer.update_time()
        score.update_score(key_group)

        # blitting
        screen.blit(background, (0, 0))
        for note in note_group:
            screen.blit(note.image, note.rect)
        for key in key_group:
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

if __name__ == "__main__":
    main()
