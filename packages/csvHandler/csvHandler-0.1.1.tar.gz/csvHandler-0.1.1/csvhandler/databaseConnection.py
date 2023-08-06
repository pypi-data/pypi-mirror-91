import sqlite3


class SqliteConnection():
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.file_path)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()
