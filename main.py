import os
from FileLoader import FileLoader
from EventHandler import EventHandler
from sys import argv, exit
import time
from datetime import datetime

if __name__ == "__main__":
    # carica token tramite file esterno, se il file non viene trovato solleva un eccezione
    access_token = ''

    base_path = argv[1]  # C:/Users/Utente/AppData/Local/FactoryGame/Saved/SaveGames'
    file_name = argv[2]  # test.txt
    full_path = base_path + '/' + file_name
    dropbox_path = '/' + file_name

    file_loader = FileLoader(access_token)

    file_loader.download_file(full_path, dropbox_path)
    print("File has been updated")

    def upload_file():
        file_date = datetime.now()
        dropbox_date = file_loader.get_file_datetime(dropbox_path)
        if dropbox_date < file_date:
            file_loader.upload_file(full_path, dropbox_path)
            print("file saved to dropbox, date: " + str(file_date))
        else:
            print("cannot update file: local file is younger than dropbox file " + str(dropbox_date) + " > " + str(file_date))


    EventHandler(base_path, file_name, upload_file)

    while True:
        time.sleep(1)

#
