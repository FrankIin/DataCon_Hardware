#GPS 	ESP32
#GND	GND
#TX 	D19
#RX 	D18
#VCC	VIN

#GSM	ESP32
#GND	BreadboardGND & BatteryGND
#TX 	RX2
#RX 	Breadboard -> 1k -> TX2 -> 4.6k -> 1k -> GND
#VCC	BatteryVCC

#boot.py is to perform board-specific initialization and configuration tasks

#import UART connections
from pin import gpsUART
import ustruct
import utime

#configure the GPS module so that all NMEA sentences are deactivated
gpsUART.write('$PUBX,40,GGA,0,0,0,0*5A\r\n')
utime.sleep_ms(100)
gpsUART.write('$PUBX,40,GLL,0,0,0,0*5C\r\n')
utime.sleep_ms(100)
gpsUART.write('$PUBX,40,GSA,0,0,0,0*4E\r\n')
utime.sleep_ms(100)
gpsUART.write('$PUBX,40,GSV,0,0,0,0*59\r\n')
utime.sleep_ms(100)
gpsUART.write('$PUBX,40,RMC,0,0,0,0*47\r\n')
utime.sleep_ms(100)
gpsUART.write('$PUBX,40,VTG,0,0,0,0*5E\r\n')
utime.sleep_ms(100)
print ('NMEA sentences deactivated')

# Calculate the update rate in milliseconds (5 minutes = 300,000 ms)
update_rate_ms = 300000

# Convert the update rate to little-endian bytes (4 bytes)
update_rate_bytes = ustruct.pack('<I', update_rate_ms)

# UBX-CFG-CFG message payload to enable ON/OFF power save mode, set update rate, and turn off cyclic tracking
payload = bytearray([
    0x06, 0x09,  # Message class and ID for UBX-CFG-CFG
    0x00, 0x00,  # No bit flags set
    0x00, 0x00, 0x00, 0x00,  # Clear masks
    0x01, 0x00,  # Save changes to permanent configuration
    0x01, 0x00,  # Set the update rate dynamic
    update_rate_bytes[0], update_rate_bytes[1], update_rate_bytes[2], update_rate_bytes[3],  # Update rate in milliseconds
    0x00, 0x00, 0x00, 0x00,  # No cyclic tracking
])

# UBX message structure: Sync characters, class, ID, payload length, payload, checksum
message = bytearray(b'\xB5\x62\x06\x09' + ustruct.pack('<H', len(payload)) + payload)
message += ustruct.pack('<H', sum(message[-len(payload):]) & 0xFFFF)

# Send the message to the NEO-6M module
gpsUART.write(message)

# Send the UBX-CFG-CFG/SAVE command to save the configuration to permanent memory
save_command = bytearray(b'\xB5\x62\x06\x09\x0D\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
gpsUART.write(save_command)


