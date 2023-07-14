import os
import subprocess
import time
from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import psutil
import ctypes, sys
from pyinjector import inject
import pyinput
from pynput.keyboard import Key, Controller

app = Flask(__name__)
steam = "C:\Program Files (x86)\Steam\steam.exe"
dll_to_inject = "botfware.dll"
tf2_exe = "C:\Program Files (x86)\Steam\steam.exe -applaunch 440 -silent -sw -w 640 -h 480 -novid -nojoy -noshaderapi -nomouse -nomessagebox -nominidumps -nohltv -nobreakpad -particles 512 -snoforceformat -softparticlesdefaultoff -steam"
bypass = "steambypassloader.exe"
steamrunning = False
keyboard = Controller()


def launch_program(program_path):
    subprocess.Popen(program_path)

def close(program_path):
    p = subprocess.Popen(program_path)
    p.terminate()

def vacbypass():
    subprocess.Popen(['vacbypass.bat'])


def is_tf2_running():
    for process in psutil.process_iter(['name', 'exe']):
        if process.info['name'] == 'hl2.exe' in process.info['exe']:
            return True
    return False

def launch_tf2_and_inject():
    while True:
        if not is_tf2_running():
            launch_program(tf2_exe)
            time.sleep(10)
        else:
            tf2_pids = []
            for process in psutil.process_iter(['name', 'exe']):
                if process.info['name'] == 'hl2.exe' in process.info['exe']:
                    tf2_pids.append(process.pid)

            if tf2_pids:
                try:
                    for pid in tf2_pids:
                        inject(pid, dll_to_inject)
                except Exception as e:
                    print(f"DLL injection failed: {str(e)}")

        time.sleep(1)

vacbypass()
time.sleep(25)
keyboard.press(Key.enter)
for process in psutil.process_iter(['name', 'exe']):
        if process.info['name'] == 'steam.exe' in process.info['exe']:
            steamrunning = True
            time.sleep(15)
            launch_tf2_and_inject()
        else:
            steamrunning = False
            p = subprocess.Popen(tf2_exe)
            p.terminate()



