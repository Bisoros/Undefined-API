import serial, requests

arduino = serial.Serial("/dev/ttyACM0", timeout=1)

while True:
    uid = arduino.readline().decode('utf-8')[1:-2]
    if uid != '':
        print(uid)
        r = requests.post('http://34.89.193.58:8080/card',
                    data = {'accountIDdest' : 'B179FG',
                            'ammount'   : 100000,
                            'currency'  : 'EUR',
                            'type'      : 'groceries',
                            'uid'       : '9E BB 22 209e bb 22 20',
                        })
        print(r.content.decode())
        exit()
