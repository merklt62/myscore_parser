import tkinter as tk
from tkinter import ttk
from tkinter import IntVar
from tkinter import BOTH
from ttkthemes import ThemedTk
from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver

from selenium.webdriver.firefox.options import Options

import pandas as pd

headers = {'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) \
             Gecko/20100101 Firefox/70.0'}
URL = 'http://m.myscore.ru/?d=1'
base_url = 'http://m.myscore.ru/match/'

league_data = []
data_1 = []
data_2 = []
data_3 = []
urls_1 = []
urls_2 = []
urls_3 = []
urls = []
full_path = []
full_path_prev = []
full_path_next = []
full_path_gecko = []
full_path_gecko_prev = []
full_path_gecko_next = []
home = []
away = []

data = ["/volleyball/", "/others", "/", "/?s=1&amp;event=refresh_button", "/tennis/", "/american-football/", "/baseball/", "/rugby/", "/handball/", "/basketball/", "/hockey/", "/?s=1&event=refresh_button", "#top", "http://www.gamblingtherapy.org/", "https://aff1xstavka.top/L?tag=s_287153m_22453c_&site=287153&ad=22453", "http://wlwinlinebet.adsrv.eacdn.com/C.ashx?btag=a_9b_53c_&affid=8&siteid=9&adid=53&c=", "https://aff1xstavka.com/L?tag=s_287153m_22453c_&site=287153&ad=22453", "/?d=1&s=1&event=refresh_button"]


class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call th0e update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor=tk.NW)

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


