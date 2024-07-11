import time, threading, guardshield, ctypes, win32api
from ctypes import windll, wintypes

from ui.interface import IncognitoInterface
from misc.bootstrapper import Bootstrapper, SystemInfo

kernel32, ntdll, user32 = windll.kernel32, windll.ntdll, windll.user32

def error_box(content: str, style: int = 0):
    return user32.MessageBoxW(0, content, "Incognito", style | 0x10 | 0x1000 | 0x10000 | 0x40000 | 0x200000)

def erase_pe_header():
    base_addy = ctypes.c_ulonglong(win32api.GetModuleHandle(None))
    old_protect = wintypes.DWORD(0)

    kernel32.VirtualProtect(ctypes.pointer(base_addy), 4096, 0x04, ctypes.pointer(old_protect))
    ctypes.memset(ctypes.pointer(base_addy), 4096, ctypes.sizeof(base_addy))

def hide_threads():
    process_id = kernel32.GetCurrentProcessId()

    process_handle = kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if process_handle is None:
        return

    thread_id = kernel32.GetCurrentThreadId()
    thread_handle = kernel32.OpenThread(0x1F03FF, False, thread_id)
    if thread_handle is None:
        kernel32.CloseHandle(thread_id)
        return

    ntdll.NtSetInformationThread(
        thread_handle, 0x11, ctypes.byref((ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
    )

    kernel32.CloseHandle(thread_handle)
    kernel32.CloseHandle(process_handle)

def watchdog_checker():
    watchdog = guardshield.Security(
        anti_debugger=True,
        detect_vm=True,
        detect_sandbox=True
    )

    erase_pe_header()
    hide_threads()

    while True:
        time.sleep(1/20)

        if watchdog.check_debug():
            interface.main_window.hide()
            pressed_btn = error_box("STOP TOUCHING ME INSIDES YOU FILTHY ANIMAL!", 0x01)

            if pressed_btn == 1: # ok
                watchdog.force_kill()
            elif pressed_btn == 2: # cancel
                error_box("We'll see about that >:)")
                watchdog.crash_pc()

if __name__ == "__main__":
    hwnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hwnd, 0)
    
    watchdog_thread = threading.Thread(target=watchdog_checker, daemon=True)
    watchdog_thread.start()

    """
    bootStrapper = Bootstrapper()
    message = bootStrapper.run()
    print(message) # we use this message to display on ui
    """

    global interface
    interface = IncognitoInterface()
    interface.start()
