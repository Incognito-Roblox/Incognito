import os, psutil, json
import win32api
import pygetwindow as gw
import pyautogui

import threading, webview
import misc.app_info as IncognitoApp

from ui.mainHTML import content as html_ui
from ui.consoleHTML import content as console_ui
from exploit.api import time, ExploitAPI
from ui.manager import EventManager

RobloxHax = ExploitAPI(time.timezone + time.process_time())
scripts_path = os.path.join(os.getcwd(), "scripts")

def process_watchdog(window, client_info: list[int, str]):
    pid, client_name = client_info

    try:
        process = psutil.Process(pid)
        process.wait()
        window.evaluate_js(f"showNotification(\"Client '{client_name}' detached!\", 'Incognito'); document.querySelector('.status').style.backgroundColor = 'red';")
    except psutil.NoSuchProcess:
        print(f"No such process with PID {pid}.")

class IncognitoInterfaceAPI:
    MaxWidth = 800
    MaxHeight = 450
    ConsoleWindowHidden = False

    def __init__(self):
        self._attached_window = None

    def ExecuteScript(self, content: str):
        RobloxHax.Execute(content)

    def InitInject(self):
        success, reason, client_info = RobloxHax.Inject()

        gw.getWindowsWithTitle('Incognito')[0].activate()

        if not success:
            return json.dumps({'success': False, 'message': reason})
        elif success == 3:
            return json.dumps({'success': False, 'message': "DONT FORCE ME TO INJECT >:("})
        elif success == 4:
            return json.dumps({'success': False, 'message': "Already injected!"})
        else:
            thread = threading.Thread(target=process_watchdog, args=(self._attached_window, client_info,), daemon=True)
            thread.start()
            return json.dumps({'success': True, 'message': "Successfully injected!"})


    def FetchAppVersion(self):
        return IncognitoApp.VERSION

    def FetchIDEData(self):
        path = os.path.join(os.getcwd(), 'bin', 'api-docs.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return json.dumps(data)

    def MinimizeWindow(self):
        self._attached_window.minimize()

    def CloseWindow(self):
        self._attached_window.destroy()
        if IncognitoInterface.console_window != None:
            IncognitoInterface.console_window.destroy()

    def FetchStoredScripts(self):
        scripts = []

        for directory in os.listdir(scripts_path):
            if directory.endswith(('.lua', '.luau', '.txt')):
                filePath = os.path.join(scripts_path, directory)

                with open(filePath, 'r', encoding='utf-8') as file:
                    scripts.append({'name': directory, 'content': file.read()})
                    file.close()

        return json.dumps(scripts)

    def SaveAllScripts(self, files_list):
        for file in files_list:
            file_name = file['fileName']
            content = file['content']

            if not file_name.endswith('.lua'):
                file_name += '.lua'

            file_path = os.path.join(scripts_path, file_name)
            with open(file_path, 'w') as f:
                f.write(content)

    def SaveTabs(self, tabsData):
        directory = os.path.join(os.getcwd(), 'bin')
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, 'save.json'), 'w', encoding="utf-8") as file:
            file.write(tabsData)

    def LoadTabs(self):
        path = os.path.join(os.getcwd(), 'bin', 'save.json')
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding="utf-8") as file:
                    data = file.read()
                    data_json = json.loads(data)
                    return json.dumps({'tabs': data_json, 'count': len(data_json)})
            else:
                return json.dumps({'tabs': [], 'count': 0})
        except json.JSONDecodeError:
            return json.dumps({'tabs': [], 'count': 0})

    def CreateScriptFile(self, file_name):
        os.makedirs(scripts_path, exist_ok=True)
        file_path = os.path.join(scripts_path, file_name)

        with open(file_path, 'w') as file:
            file.write('print("incognito w")')

    def SaveScriptFile(self, file_name, content):
        if not file_name.endswith('.lua') or file_name.endswith('.luau'):
            file_name += '.lua'

        file_path = os.path.join(scripts_path, file_name)
        with open(file_path, 'w') as file:
            file.write(content)

    def ConsoleWindow(self):
        if hasattr(IncognitoInterface, 'console_window') and IncognitoInterface.console_window:
            if not self.ConsoleWindowHidden:
                IncognitoInterface.console_window.hide()
                self.ConsoleWindowHidden = True
            else:
                IncognitoInterface.console_window.show()
                self.ConsoleWindowHidden = False
        else:
            IncognitoInterface.console_window = webview.create_window(
                'Incognito Console',
                html=console_ui,
                height=400, width=700,
                background_color='#242424',
                on_top=True, frameless=True,
                easy_drag=True, zoomable=False
            )
    def messageHandler(self, data):
        if IncognitoInterface.console_window:
            IncognitoInterface.console_window.evaluate_js(f'printMessage(...{json.dumps(data["args"])})')

    def SendNotification(self, data, title="Incognito"):
        self._attached_window.evaluate_js(f"showNotification('{data}', '{title}');")

    def startResize(self, corner):
        LEFT_MOUSE_BUTTON = 0x01

        stateLeft = win32api.GetAsyncKeyState(LEFT_MOUSE_BUTTON)
        beforex, beforey = pyautogui.position()

        window = gw.getWindowsWithTitle('Incognito')[0]
        winXbefore, winYbefore = window.left, window.top
        winWbefore, winHbefore = window.width, window.height

        cornerMovement = {
            'bottom-left': lambda bx, by, ax, ay: (bx - ax, ay - by),
            'top-left': lambda bx, by, ax, ay: (bx - ax, by - ay),
            'top-right': lambda bx, by, ax, ay: (ax - bx, by - ay),
            'bottom-right': lambda bx, by, ax, ay: (ax - bx, ay - by),
            'left': lambda bx, by, ax, ay: (bx - ax, 0),
            'right': lambda bx, by, ax, ay: (ax - bx, 0),
            'top': lambda bx, by, ax, ay: (0, by - ay),
            'bottom': lambda bx, by, ax, ay: (0, ay - by),
        }

        while True:
            currentState = win32api.GetAsyncKeyState(LEFT_MOUSE_BUTTON) & 0x8000
            if currentState != stateLeft:
                stateLeft = currentState
                if currentState == 0:
                    break

            afterx, aftery = pyautogui.position()

            totalx, totaly = cornerMovement[corner](beforex, beforey, afterx, aftery)
            newX, newY = winXbefore, winYbefore
            newWidth = winWbefore + totalx if corner not in ['top', 'bottom'] else winWbefore
            newHeight = winHbefore + totaly if corner not in ['left', 'right'] else winHbefore

            window.resizeTo(max(newWidth, self.MaxWidth), max(newHeight, self.MaxHeight))

            if (newWidth >= self.MaxWidth and newHeight >= self.MaxHeight):
                newX = winXbefore if 'right' in corner or corner in ['top', 'bottom'] else winXbefore - totalx
                newY = winYbefore if 'bottom' in corner or corner in ['left', 'right'] else winYbefore - totaly

                window.moveTo(newX, newY)

            beforex, beforey = afterx, aftery
            winXbefore, winYbefore = newX, newY
            winWbefore, winHbefore = newWidth, newHeight

            time.sleep(0.001)

    def topMost(self, arg: str): # need better method, causes crashing?
        if arg == 'enable':
            self._attached_window.on_top = True
        elif arg == 'disable':
            self._attached_window.on_top = False

class IncognitoInterface:
    main_window = None
    console_window = None
    interface_api: IncognitoInterfaceAPI = None

    def __init__(self):
        self.interface_api = IncognitoInterfaceAPI()
        self.main_window = webview.create_window(
            'Incognito',
            html=html_ui,
            height=525, width=980,
            background_color='#242424',
            on_top=False, frameless=True,
            easy_drag=True, zoomable=False,
            js_api=self.interface_api, resizable=True
        )
        self.interface_api._attached_window = self.main_window

        EventManager.subscribe('error_message', lambda data: self.interface_api.messageHandler(data))
        EventManager.subscribe("notification", lambda data: self.interface_api.SendNotification(data))

    def start(self):
        webview.start(debug=False)
