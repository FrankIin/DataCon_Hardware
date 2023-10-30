# Import UART connection to GPS module
from pin import gpsUART
import utime, time

# Define variable if error occurs
TIMEOUT = False
FIX_STATUS = False

# Variables to save data
latitude = ""
longitude = ""
satellites = ""
GPStime = ""

# Function to retrieve the coords from module
def getGPS():
    # Let this function make use of the variable defined above
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    # Timeout after 8 seconds
    timeout = time.time() + 8 
    while True:
        
        # Enable GPGGA NMEA Sentence for coords
        gpsUART.write('$PUBX,40,GGA,1,1,0,0,0,0*5A\r\n')
        
        # Wait one second
        utime.sleep(1)
        
        # Read GPGGA NMEA Sentence and split with comma
        buff = str(gpsUART.readline())
        parts = buff.split(',')
    
        # Retrieve the Latitude, Longitude, GPSTime and amount of sattelites
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = '-' + latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = '-' + longitude
                satellites = parts[7]
                GPStime = str((int(parts[1][0:2]) + 1)) + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                
                # Turn off NMEA Sentence
                gpsUART.write('$PUBX,40,GGA,0,0,0,0*5A\r\n')
                break
        
        # If GPGGA Sentence has not been found
        if (time.time() > timeout):
            TIMEOUT = True
            break
        
        # Wait one second if GPGGA Sentence has not been found
        utime.sleep(1)
        
# Function to convert GPGGA data to useable coordinates        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

# Main function that is being called and returns coords
def main():
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    # Retrieve data
    getGPS()
    
    # If data has been found
    if(FIX_STATUS == True):
        FIX_STATUS = False
        return (GPStime,latitude,longitude)
    
    # If data has not beed found    
    if(TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False
        return None
    
    




