import pandas as pd
import datetime as dt

def create_database(year, number):
    COLUMN_NAMES = ['Day', 'Sel', 'Words', 'Meaning']
    export_dict = {}

    for name in COLUMN_NAMES:
        export_dict[name] = []

    startDate = dt.date(year, 1, 1)

    for _ in range(0, number):
        export_dict['Day'].append(startDate.isoformat())
        export_dict['Sel'].append('0*0')
        export_dict['Words'].append('*')
        export_dict['Meaning'].append('*')
        startDate += dt.timedelta(days = 1)

    df = pd.DataFrame(export_dict)
    df.to_csv('data/csv/database.csv', sep = '|', index = False, encoding = 'utf-8')

def save_database(year, number, day_list):

    COLUMN_NAMES = ['Day', 'Sel', 'Words', 'Meaning']
    export_dict = {}

    for name in COLUMN_NAMES:
        export_dict[name] = []

    startDate = dt.date(year, 1, 1)

    for i in range(0, number):
        day = day_list[i]
        sel = day.sel[0] + '*' + day.sel[1]
        words = day.words[0] + '*' + day.words[1]
        meanings = day.meanings[0] + '*' + day.meanings[1]

        export_dict['Day'].append(startDate.isoformat())
        export_dict['Sel'].append(sel)
        export_dict['Words'].append(words)
        export_dict['Meaning'].append(meanings)
        startDate += dt.timedelta(days = 1)

    df = pd.DataFrame(export_dict)
    df.to_csv('data/csv/database.csv', sep = '|', index = False, encoding = 'utf-8')

def load_database(day_list):
    df = pd.read_csv('data/csv/database.csv', delimiter = '|', encoding = 'utf-8')
    list_of_rows = [list(row) for row in df.values]
    
    for i in range(len(day_list)):
        day_list[i].sel = list_of_rows[i][1].split('*')
        day_list[i].words = list_of_rows[i][2].split('*')
        day_list[i].meanings = list_of_rows[i][3].split('*')