def write():
    df = pd.DataFrame(data_1)
    writer = pd.ExcelWriter('next_day_table.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def init_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    return driver


def get_link():
    for path_1 in full_path_gecko:
        driver = init_driver()
        driver.get(path_1)
        driver.implicitly_wait(20)

        # Ссылки на пред матч 1-й команды
        try:
            trs_home = driver.find_elements_by_class_name('odd')[0].get_attribute("onclick")[84:92]
            home.append(base_url + trs_home)
        except:
            data_2.append({
                'time_1': '',
                'command_1_1': '',
                'command_2_1': '',
                'score_1_1': '',
                'score_2_1': '',
                'ratio_1_1': '',
                'ratio_2_1': '',
                'ratio_3_1': ''
                  })
            continue
        # Ссылки на пред матч 2-й команды
        try:
            trs_away = driver.find_element_by_class_name('h2h_away').find_elements_by_class_name('odd')[0].get_attribute("onclick")[84:92]
            away.append(base_url + trs_away)
        except:
            data_3.append({
                'time_2': '',
                'command_1_2': '',
                'command_2_2': '',
                'score_1_2': '',
                'score_2_2': '',
                'ratio_1_2': '',
                'ratio_2_2': '',
                'ratio_3_2': ''
                  })
            continue
        driver.quit()


def write_home_team():
    for i in home:
        requests = session.get(i, headers=headers)

        soup = bs(requests.content, 'lxml')
        # Контейнер в котором хранятся наши элементы
        div = soup.find('div', id='main')
        try:
            time_1 = div.find_all('div', class_='detail')[2].text
        except:
            time_1 = div.find('div', class_='detail').text

        command_1 = div.find('h3').text.split(' - ')[0]
        command_2 = div.find('h3').text.split(' - ')[1]

        try:
            score_1 = div.find('div', class_='detail').find('b').text.split(':')[0]
            score_1 = int(score_1)
        except:
            score_1 = ''
        try:
            score_2 = div.find('div', class_='detail').find('b').text.split(':')[1]
            score_2 = int(score_2)
        except:
            score_2 = ''

        try:
            ratio_1 = div.find('p', class_='odds-detail').find('a').text
            ratio_1 = float(ratio_1)
        except:
            ratio_1 = '-'
        try:
            ratio_2 = div.find('p', class_='odds-detail').find_all('a')[1].text
            ratio_2 = float(ratio_2)
        except:
            ratio_2 = '-'
        try:
            ratio_3 = div.find('p', class_='odds-detail').find_all('a')[2].text
            ratio_3 = float(ratio_3)
        except:
            ratio_3 = '-'

        data_2.append({
            'time_1': time_1,
            'command_1_1': command_1,
            'command_2_1': command_2,
            'score_1_1': score_1,
            'score_2_1': score_2,
            'ratio_1_1': ratio_1,
            'ratio_2_1': ratio_2,
            'ratio_3_1': ratio_3
            })


def write_away_team():
    for j in away:
        requests = session.get(j, headers=headers)

        soup = bs(requests.content, 'lxml')
        # Контейнер в котором хранятся наши элементы
        div = soup.find('div', id='main')
        try:
            time_2 = div.find_all('div', class_='detail')[2].text
        except:
            time_2 = div.find('div', class_='detail').text

        command_1 = div.find('h3').text.split(' - ')[0]
        command_2 = div.find('h3').text.split(' - ')[1]

        try:
            score_1 = div.find('div', class_='detail').find('b').text.split(':')[0]
            score_1 = int(score_1)
        except:
            score_1 = ''
        try:
            score_2 = div.find('div', class_='detail').find('b').text.split(':')[1]
            score_2 = int(score_2)
        except:
            score_2 = ''

        try:
            ratio_1 = div.find('p', class_='odds-detail').find('a').text
            ratio_1 = float(ratio_1)
        except:
            ratio_1 = '-'
        try:
            ratio_2 = div.find('p', class_='odds-detail').find_all('a')[1].text
            ratio_2 = float(ratio_2)
        except:
            ratio_2 = '-'
        try:
            ratio_3 = div.find('p', class_='odds-detail').find_all('a')[2].text
            ratio_3 = float(ratio_3)
        except:
            ratio_3 = '-'

        data_3.append({
            'time_2': time_2,
            'command_1_2': command_1,
            'command_2_2': command_2,
            'score_1_2': score_1,
            'score_2_2': score_2,
            'ratio_1_2': ratio_1,
            'ratio_2_2': ratio_2,
            'ratio_3_2': ratio_3
            })


def lig():
    for lg in league_data:
        data_1.append({'liga: lg'})


def get_today_game():
    for path in full_path:
        requests = session.get(path, headers=headers)

        soup = bs(requests.content, 'lxml')
        # Контейнер в котором хранятся наши элементы
        div = soup.find('div', id='main')

        try:
            time = div.find_all('div', class_='detail')[2].text
        except:
            time = div.find('div', class_='detail').text

        command_1 = div.find('h3').text.split(' - ')[0]
        command_2 = div.find('h3').text.split(' - ')[1]

        try:
            score_1 = div.find('div', class_='detail').find('b').text.split(':')[0]
            score_1 = int(score_1)
        except:
            score_1 = ''
        try:
            score_2 = div.find('div', class_='detail').find('b').text.split(':')[1]
            score_2 = int(score_2)
        except:
            score_2 = ''

        try:
            ratio_1 = div.find('p', class_='odds-detail').find('a').text
            ratio_1 = float(ratio_1)
        except:
            ratio_1 = '-'
        try:
            ratio_2 = div.find('p', class_='odds-detail').find_all('a')[1].text
            ratio_2 = float(ratio_2)
        except:
            ratio_2 = '-'
        try:
            ratio_3 = div.find('p', class_='odds-detail').find_all('a')[2].text
            ratio_3 = float(ratio_3)
        except:
            ratio_3 = '-'

        data_1.append({
            'time': time,
            'command_1': command_1,
            'command_2': command_2,
            'score_1': score_1,
            'score_2': score_2,
            'ratio_1': ratio_1,
            'ratio_2': ratio_2,
            'ratio_3': ratio_3
            })


def write_xlsx():
    for i in range(len(data_1)):
        data_1[i].update(data_2[i])
        data_1[i].update(data_3[i])
    df = pd.DataFrame(data_1)
    writer = pd.ExcelWriter('all_table_next_day.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def write_all_in_one():
    get_today_game()
    get_link()
    write_home_team()
    write_away_team()
    write_xlsx()


def write_today_game():
    get_today_game()
    write()


def get_all_and_write():
    soup = bs(requests.content, 'lxml')

    # Контейнер в котором хранятся наши элементы

    div = soup.find('div', id="score-data")
    all_url = div.find_all('a')
    for all in all_url:
        all = all.get('href')
        full_path.append('http://m.myscore.ru' + all)
        full_path_gecko.append('https://www.myscore.ru/' + all + '#h2h;overall')
    get_today_game()
    get_link()
    write_home_team()
    write_away_team()
    write_xlsx()


def chk_btn_click(widget):
    soup = bs(requests.content, 'lxml')

    # Контейнер в котором хранятся наши элементы

    div = soup.find('div', id="score-data")

    leagues = div.find('h4', text=widget.cget('text'))
    urls_1 = leagues.find_all_next('a')

    try:
        leagues_n = leagues.find_next('h4')
        urls_2 = leagues_n.find_all_previous('a')
    except:
        pass

    try:
        urls = list(set(urls_1) & set(urls_2))
    except:
        urls = urls_1

    for url in urls:
        url = url.get('href')
        if url not in data:
            full_path.append('http://m.myscore.ru' + url)
            full_path_gecko.append('https://www.myscore.ru/' + url + '#h2h;overall')


def clear():
    league_data.clear()
    data_1.clear()
    data_2.clear()
    data_3.clear()
    urls_1.clear()
    urls_2.clear()
    urls_3.clear()
    urls.clear()
    full_path.clear()
    full_path_gecko.clear()
    home.clear()
    away.clear()

    for state in cbtn_states:
        state.set(0)


def get_league():
    for lg, var in zip(league_data, cbtn_states):
        if var.get() == 1:
            print(lg, var.get())
    print(len(full_path))
    print(len(full_path_gecko))


root = ThemedTk(theme='arc')
root.title('myscore')
root.geometry('680x460+300+200')
root.resizable(0, 0)

top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.55, anchor='n')

scroll_frame = Scrollable(top_frame)

lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.65, relwidth=0.6, relheight=0.3, anchor='n')

