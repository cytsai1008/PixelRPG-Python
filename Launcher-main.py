import sys
import json
import os
from os.path import expanduser
from PySide2 import QtWidgets, QtCore, QtGui
import pyautogui
import numpy as np

def CheckWorkDir():
    HomeDir = expanduser("~")
    HomeDir = HomeDir.lower()
    #HomeDir = HomeDir.replace("\\","\\\\")
    #print(HomeDir)
    CurrentDir = os.getcwd()
    CurrentDir = CurrentDir.lower()
    #print(CurrentDir)
    if CurrentDir in ["c:\\windows\\system32", HomeDir]:
        print("Error, Please change Work Dir.")
        os.system("pause")
        quit()

    if CurrentDir.find("pixelrpg-python") == -1:
        print("[WARN] You are not in PixelRPG-Python Folder.")
        #print("Your current working directory is:", CurrentDir)
        
from Ui_Launcher import Ui_Main_Window

CheckWorkDir()

#check if config.json exsists
if not os.path.isfile("config.json"):
    print("[WARN] config.json not found.")
    print("[WARN] Creating new config.json.")
    #read screen biggest resolution
    width, height= pyautogui.size()
    screensize = (f"{width} x {height}")
    print(f"[INFO] Your screen size is {screensize}")
    '''
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    '''
    with open("config.json", "w") as f:
        #add resolution, music, windowed to json
        json.dump({"resolution": [screensize, "1280 x 720"], "music": "on", "windowed": "on"}, f)

#try json file is readable
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        '''
        try:
            if config["screensize"] == screensize:
                pass
        except:
            print("[WARN] config.json corrupt.")
            with open("config.json", "w") as f:
                json.dump({"resolution": screensize, "music": "on", "windowed": "on"}, f)
        '''

        #print(f"[INFO] Your screen size is {config["resolution"]})

except:
    print("[WARN] config.json corrupt.")
    print("[WARN] retry creating new config.json.")
    #read screen biggest resolution
    width, height= pyautogui.size()
    screensize = (f"{width} x {height}")
    print(f"[INFO] Your screen size is {screensize}")
    '''
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    '''
    with open("config.json", "w") as f:
        #add resolution, music, windowed to json
        json.dump({"resolution": screensize, "music": "on", "windowed": "on"}, f)
finally:
    #convert resolution list to string and remove json characters and seprate each value to new line
    #config["resolution"] = str(config["resolution"]).replace("[", "").replace("]", "").replace("'", "").replace(",", "\n")
    #resolution = np.array(config["resolution"].split("\n"))
    print(f"[INFO] The resolution in config is {config['resolution']}")
    print(f"[INFO] The music in config is {config['music']}")
    print(f"[INFO] The windowed in config is {config['windowed']}")
    print('[INFO] Starting launcher window')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Main_Window()
        self.ui.setupUi(self)
        #add combo box text from config.json
        self.ui.Resolution_Settings.addItems(config["resolution"])


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())