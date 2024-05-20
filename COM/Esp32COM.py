import serial
MAX_BUFF_LEN = 255

port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

def read_serial(num_char = 1):
    str = port.read(num_char)
    return str.decode(errors='ignore')

def write_serial(cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())

while(True):
    str = read_serial(MAX_BUFF_LEN)
    print(str)

    cmd = input()
    write_serial(cmd)
