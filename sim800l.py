# Import UART connection for sim800l module
from pin import gsmUART
import utime

# Variable to check connection
access = True

# Function to send AT commands and read responses
def send_at_command(command):
    gsmUART.write(command + b'\r\n')
    utime.sleep_ms(500) 
    response = gsmUART.read(gsmUART.any())
    print(response)
    return response

def main():
    global access
    # Check if SIM800L is responsive
    gsmUART.read()
    response = send_at_command(b'AT')
    if b'OK' in response:
        print("SIM800L is responsive")
    else:
        print("SIM800L is not responsive")
        access = False

    # Check if SIM800L is registered on the network
    response = send_at_command(b'AT+CREG?')
    if b'+CREG: 0,1' in response or b'+CREG: 0,5' in response:
        print("SIM800L is registered on the network")
    else:
        print("SIM800L is not registered on the network")
        access = False

    # Get battery status
    response = send_at_command(b'AT+CBC')
    if b'+CBC:' in response:
        battery_status = response.decode('utf-8').split(':')[-1].strip()
        print("Battery Status:", battery_status)
    else:
        print("Failed to retrieve battery status")
        
    return access

