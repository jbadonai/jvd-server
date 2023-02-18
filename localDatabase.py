import sqlite3


class LocalDatabase():
    def __init__(self):
        self.dbname = 'localdb.db'

    def create_settings_database(self):
        ''' creates settings table in the database '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            command = '''
            CREATE TABLE IF NOT EXISTS Settings
            (
            id integer primary key AUTOINCREMENT,
            key TEXT,
            value TEXT      
            )
            '''
            cursor.execute(command)
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in LocalDatabase module 'CREATE SETTINGS DATABASE' : {e}")

    def update_setting(self, key, value):
        ''' update the value of a setting using the key'''
        try:

            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("update Settings set value = ? where key = ?", (value, key))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'UPDATE SETTING': {e}")

    def get_settings(self, key):
        ''' Reterieve a particular settings from the database using the key '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("select value from Settings where key = ?", (key,))
            ans = cursor.fetchall()
            return ans[0][0]
        except Exception as e:
            print(f"An error occurred in localDatabase.py > get_settings() [{key}]:{e}")
            return None

    def is_setting_key_in_database(self, key):
        ''' check if a particular key exist in the settings table'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("select value from Settings where key = ?", (key,))
            ans = cursor.fetchall()
            if len(ans) == 0:
                return False
            else:
                return True

        except Exception as e:
            print(f"An error occurred in database moodule 'IS SETTING KEY IN DATABASE' : {e}")

    def setup_create_settings(self, key, value):
        ''' set up required columns in the settings table '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("insert into Settings (key, value) values (?, ?)", (key, value))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'SETUP CREATE SETTINGS': {e}")

    def initialize_database(self):
        '''
        creates required tables for video and settings in the database
        checks for required settings key entry and create one if not available
        '''
        try:
            print("Initializing and checking the database...")
            # crates settings table if it dow not exist.
            self.create_settings_database()

        except Exception as e:
            print(f"An error occurred in database module 'INITIALIZE DATABASE': {e}")

