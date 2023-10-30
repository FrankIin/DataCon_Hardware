from pin import gsmUART, gpsUART
import neo6m
import post
import utime
import sim800l

# Define the interval in seconds (5 minutes = 300 seconds)
interval_seconds = 60

while True:
    # Turn on power for gps module
    
    # Get coords from GPS module
    data = neo6m.main()
    
    # Check if coords has been sent
    if data is not None:
        print(data)
        # data = [GPStime, Latitude, Longitude]
        
        # after data is obtained, you can shutdown module via npn transistor to give it no power
        
        # If sim800l is connected to internet
        if sim800l.main():
            # Send coords to webserver
            post.main(data)
            
            
            # Wait 5 minutes
            utime.sleep(interval_seconds)
        else:
            print("Connection lost with sim800l module")
            
            # Try again in 10 seconds
            utime.sleep(10)        
        
    else:
        # If coords has not been found, try again in 10 seconds
        utime.sleep(10)

    



