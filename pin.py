import machine
#create two UART objects for the GPS en GSM modules
gpsUART = machine.UART(1, baudrate=9600, tx=machine.Pin(18), rx=machine.Pin(19))
gsmUART = machine.UART(2, baudrate=9600, tx=machine.Pin(17), rx=machine.Pin(16))

print(gpsUART)
print(gsmUART)
