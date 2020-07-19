import pygame as pg
import pandas as pd
import datetime as dt
import textwrapping as tw

class Card:

    date = dt.date(1,1,1)
    X = 50
    Y = 50
    SIZE_X = 890
    SIZE_Y = 530
    COLOR = (255, 255, 255)
    ALPHA = 220
    COLOR_PALETTE = []

    fonts = {} 
    selected = False
    number = -1
    sel = []
    words = []
    meanings = []

    def __init__(self, date, palette, number, fonts):
        self.date = date
        self.COLOR_PALETTE = palette
        self.selected = False
        self.number = number
        self.read_from_database()
        self.fonts = fonts

    def return_weekday(self):
        weekday = self.date.weekday()
        weekday_string = ''

        if weekday == 0:
            weekday_string = 'Poniedziałek'
        elif weekday == 1:
            weekday_string = 'Wtorek'
        elif weekday == 2:
            weekday_string = 'Środa'
        elif weekday == 3:
            weekday_string = 'Czwartek'
        elif weekday == 4:
            weekday_string = 'Piątek'
        elif weekday == 5:
            weekday_string = 'Sobota'
        elif weekday == 6:
            weekday_string = 'Niedziela'

        return weekday_string.upper()

    def return_month(self):
        month = self.date.month
        month_string = ''

        if month == 1:
            month_string = 'Stycznia'
        elif month == 2:
            month_string = 'Lutego'
        elif month == 3:
            month_string = 'Marca'
        elif month == 4:
            month_string = 'Kwietnia'
        elif month == 5:
            month_string = 'Maja'
        elif month == 6:
            month_string = 'Czerwca'
        elif month == 7:
            month_string = 'Lipca'
        elif month == 8:
            month_string = 'Sierpnia'
        elif month == 9:
            month_string = 'Września'
        elif month == 10:
            month_string = 'Października'
        elif month == 11:
            month_string = 'Listopada'
        elif month == 12:
            month_string = 'Grudnia'

        return month_string.upper()

    def read_from_database(self):
        df = pd.read_csv('data/csv/database.csv', delimiter = '|', encoding = 'utf-8')
        list_of_rows = [list(row) for row in df.values]

        self.sel = list_of_rows[self.number][1].split('*')
        self.words = list_of_rows[self.number][2].split('*')
        self.meanings = list_of_rows[self.number][3].split('*')

    def draw_words(self, display):

        if self.selected:
            SIZE_1 = 20
            SIZE_2 = 30
        else:
            SIZE_1 = 30
            SIZE_2 = 20

        if self.sel[0] == '0':
            pg.draw.rect(display, self.COLOR_PALETTE[0], (100 - SIZE_1 // 2, 290 - SIZE_1 // 2, SIZE_1, SIZE_1), 2)
        else:
            pg.draw.rect(display, self.COLOR_PALETTE[0], (100 - SIZE_1 // 2, 290 - SIZE_1 // 2, SIZE_1, SIZE_1), 0)
        if self.words[0]:
            tw.blit_text(display, self.words[0] + " - " + self.meanings[0], (140, 270), self.fonts["Words"], self.COLOR_PALETTE[1], self.COLOR_PALETTE[0], 1.0, 910, len(self.words[0].split(" ")))

        
        if self.sel[1] == '0':
            pg.draw.rect(display, self.COLOR_PALETTE[0], (100 - SIZE_2 // 2, 440 - SIZE_2 // 2, SIZE_2, SIZE_2), 2)
        else:
            pg.draw.rect(display, self.COLOR_PALETTE[0], (100 - SIZE_2 // 2, 440 - SIZE_2 // 2, SIZE_2, SIZE_2), 0)
        if self.words[1]:
            tw.blit_text(display, self.words[1] + " - " + self.meanings[1], (140, 420), self.fonts["Words"], self.COLOR_PALETTE[1], self.COLOR_PALETTE[0], 1.0, 910, len(self.words[1].split(" ")))

    def draw(self, display):
        s = pg.Surface((self.SIZE_X, self.SIZE_Y))
        s.set_alpha(self.ALPHA)
        s.fill(self.COLOR)
        display.blit(s, (self.X, self.Y))

        year_surf = self.fonts["Year"].render(str(self.date.year), True, self.COLOR_PALETTE[3])
        year_width = year_surf.get_size()[0]
        display.blit(year_surf, (495 - year_width // 2, 200))

        day_surf = self.fonts["Day"].render(str(self.date.day), True, self.COLOR_PALETTE[0])
        weekday_surf = self.fonts["Weekday"].render(self.return_weekday(), True, self.COLOR_PALETTE[1])
        month_surf = self.fonts["Month"].render(self.return_month(), True, self.COLOR_PALETTE[0])

        day_width = day_surf.get_size()[0]
        weekday_width = weekday_surf.get_size()[0]
        month_width = month_surf.get_size()[0]

        full_width = day_width + 30 + month_width

        display.blit(day_surf, (495 - full_width // 2, self.Y + 23))
        display.blit(month_surf, (495 - full_width // 2 + day_width + 30, self.Y + 23))
        display.blit(weekday_surf, (495 - weekday_width // 2, self.Y + 128))

        self.draw_words(display)

        