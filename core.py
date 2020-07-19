import pygame as pg
import datetime as dt
import database_operations as db
import keyboard_input as ki
import textwrapping as tw
from day import Card

PALETTES = {}
PALETTES["Pink"] = [(212, 119, 145), (227, 161, 180), (237, 185, 206), (255, 239, 248)]
PALETTES["Green"] = [(106, 194, 168), (160, 232, 211), (192, 237, 224), (239, 255, 248)]

WIDTH = 990
HEIGHT = 630
SIZE = (WIDTH, HEIGHT)
TITLE = 'Calendar'
YEAR = 2020
NUMBER = 500

display = pg.display.set_mode(SIZE)
pg.display.set_caption(TITLE)

run = True
clock = pg.time.Clock()
visible = int((dt.date.today() - dt.date(YEAR, 1, 1)) / dt.timedelta(days = 1))
STARTING_VISIBLE = visible
palette = "Green"

loading_progress = 0.0

bg = {}
bg["Pink"] = pg.image.load('img/pink_circles_background.png')
bg["Green"] = pg.image.load('img/green_leaves_background.png')
tooltip = pg.image.load('img/tooltip.png')
ctrl_img = {
    "Pink": pg.image.load('img/ctrl_pink.png'),
    "Green": pg.image.load('img/ctrl_green.png')
}
menu = pg.image.load('img/ctrl_menu.png')

