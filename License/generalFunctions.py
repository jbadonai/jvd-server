import math
import pyautogui
import threading
import time
from PyQt5.QtWidgets import  QFileDialog
import subprocess
import uuid
import platform
from security import JBHash, JBEncrypter
from videoDatabase import VideoDatabase
from environment import Config
import re


class GeneralFunctions():
    def __init__(self):
        super(GeneralFunctions, self).__init__()

    def is_trial_activated(self):
        fr = VideoDatabase().get_settings('trial_activated')
        return bool(int(fr))

    def is_trial_expired(self):
        fr = VideoDatabase().get_settings('trial_expired')
        return bool(int(fr))

    def is_fully_activated(self):
        fr = VideoDatabase().get_settings('fully_activated')
        return bool(int(fr))

    def is_message_sent_successful(self):
        fr = VideoDatabase().get_settings('message_sent_successfully')
        return bool(int(fr))

    def get_this_machine_id(self):
        try:
            my_system = platform.uname()

            system = my_system.system
            nodeName = my_system.node
            release = my_system.release
            machine = my_system.machine
            processor = my_system.processor

            # set system id literal
            message = f"{nodeName}.{system}.{release}.{machine}.{processor}.{Config().config('ENCRYPT_PASSWORD')}"

            # layer 1 encryption of system id [encrption]
            encryptedMessage = JBEncrypter().encrypt(message, Config().config('ENCRYPT_PASSWORD'))

            # layer 1 encryption of system id [hash]
            hashMessage = JBHash().hash_message_with_nonce(message)

            # layer 2 encryption of stystem id layer 1 [hash] + uuid
            machineID = uuid.uuid5(uuid.NAMESPACE_URL, hashMessage[1])

            # print('-----------------------------')
            # print(encryptedMessage)

            machine_id = {"id": str(machineID), "key": encryptedMessage.decode()}

            return machine_id

            pass

        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] >  Get_this_machine_id(): {e}")

    def apply_user_to_this_machine(self, user_data):
        pass

    def get_screen_height(self):
        size = pyautogui.size()
        return size.height

    def get_screen_size(self):
        size = pyautogui.size()
        return size

    def check(self, email):
        try:
            # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

            # if re.search(regex, email):
            if re.fullmatch(regex, email):
                print("Valid Email")
                return True
            else:
                print("Invalid Email")
                return False
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] >  check(): {e}")

    def browse_folder_location(self, parent):
        try:
            print('browsing for folder location...')
            dl = QFileDialog.getExistingDirectory(parent, "open location")
            if dl != "":
                return dl
            else:
                return None
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] >  browse_folder_location():\n{e}")
            return None
        pass

    def browse_file_location(self, parent):
        try:
            dl,_ = QFileDialog.getOpenFileName(parent, "Open", "open location")
            if dl != "":
                # print(dl)
                return dl
            else:
                return None
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > browse_file_location(): \n >>>{e}")
            return None

    def centralize_main_window(self, mainWindow, size_percentage = 70):

        try:
            size = pyautogui.size()  # get screen resolution
            height = int(size.height * size_percentage / 100)  # set windows height to 70% of the the screen height
            width = int(size.width * size_percentage / 100)  # set window width to 70% of the screen width
            top = int(size.height / 2) - height / 2  # centralize the top
            left = int(size.width / 2) - width / 2  # centralize the width
            mainWindow.setGeometry(int(left), int(top), int(width), int(height))  # set windows geometry.
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > centralize_main_window(): {e}")

    def generate_video_download_options(self, logger, hook, outtemplate="test.%(ext)s", video_format ="'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'", username=None, password=None):
        try:
            ydl_opts = None

            if username is None or password is None:
                ydl_opts = {
                    'ignoreerrors': True,
                    # 'outtmpl': outtemplate,
                    # 'format': video_format,
                    # 'postprocesor-args': 'loglevel quiet, -8',
                    # 'nopart': True,
                    # 'quiet': True,
                    'logger': logger,
                    'progress_hooks': [hook],
                }
            else:
                ydl_opts = {
                    'ignoreerrors': True,
                    # 'outtmpl': outtemplate,
                    # # 'format': video_format,
                    # 'username': username,
                    # 'password': password,
                    # 'postprocesor-args': 'loglevel quiet, -8',
                    # 'nopart': True,
                    # 'quiet': True,
                    'logger': logger,
                    'progress_hooks': [hook],
                }
            return ydl_opts
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > generate_video-download_options(): {e}")

    def generate_audio_download_options(self, outtemplate, logger, hook, username=None, password=None):
        try:
            ydl_opts = None

            if username is None or password is None:
                ydl_opts = {
                    'ignoreerrors': True,
                    'outtmpl': outtemplate,
                    # 'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',

                    }],
                    'postprocesor-args': 'loglevel quiet, -8',
                    'nopart': True,
                    'quiet': True,
                    'logger': logger,
                    'progress_hooks': [hook],
                }

            else:
                ydl_opts = {
                    'ignoreerrors': True,
                    'outtmpl': outtemplate,
                    # 'format': 'bestaudio/best',
                    'password': password,
                    'username': username,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',

                    }],
                    'postprocesor-args': 'loglevel quiet, -8',
                    'nopart': True,
                    'quiet': True,
                    'logger': logger,
                    'progress_hooks': [hook],

                }

            return ydl_opts
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > generate_audio_download_options(): {e}")

    def scroll_to_bottom(self, obj: object):
        try:
            # scrollBar = self.scrollArea_downloadItems.verticalScrollBar()
            # obj.verticalScrollBar().setValue(2147483647)
            for x in range(3):
                obj.verticalScrollBar().setValue(2147483647)
                time.sleep(0.1)
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > scroll_to_bottom(): {e}")

    def dict_to_list(self, dictionary):
        '''
        converts dictionary to list
        :param dictionary:
        :return:
        '''

        try:
            new_list = []
            for item in dictionary:
                new_list.append(dictionary[item])

            return new_list
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > dict_to_list(): {e}")

    def format_seconds(self, seconds):
        try:
            h = seconds // 3600
            ms = seconds % 3600
            m = ms // 60
            s = ms % 60

            if h > 0 and m > 0:
                return f"{str(h).zfill(2)}h:{str(m).zfill(2)}m:{str(s).zfill(2)}s"
            if h == 0 and m > 0:
                return f"{str(m).zfill(2)}m:{str(s).zfill(2)}s"
            if h == 0 and m == 0 and s > 0:
                return f"{str(s).zfill(2)}s"
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > format_seconds(): {e}")

    def database_list_to_dictionary(self, dbList):
        try:
            d = {}
            d['download_video']= bool(dbList[1])
            d['download_all']= bool(dbList[2])
            d['format']= dbList[3]
            d['url']= dbList[4]
            d['title']=(dbList[5])
            d['is_playlist']= bool(dbList[6])
            d['playlist_index']= dbList[7]
            d['playlist_title']= dbList[8]
            d['playlist_url']= dbList[9]
            d['thumbnail']= dbList[10]
            d['status']= dbList[11]
            d['download_location']= dbList[12]

            return d
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > database_list_to_dictionary(): {e}")

    def screen_the_title(self, title):
        """
        This function removes illegal characters from text passed into it.
        it was intended to remove illegal characters from video title which can cause error while saving
        """

        try:
            final = ""  # holds the final result
            for c in title:  # loop through every character in the text supplied
                # check if current character is accepted
                if c.isalnum() or c.isalpha() or c.isspace() or c.isnumeric() or c.isdigit() or c.isidentifier():
                    final = final + c  # add the accepted character to the final result

            return final
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > screen_the_title() {e}")

    def purify_raw_data_from_database_dict(self, d: dict):
        """
        This makes sure that all data types are correct by converting expected data to their data types.
        expected data from dictionary

        takes in dictionary as the argument and return a dictionary
        """
        try:
            download_video = bool(d['download_video'])
            download_all = bool(d['download_all'])
            video_format = d['format']
            url = d['url']
            title = self.screen_title(d['title'])
            is_playlist = bool(d['is_playlist'])
            playlist_index = d['playlist_index']
            playlist_title = d['playlist_title']
            playlist_url = d['playlist_url']
            thumbnail = d['thumbnail']
            status = d['status']
            download_location = d['download_location']

            my_data = {'download_video': download_video,
                       'download_all': download_all,
                       'format': video_format,
                       'title': title,
                       'url': url,
                       'is_playlist': is_playlist,
                       'playlist_index': playlist_index,
                       'playlist_title': playlist_title,
                       'playlist_url': playlist_url,
                       'thumbnail': thumbnail,
                       'status': status,
                       'download_location': download_location
                       }
            return my_data
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > purify_raw_dat_from_database() : {e}")

    def purify_raw_data_from_database_list(self, d):
        """
        This makes sure that all data types are correct by converting expected data to their data types
        expected data list from database directly.
        """
        try:
            download_video = bool(d[1])
            download_all = bool(d[2])
            video_format = d[3]
            url = d[4]
            title = self.screen_title(d[5])
            is_playlist = bool(d[6])
            playlist_index = d[7]
            playlist_title = d[8]
            playlist_url = d[9]
            thumbnail = d[10]
            status = d[11]
            download_location = d[12]

            my_data = {'download_video': download_video,
                       'download_all': download_all,
                       'format': video_format,
                       'title': title,
                       'url': url,
                       'is_playlist': is_playlist,
                       'playlist_index': playlist_index,
                       'playlist_title': playlist_title,
                       'playlist_url': playlist_url,
                       'thumbnail': thumbnail,
                       'status': status,
                       'download_location': download_location
                       }
            return my_data
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > purify_raw_data_from_database_list() : {e}")

    def convert_size(self, size_bytes):
        ''' This function converts size in bytes to respective value in KB, MB, GB...'''
        try:
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > convert_siae(): {e}")

    def IsInternet(self):
        try:
            ''' This function checks for internet availability'''
            result = subprocess.getoutput("ping www.google.com -n 1")

            if result.lower().__contains__('timed out'):
                return False
            elif result.lower().__contains__('general failure'):
                return False
            elif result.lower().__contains__('could not find host'):
                return False
            elif result.__contains__('TTL='):
                return True
            else:
                return False
        except Exception as e:
            return f"An Error Occurred in [generalFunctions.py] > IsInternet(): [{e}][{result}]"

    def is_url_valid(self, url):
        pattern = "^(?:http(s)?://)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
        if re.search(pattern, url):
            if str(url).lower().__contains__('www') or str(url).lower().__contains__('http'):
                return True
        else:
            return False

    def run_function(self, functionName, join: bool = False, *args):
        try:
            t = threading.Thread(target=functionName, args=args)
            t.daemon = True
            t.start()
            if join:
                t.join()
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > run_function(): {e}")

    def extract_playlist_video_download_data_list(self, rawdata):
        try:
            download_data_list = []

            for d in rawdata['entries']:
                try:
                    title = d['title']
                    url = d['webpage_url']
                    playlist_index = d['playlist_index']
                    playlist_title = d['playlist_title']
                    thumbnail = d['thumbnail']
                    isPlaylist = True
                    data = (title, url, isPlaylist, playlist_index, playlist_title, thumbnail)
                    # print(f"DATA >>>>> {data}")
                    download_data_list.append(data)
                except Exception as e:
                    print(f'an error occurred in extract playlist video download: {e}')
                    # print(title, '>', url)
                    # print(download_data_list)
                    # input("have you seen the error above")
                    # time.sleep(0.5)
                    continue

            # print(download_data_list)
            return download_data_list
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > extract_playlist_video_download_data_list(): {e}")

    def extract_single_video_download_data_list(self, rawdata):
        try:
            download_data_list = []
            d = rawdata
            title = d['title']
            url = d['webpage_url']
            playlist_index = None
            playlist_title = None
            thumbnail = d['thumbnail']
            isPlaylist = False

            data = (title, url, isPlaylist, playlist_index, playlist_title, thumbnail)
            download_data_list.append(data)

            return download_data_list
        except Exception as e:
            print(f"An Error Occurred in [generalFunctions.py] > extract_single_video_download_data_list(): {e}")

