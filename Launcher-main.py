import json
import os
import random
import sys
import time

import pyautogui
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QProcess, Qt
from PySide2.QtGui import QFontDatabase, QPixmap
from PySide2.QtWidgets import QSplashScreen

from Ui_Launcher import Ui_Main_Window


# WORKING DIR CHECK START


def CheckWorkDir():
    from os.path import expanduser

    HomeDir = expanduser("~")
    HomeDir = HomeDir.lower()
    CurrentDir = os.getcwd()
    CurrentDir = CurrentDir.lower()
    if CurrentDir in ["windows\\system32", HomeDir]:
        print("Error, Please change Work Dir.")
        os.system("pause")
        sys.exit()

    if CurrentDir.find("pixelrpg-python") == -1:
        print("[WARN] You are not in PixelRPG-Python Folder.")
        print("Continue? (To exit, press Ctrl+C)")
        try:
            # countdown for 5 seconds
            for i in range(5):
                print(str(5 - i) + "...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("[WARN] Ctrl+C detected. Exiting...")
            sys.exit()
    del CurrentDir, HomeDir, expanduser


CheckWorkDir()
del CheckWorkDir

# create Log folder if not exists
if not os.path.exists("Log"):
    os.makedirs("Log")


# TODO: rewrite print to logging

# WORKING DIR CHECK END

# PYINSTALLER CHECK START


def CheckPyInstaller():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("[INFO] You are running from PyInstaller packed executable.")
        return True
    else:
        print("[INFO] You are running from normal Python source code.")
        return False


# PYINSTALLER CHECK END


def open_github_website():
    print(
        "[ERROR] Something went wrong while opening Select Class Window. I suggest you re-download game file"
    )
    import webbrowser

    webbrowser.open(
        "https://www.github.com/cytsai1008/PixelRPG-Python",
        new=0,
        autoraise=True,
    )
    del webbrowser


# JSON CHECK START


def json_dump():
    width, height = pyautogui.size()
    screensize = f"{width} x {height}"
    print(f"[INFO] Your screen size is {screensize}")
    with open("Json/config.json", "w") as f:
        # add resolution, music, windowed to json
        if width > 1920 and height > 1080:
            json.dump(
                {
                    "resolution": [screensize, "1920 x 1080", "1280 x 720"],
                    "preferresolution": screensize,
                    "music": True,
                    "windowed": False,
                    "fps": 60,
                },
                f,
                indent=4,
            )
        else:
            json.dump(
                {
                    "resolution": [screensize, "1280 x 720"],
                    "preferresolution": screensize,
                    "music": True,
                    "windowed": False,
                    "fps": 60,
                },
                f,
                indent=4,
            )
        # add resolution 2k and 4k if screensize over 1920 x 1080


if not os.path.isfile("Json/config.json"):
    print("[WARN] config.json not found.")
    print("[WARN] Creating new config.json.")
    # read screen biggest resolution
    json_dump()

# try json file is readable
try:
    with open("Json/config.json", "r") as f:
        config = json.load(f)
        resolution = config["resolution"]
        preferresolution = config["preferresolution"]
        music = config["music"]
        windowed = config["windowed"]
        fps = config["fps"]
    del config

except:
    print("[WARN] config.json corrupt.")
    print("[WARN] retry creating new config.json.")
    # read screen biggest resolution
    json_dump()
finally:
    with open("Json/config.json", "r") as f:
        config = json.load(f)
    print(f"[INFO] The resolution in config is {config['resolution']}")
    print(f"[INFO] The music in config is {config['music']}")
    print(f"[INFO] The windowed in config is {config['windowed']}")
    print(f"[INFO] The fps in config is {config['fps']}")
    print("[INFO] Starting launcher window")


# JSON CHECK END

# SYSTEM LANGUAGE CHECK START


def check_lang():
    # use module locale to check system language
    try:
        with open("Json/config.json", "r") as f:
            lang_config = json.load(f)
            lang = lang_config["lang"]
            print(f"[INFO] Language in config is {lang}")
            print("[INFO] Skipping system language detection")
            syslang = lang
            del lang, f, lang_config
    except:
        import locale

        syslang = locale.getdefaultlocale()[0].lower()
        del locale

    if syslang in ["zh_tw", "zh_hk", "zh_mo", "zh_hant"]:
        print("[INFO] System language is Chinese Traditional")
        return "zh-hant"
    elif syslang in ["zh_cn", "zh_sg", "zh_my", "zh_hans"]:
        print("[INFO] System language is Chinese Simplified")
        return "zh-hans"
    elif syslang in ["ja_jp", "ja"]:
        print("[INFO] System language is Japanese")
        return "ja"
    else:
        print("[INFO] System language current is not support, set to English")
        return "en"


return_lang = check_lang()
del check_lang


# SYSTEM LANGUAGE CHECK END


def json_save(self):
    # get resolution from combo box
    preferresolution = self.ui.Resolution_Settings.currentText()
    # get windowed from check box
    windowed = self.ui.Windowed_Settings.isChecked()
    # get music from check box
    music = self.ui.Music_On.isChecked()
    # get fps from spin box
    fps = self.ui.FPS_Settings.value()
    # write to config.json
    with open("Json/config.json", "r") as f:
        a = json.load(f)
    with open("Json/config.json", "w") as f:
        # add dict
        try:
            json_lang = a["lang"]
            data = {
                "resolution": a["resolution"],
                "preferresolution": preferresolution,
                "music": music,
                "windowed": windowed,
                "fps": fps,
                "lang": json_lang,
            }
        except:
            data = {
                "resolution": a["resolution"],
                "preferresolution": preferresolution,
                "music": music,
                "windowed": windowed,
                "fps": fps,
            }
        json.dump(data, f, indent=4)
    del a, data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.ui = Ui_Main_Window()
        self.ui.setupUi(self)
        # setup font
        QFontDatabase.addApplicationFont("Launcher Asset/unifont-14.0.01.ttf")
        # add combo box text from config.json
        self.ui.Resolution_Settings.addItems(config["resolution"])
        # set combo box text from config.json if preferresolution exist
        self.ui.Resolution_Settings.setCurrentText(config["preferresolution"])
        print(f"[INFO] Prefer resolution is {config['preferresolution']}")

        # localization
        from launcher_localization import lang_module

        lang_module(self, return_lang)
        # setting up environment

        if config["windowed"]:
            # Always remember to change Ui_Launcher file while re-compiling
            self.ui.Windowed_Settings.setChecked(True)
        else:
            self.ui.Windowed_Settings.setChecked(False)

        if config["music"]:
            # Always remember to change Ui_Launcher file while re-compiling
            self.ui.Music_On.setChecked(True)
            self.ui.Music_Off.setChecked(False)
        else:
            self.ui.Music_On.setChecked(False)
            self.ui.Music_Off.setChecked(True)

        self.ui.FPS_Settings.setValue(int(config["fps"]))
        self.ui.FPS_Settings.setReadOnly(True)
        self.ui.FPS_Settings.setEnabled(False)
        self.ui.label_FPS.setEnabled(False)
        # play button click
        self.ui.Button_Play.clicked.connect(self.Play)
        # save button click
        self.ui.Button_Save.clicked.connect(self.json_save)
        self.ui.Button_Reset.clicked.connect(self.json_reset)
        self.ui.Background.mousePressEvent = self.background_click

    def background_click(self, event):
        import random

        rick = random.randint(1, 20)
        if rick == 10:
            import webbrowser

            print("[INFO] Rick Astley is coming")
            QtWidgets.QMessageBox.information(
                self, "Look what have you done!", "Never Gonna Give You Up :)"
            )
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            sys.exit(0)

    def json_reset(self):
        json_dump()
        print("[INFO] Reset config.json")
        with open("Json/config.json", "r") as f:
            config = json.load(f)
        self.ui.Windowed_Settings.setChecked(False)
        self.ui.Music_On.setChecked(True)
        self.ui.Music_Off.setChecked(False)
        width, height = pyautogui.size()
        screensize = f"{width} x {height}"
        self.ui.Resolution_Settings.clear()
        self.ui.Resolution_Settings.addItems(config["resolution"])
        self.ui.Resolution_Settings.setCurrentText(screensize)
        self.ui.FPS_Settings.setValue(60)

    def json_save(self):
        # get resolution from combo box
        preferresolution = self.ui.Resolution_Settings.currentText()
        # get windowed from check box
        windowed = self.ui.Windowed_Settings.isChecked()
        # get music from check box
        music = self.ui.Music_On.isChecked()
        # get fps from spin box
        fps = self.ui.FPS_Settings.value()
        # write to config.json
        with open("Json/config.json", "w") as f:
            # add dict
            data = {
                "resolution": config["resolution"],
                "preferresolution": preferresolution,
                "music": music,
                "windowed": windowed,
                "fps": fps,
            }
            json.dump(data, f, indent=4)
        print("[INFO] Save config.json")
        del preferresolution, windowed, music, fps, data

    def Play(self):
        print("[INFO] Starting game and saving settings data")
        self.showMinimized()
        json_save(self)
        with open("Json/config.json", "r") as f:
            data = json.load(f)
        print(
            f"[INFO] Starting up the game with the resolution is {data['preferresolution']} \n"
            f"with windowed {data['windowed']}, \n"
            f"music is {data['music']}, \n"
            f"fps is {data['fps']}\n"
        )
        del data

        def Run_cc(self, method, ProcName):
            self.p = QProcess()
            self.p.setProcessChannelMode(QProcess.ForwardedChannels)
            self.p.start(method, [ProcName])
            print("[INFO] Play Button clicked, please select character to play")

        def Run_cc2(self, ProcName):
            self.p = QProcess()
            self.p.setProcessChannelMode(QProcess.ForwardedChannels)
            self.p.start(ProcName)

        if CheckPyInstaller():
            if os.path.exists("cc_main.exe"):
                try:
                    Run_cc2(self, "cc_main.exe")
                except:
                    open_github_website()
            else:
                open_github_website()
        else:
            if os.path.exists("cc_main.py"):
                try:
                    Run_cc(self, "python", "cc_main.py")
                except:
                    open_github_website()
            else:
                open_github_website()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    pixmap = QPixmap("Launcher Asset/Logo_Splash.png")
    splash = QSplashScreen(pixmap)
    splashlabel = QtWidgets.QLabel(splash)
    splashgif = QtGui.QMovie("Launcher Asset/Logo_Splash.gif")
    splashlabel.setMovie(splashgif)
    splashgif.start()
    splash.show()
    secret_message = random.randint(1, 1000)
    if secret_message == 34:
        splash_message = "You can be Rick Rolled by press the image"
    elif secret_message == 615:
        splash_message = "Tetora is my husband"
    else:
        splash_message = "Loading..."
    splash.showMessage(splash_message, Qt.AlignBottom, Qt.black)
    delayTime = 1.3
    timer = QtCore.QElapsedTimer()
    timer.start()
    while timer.elapsed() < delayTime * 1000:
        app.processEvents()
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
