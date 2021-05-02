import dropbox
from dropbox.files import WriteMode
import datetime

class FileLoader:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, dropbox_path):
        dropbpx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            dropbpx.files_upload(f.read(), dropbox_path, mode=WriteMode.overwrite)

    def get_file_datetime(self, dropbox_path):
        hours = datetime.timedelta(hours = 2)
        dropbpx = dropbox.Dropbox(self.access_token)
        server_date = dropbpx.files_get_metadata(dropbox_path).server_modified
        return server_date + hours

    def download_file(self, download_path, dropbox_path):
        dropbpx = dropbox.Dropbox(self.access_token)
        dropbpx.files_download_to_file(download_path, dropbox_path)