import serial, requests
from time import sleep
arduino = serial.Serial("/dev/ttyACM0", timeout=1)
from threading import Thread

import tkinter as tk

res = ''

def getUID(currv, ammv):
    while True:
        uid = arduino.readline().decode('utf-8')[1:-2]
        if uid != '':
            print(uid)
            r = requests.post('http://34.89.193.58:8080/card',
                        data = {'accountIDdest' : 'B179FG',
                                'ammount'   : int(ammv),
                                'currency'  : currv,
                                'type'      : 'groceries',
                                'uid'       : uid,
                            })
            res = r.content.decode()
            for widget in root.winfo_children():
                widget.destroy()

            label = tk.Label(root, text=res, anchor="center")
            label.pack()


def callback():
    ammv = amm.get()
    currv = curr.get()
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Please card", anchor="center")
    label.pack()

    thread = Thread(target = getUID, args = (currv, ammv))
    thread.start()
    # thread.join()

    # for widget in root.winfo_children():
    #     widget.destroy()

    # label = tk.Label(root, text=res)
    # label.pack()

root = tk.Tk()
root.resizable(False, False)
root.wm_title('POS')
root.geometry("300x150")

label = tk.Label(root, text="Ammount") # Create a text label
label.pack(fill = 'y') # Pack it into the window

amm = tk.Entry(root)
amm.pack(fill = 'y')

label = tk.Label(root, text="Currency") # Create a text label
label.pack(fill = 'y') # Pack it into the window

curr = tk.Entry(root)
curr.pack(fill = 'y')

b = tk.Button(root, text = 'OK', command = callback)
b.pack(fill = 'y')

root.mainloop()