import os
import subprocess
import time
from flask import Flask
import psutil
from pyinjector import inject
from pynput.keyboard import Key, Controller

app = Flask(__name__)
steam = r"C:\Program Files (x86)\Steam\steam.exe"
dll_to_inject = "botfware.dll"
tf2_exe = r"C:\Program Files (x86)\Steam\steam.exe -applaunch 440 -silent -sw -w 640 -h 480 -novid -nojoy -noshaderapi -nomouse -nomessagebox -nominidumps -nohltv -nobreakpad -particles 512 -snoforceformat -softparticlesdefaultoff -steam"
bypass = "steambypassloader.exe"
steamrunning = False
keyboard = Controller()


def launch_program(program_path):
    subprocess.run(program_path)


def close(program_path):
    subprocess.run(program_path)


def vacbypass():
    subprocess.run(['vacbypass.bat'])


def is_tf2_running():
    return any(process.info['name'] == 'hl2.exe' for process in psutil.process_iter(['name']))


def launch_tf2_and_inject():
    while True:
        if not is_tf2_running():
            launch_program(tf2_exe)
            time.sleep(5)  # Reduce the sleep time here
        else:
            tf2_pids = [process.pid for process in psutil.process_iter(['name']) if process.info['name'] == 'hl2.exe']
            if tf2_pids:
                try:
                    for pid in tf2_pids:
                        inject(pid, dll_to_inject)
                except Exception as e:
                    print(f"DLL injection failed: {str(e)}")

        time.sleep(0.5)  # Reduce the sleep time here


if __name__ == "__main__":
    Thread(target=vacbypass).start()
    time.sleep(25)
    keyboard.press(Key.enter)
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'steam.exe':
            steamrunning = True
            time.sleep(15)
            launch_tf2_and_inject()
        else:
            steamrunning = False
            subprocess.run(tf2_exe, shell=True)
