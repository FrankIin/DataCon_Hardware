import utime
from pin import gsmUART
import ujson

# Define the URL of the HTTP endpoint
url = "https://atlantic-shard-bream.glitch.me/data/add"

# Create a function to send the HTTP POST request
def send_http_post_request(data, url):
    success = True
    # JSON data to send in the POST request
    json_data = {
        "tracker_id": 1,
        "lat": data[1],
        "long": data[2]
    }
    # Convert the JSON data to a string
    json_payload = ujson.dumps(json_data)
    try:
        # Acknowledge connection to sim800l
        gsmUART.write('AT\r\n')   
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Connection to sim800l has failed.")
        
        # Set sim800l to GPRS mode
        gsmUART.write('AT+SAPBR=3,1,\"Contype\",\"GPRS\"\r\n')
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed setting GPRS mode")
        
        # Set APN to 'internet' for Simyo
        gsmUART.write('AT+SAPBR=3,1,\"APN\",\"internet\"\r\n')
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed setting APN")
        
        # Check if the module is registered
        gsmUART.write(b'AT+CREG?\r\n')
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to register")
        
        # Establish GPRS connection
        gsmUART.write('AT+SAPBR=1,1\r\n')
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to establish connection")
        
        # Wait for GPRS to be active
        while True:
            gsmUART.write('AT+SAPBR=2,1\r\n')
            utime.sleep_ms(1000)
            response = gsmUART.read()
            print(response)
            if "1,1," in response:
                break
            
        # Initialize HTTP session
        gsmUART.write("AT+HTTPINIT\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print(response)
            print("Failed to initialize HTTP")
        
        # Set the HTTP context ID
        gsmUART.write("AT+HTTPPARA=\"CID\",1\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to set context ID")
        
        # Set the URL
        gsmUART.write("AT+HTTPPARA=\"URL\",\"" + url + "\"\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        print(response)
        if "OK" not in response:
            print("Failed to set URL")
        
        # Set the HTTP content type and content length
        gsmUART.write("AT+HTTPPARA=\"CONTENT\",\"application/json\"\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to set content type")
            
        
        # Enable SSL for HTTP communication
        gsmUART.write("AT+HTTPSSL=1\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to enable SSL")
        
        # Specify the data length and timeout
        gsmUART.write("AT+HTTPDATA=" + str(len(json_payload)) + ",100000\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        
        # Send the JSON data
        gsmUART.write(json_payload)
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to send JSON data")
        
        # Perform HTTP POST request
        gsmUART.write("AT+HTTPACTION=1\r\n")
        utime.sleep(10)  # Wait for the response
        response = gsmUART.read()
        if "20" not in response:
            print("Failed to send message")
            print(response)
            success = False
        else:
            print("Message send")
            
        # Read the response
        gsmUART.write("AT+HTTPREAD\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to read response")  
        
        # Close the HTTP session
        gsmUART.write("AT+HTTPTERM\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to close HTTP session")
        
        # Close the GPRS connection
        gsmUART.write("AT+SAPBR=0,1\r\n")
        utime.sleep_ms(1000)
        response = gsmUART.read()
        if "OK" not in response:
            print("Failed to close GPRS connection")
        
        return success
    except Exception as e:
        print("Error:", e)
        return None

def main(data):
    # Send the HTTP POST request
    respond = False
    counter = 0
    while (respond == False):
        respond = send_http_post_request(data, url)
        if (respond == False):
            print("Retry...")
            counter = counter + 1
        if (counter == 5):
            print("Message not been able to send")
            break

