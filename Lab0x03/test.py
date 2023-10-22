import pyb

vcp = pyb.USB_VCP()
vcp.isconnected()   # return true if connected as serial

def choose_cmnd(command):
    if command =='a':
        print("function a")
    elif command =='b':
        print("function b")

while True:
    if vcp.any():
        command = vcp.read(1)
        choose_cmnd(command.decode('utf-8'))

        
