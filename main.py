import os
from FileLoader import FileLoader
from EventHandler import EventHandler
from sys import argv, exit
import time
from datetime import datetime
from Game import Game
import PySimpleGUI as sg
import threading

if __name__ == "__main__":

    def threadFunc(base_path, file_name):
        EventHandler(base_path, file_name, upload_file)

    access_token = ''
    file_loader = FileLoader(access_token)

    base_path = ''  # C:/Users/Utente/AppData/Local/FactoryGame/Saved/SaveGames'
    file_name = ''  # test.txt
    full_path = base_path + '/' + file_name
    dropbox_path = '/' + file_name

    def upload_file():
        file_date = datetime.now()
        dropbox_date = file_loader.get_file_datetime(dropbox_path)
        if dropbox_date is None or dropbox_date < file_date:
            file_loader.upload_file(full_path, dropbox_path)
            print("file saved to dropbox, date: " + str(file_date))
        else:
            print("cannot update file: local file is younger than dropbox file " + str(dropbox_date) + " > " + str(file_date))

    games = {}

    add_game_section = [
        [
            sg.Text("Nome del gioco"),
            sg.In(size=(25, 1), enable_events=True, key="-GAME-NAME-"),
            sg.Text("Percorso dei salvataggi"),
            sg.In(size=(25, 1), enable_events=True, key="-GAME-PATH-"),
            sg.FolderBrowse()
        ]
    ]

    game_list_section = [
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-GAME LIST-"
            )
        ]
    ]

    file_section = [
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    button_section = [
        [sg.Button("Start", button_color=("white", "blue"), size=(6, 1))],
        [sg.Button("Crea", button_color=("white", "blue"), size=(6, 1))],
        [sg.Button("Stop", button_color=("white", "red"), size=(6, 1))],
    ]

    # ----- Full layout -----
    layout = [
        [
            add_game_section,
            sg.Column(game_list_section),
            sg.Column(file_section),
            sg.Column(button_section)

        ]
    ]

    window = sg.Window("Cross Save", layout)

    while True:
        event, values = window.read()
        if event == "-GAME-PATH-":
            folder = values["-GAME-PATH-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            game = Game(values["-GAME-NAME-"], folder, file_list)
            games[game.name] = game
            game_list_frame = []
            for e in games:
                game_list_frame += [games[e].name]
            window["-GAME LIST-"].update(game_list_frame)
        elif event == "-GAME LIST-":
            try:
                file_fnames = [
                    f
                    for f in games[values["-GAME LIST-"][0]].file_name
                    if os.path.isfile(os.path.join(folder, f))
                       and f.lower().endswith((".sav", ".sav", ".txt"))
                ]
                window["-FILE LIST-"].update(file_fnames)
            except:
                pass
        elif event == 'Start':
            if len(values["-FILE LIST-"]) <= 0:
                sg.Popup('Seleziona un file per avviare la sincronizzazione, altrimenti utilizza la funzione crea', keep_on_top=True)
            else:
                file = values["-FILE LIST-"][0]
                path = games[values["-GAME LIST-"][0]].folder_path
                base_path = path  # C:/Users/Utente/AppData/Local/FactoryGame/Saved/SaveGames'
                file_name = file  # test.txt
                full_path = base_path + '/' + file_name
                dropbox_path = '/' + file_name
                sg.Popup(base_path + " " + file_name + " " + full_path + " " + dropbox_path + " ", keep_on_top=True)
                th = threading.Thread(target=threadFunc, args=(base_path, file_name))
                th.start()
        elif event == 'Crea':
            sg.Popup('Non ancora implementato', keep_on_top=True)
        elif event == 'Stop':
            sg.Popup('Non ancora implementato', keep_on_top=True)
        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

    # inizializzo tutti i giochi

    # base_path = argv[1]  # C:/Users/Utente/AppData/Local/FactoryGame/Saved/SaveGames'
    # file_name = argv[2]  # test.txt
    # full_path = base_path + '/' + file_name
    # dropbox_path = '/' + file_name
    #
    # file_loader = FileLoader(access_token)
    #
    # file_loader.download_file(full_path, dropbox_path)
    # print("File has been updated")
    #
    # def upload_file():
    #     file_date = datetime.now()
    #     dropbox_date = file_loader.get_file_datetime(dropbox_path)
    #     if dropbox_date < file_date:
    #         file_loader.upload_file(full_path, dropbox_path)
    #         print("file saved to dropbox, date: " + str(file_date))
    #     else:
    #         print("cannot update file: local file is younger than dropbox file " + str(dropbox_date) + " > " + str(file_date))
    #
    #
    # EventHandler(base_path, file_name, upload_file)
    #
    # while True:
    #     time.sleep(1)

#