load_button_1 = ttk.Button(lower_frame, text='Записать результаты всех матчей в один файл', command=write_all_in_one)
load_button_1.place(relx=0, rely=0, relwidth=1, relheight=0.35)

load_button_2 = ttk.Button(lower_frame, text='Выбрать всё и записать в один файл', command=get_all_and_write)
load_button_2.place(relx=0, rely=0.33, relwidth=1, relheight=0.35)

load_button_3 = ttk.Button(lower_frame, text='Записать результаты \n    матчей на завтра', command=write_today_game)
load_button_3.place(relx=0, rely=0.65, relwidth=0.51, relheight=0.35)

load_button_4 = ttk.Button(lower_frame, text='Очистить', command=clear)
load_button_4.place(relx=0.5, rely=0.65, relwidth=0.5, relheight=0.35)


global requests
session = requests.Session()  # иллюзия непрерывности во времени
requests = session.get(URL, headers=headers)  # эмулируем открытие

soup = bs(requests.content, 'lxml')
# Контейнер в котором хранятся наши элементы
div = soup.find('div', id='score-data')

leagues = div.find_all('h4')  # Находим все лиги
cbtn_states = []
for league in leagues:
    league = league.text
    league_data.append(league)
    cbtn_state = IntVar()
    # все привязанные переменные сохраняем в список
    cbtn_states.append(cbtn_state)
    cbtn = ttk.Checkbutton(scroll_frame, text=league, variable=cbtn_state)
    # Делаем, чтобы при нажатии в обработчик передавался сам виджет:
    cbtn.config(command=lambda widget=cbtn: chk_btn_click(widget))
    cbtn.pack(expand=1, fill=BOTH)

scroll_frame.update()


root.mainloop()