class SelectBlock:

    base_size = 0
    max_size = 0
    pos = (0, 0)

    def __init__(self, base_size, max_size, pos):
        self.base_size = base_size
        self.max_size = max_size
        self.pos = pos

    def draw(self, display, pal, trigger, value):
        if not trigger == value:
            pg.draw.rect(display, (255, 255, 255), (self.pos[0] - self.base_size // 2, self.pos[1] - self.base_size // 2, self.base_size, self.base_size), 0)
            pg.draw.rect(display, pal[0], (self.pos[0] - self.base_size // 2, self.pos[1] - self.base_size // 2, self.base_size, self.base_size), 2)
        else:
            pg.draw.rect(display, pal[0], (self.pos[0] - self.max_size // 2, self.pos[1] - self.max_size // 2, self.max_size, self.max_size), 0)


def draw_loading():
    display.blit(bg[palette], (0, 0))
    load_surf = pg.font.Font('fonts/Montserrat-Bold.otf', 90).render(str(int(loading_progress)) + "%", True, PALETTES[palette][0])
    load_width = load_surf.get_size()[0]
    display.blit(load_surf, (495 - load_width // 2, 230))
    pg.draw.rect(display, (255,255,255), (395, 330, 200, 30), 0)
    pg.draw.rect(display, PALETTES[palette][1], (395, 330, int(loading_progress) * 2, 30), 0)
    pg.draw.rect(display, PALETTES[palette][1], (395, 330, 200, 30), 3)
    pg.display.update()

def draw_tutorial():
    display.blit(bg[palette], (0, 0))
    display.blit(tooltip, (0,0))
    waiting = True
    pg.display.update()
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = False
        clock.tick(30)

def init():
    pg.init()
    global loading_progress
    loading_progress = 10.0
    f = open("core.properties", "r")
    x = f.read()
    f.close()
    if x == "0":
        draw_tutorial()
        f = open("core.properties", "w")
        f.write("1")
        
    try:
        f = open("data/csv/database.csv")
    except:
        print("Database not found, creating new from Template")
        db.create_database(YEAR, NUMBER)
    display.blit(bg[palette], (0, 0))
    pg.display.update()
    draw_loading()
    loading_progress = 20.0
    print("Core initialized")


def generate_days():
    global loading_progress
    day_list = []
    p = NUMBER // 100

    fonts = {
        "Day": pg.font.Font('fonts/Montserrat-Bold.otf', 90),
        "Month": pg.font.Font('fonts/Montserrat-SemiBold.otf', 90),
        "Weekday": pg.font.Font('fonts/Montserrat-Bold.otf', 45),
        "Year": pg.font.Font('fonts/Montserrat-Bold.otf', 300),
        "Words": pg.font.Font('fonts/Montserrat-Bold.otf', 35),
        "Meaning": pg.font.Font('fonts/Montserrat-Bold.otf', 35)
    }

    for i in range(NUMBER):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        if i % p == 0:
            if loading_progress < 100:
                loading_progress += 0.8
            draw_loading()
        day = Card(dt.date(YEAR, 1, 1) + dt.timedelta(days = i), PALETTES[palette], i, fonts)
        day_list.append(day)
    return day_list

def start_anim():
    s = pg.Surface((990, 630), pg.SRCALPHA)
    alpha = 0
    for i in range(255):
        alpha += 1
        s.set_alpha(alpha)
        s.fill((255, 255, 255, alpha))
        display.blit(s, (0, 0))
        pg.display.update()
    for i in range(255):
        alpha -= 1
        s.set_alpha(alpha)
        s.fill((255, 255, 255, alpha))
        display.blit(s, (0, 0))
        pg.display.update()
    

def main_loop():
    global run, visible, palette, bg
    pg.key.set_repeat(500, 50)

    print("Images loaded")
    day_list = generate_days()
    print("Entering main loop")

    start_anim()

    ctrl = False
    prev = visible
    screen = 0
    sel = 0
    mode = 0
    input_string = ''
    word = 0

    while run:

        all_keys = pg.key.get_pressed()
        if all_keys[pg.K_LCTRL]:
            ctrl = True
        else:
            ctrl = False

        selects = []
        for i in range(5):
            block = SelectBlock(25,32,(100,95 + i*110))
            selects.append(block)

        if screen == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    key = event.key
                    if not ctrl:
                        if key == pg.K_RIGHT:
                            prev = visible
                            visible += 1
                        if key == pg.K_LEFT:
                            prev = visible
                            visible -= 1                        
                        if key == pg.K_ESCAPE:
                            prev = visible
                            visible = STARTING_VISIBLE
                        if key == pg.K_UP or key == pg.K_DOWN:
                            day_list[visible].selected = not day_list[visible].selected
                        if key == pg.K_x:
                            palette = "Pink"
                        if key == pg.K_z:
                            palette = "Green"
                        if key == pg.K_RETURN:
                            if day_list[visible].selected:
                                if day_list[visible].sel[1] == "1":
                                    day_list[visible].sel[1] = "0"
                                elif day_list[visible].sel[1] == "0":
                                    day_list[visible].sel[1] = "1"
                            else:
                                if day_list[visible].sel[0] == "1":
                                    day_list[visible].sel[0] = "0"
                                elif day_list[visible].sel[0] == "0":
                                    day_list[visible].sel[0] = "1"
                    else:
                        if key == pg.K_z:
                            temp = visible
                            visible = prev
                            prev = temp
                        if key == pg.K_s:
                            db.save_database(YEAR, NUMBER, day_list)
                        if key == pg.K_l:
                            db.load_database(day_list)
                        if key == pg.K_a:
                            screen = 1

            display.blit(bg[palette], (0, 0))
            day_list[visible].COLOR_PALETTE = PALETTES[palette]
            day_list[visible].draw(display)

            if ctrl:
                display.blit(ctrl_img[palette], (0,0))
        
        if screen == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    key = event.key
                    if key == pg.K_UP:
                        sel -= 1
                        if sel < 0:
                            sel+=5
                    if key == pg.K_DOWN:
                        sel += 1
                        sel %= 5
                    if key == pg.K_ESCAPE:
                        screen = 0
                    if key == pg.K_RETURN:
                        if sel == 0:
                            day_list[visible].words[0] = ''
                            day_list[visible].meanings[0] = ''
                            screen = 0
                        elif sel == 1:
                            day_list[visible].words[1] = ''
                            day_list[visible].meanings[1] = ''
                            screen = 0
                        elif sel == 2:
                            screen = 2
                            word = 0
                        elif sel == 3:
                            screen = 2
                            word = 1
                        elif sel == 4:
                            screen = 0

            display.blit(bg[palette], (0, 0))
            display.blit(menu, (0, 0))
            for i, block in enumerate(selects):
                block.draw(display, PALETTES[palette], sel, i)

        if screen == 2:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    key = event.key
                    uni = event.unicode
                    if key == pg.K_ESCAPE:
                        screen = 0
                    if key == pg.K_RETURN:
                        if mode == 1:
                            mode = 0
                            screen = 0
                            day_list[visible].meanings[word] = input_string
                            input_string = ''
                        else:
                            mode += 1
                            day_list[visible].words[word] = input_string
                            input_string = ''
                    elif key == pg.K_BACKSPACE:
                        if len(input_string) > 0:
                            input_string = input_string[:-1]
                    elif uni:
                        if (len(input_string) <= 40 and mode == 0) or (len(input_string) <= 80 and mode == 1):
                            input_string += uni

            display.blit(bg[palette], (0, 0))
            s = pg.Surface((890, 530))
            s.set_alpha(220)
            s.fill((255, 255, 255))
            display.blit(s, (50, 50))

            if mode == 0:
                text_surf = pg.font.Font('fonts/Montserrat-SemiBold.otf', 50).render("PODAJ ZWROT", True, PALETTES[palette][0])
                text_width = text_surf.get_size()[0]
                display.blit(text_surf, (495 - text_width // 2, 80))

                text_surf = pg.font.Font('fonts/Montserrat-SemiBold.otf', 25).render("(MAKSYMALNIE 40 ZNAKÓW):", True, PALETTES[palette][1])
                text_width = text_surf.get_size()[0]
                display.blit(text_surf, (495 - text_width // 2, 140))

                tw.blit_text(display, input_string, (100, 200), pg.font.Font('fonts/Montserrat-SemiBold.otf', 40), PALETTES[palette][0], PALETTES[palette][0], 0.9, 890, 0)


            elif mode == 1:
                text_surf = pg.font.Font('fonts/Montserrat-SemiBold.otf', 50).render("PODAJ ZNACZENIE", True, PALETTES[palette][0])
                text_width = text_surf.get_size()[0]
                display.blit(text_surf, (495 - text_width // 2, 80))

                text_surf = pg.font.Font('fonts/Montserrat-SemiBold.otf', 25).render("(MAKSYMALNIE 80 ZNAKÓW):", True, PALETTES[palette][1])
                text_width = text_surf.get_size()[0]
                display.blit(text_surf, (495 - text_width // 2, 140))

                tw.blit_text(display, input_string, (100, 200), pg.font.Font('fonts/Montserrat-SemiBold.otf', 40), PALETTES[palette][1], PALETTES[palette][1], 0.9, 890, 0)
        
        pg.display.update()
        clock.tick(30)

    print("Saving database")
    db.save_database(YEAR, NUMBER, day_list)
    pg.quit()
    quit()