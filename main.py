# Código por Diego Eduardo Flores Sandoval
# https://github.com/LaloFl                         
                                                   
#                        ,,                      ,,  
# `7MMF'               `7MM         `7MM"""YMM `7MM  
#   MM                   MM           MM    `7   MM  
#   MM         ,6"Yb.    MM  ,pW"Wq.  MM   d     MM  
#   MM        8)   MM    MM 6W'   `Wb MM""MM     MM  
#   MM      ,  ,pm9MM    MM 8M     M8 MM   Y     MM  
#   MM     ,M 8M   MM    MM YA.   ,A9 MM         MM  
# .JMMmmmmMMM `Moo9^Yo..JMML.`Ybmd9'.JMML.     .JMML.
                                                 
import machine, ssd1306, utime, network, socket

# Conexión con OLED
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def autoOLEDWrite(text):
    text = text.replace('\xf3', 'o')
    text = text.replace('\xed', 'i')
    text = text.replace('\xe1', 'a')
    text = text.replace('\xe9', 'e')
    text = text.replace('\xfa', 'u')
    text = text.replace('\xf1', 'ni')
    text = text.replace('\xc1', 'A')
    text = text.replace('\xc9', 'E')
    text = text.replace('\xcd', 'I')
    text = text.replace('\xd3', 'O')
    text = text.replace('\xda', 'U')
    text = text.replace('\xd1', 'Ni')
    text = text.replace('\n', '')

    step = 0
    for i in range(len(text)):
        step += 1 if (i % 15 == 0 and i != 0) else 0
        oled.text(text[i], (i%15)*8, step*11)
        # if (i % 15 == 0 and i != 0):
        #     oled.text(text[:((i%15)*step)], 0, step*10)
        #     step += 1

# LED
led = machine.Pin("LED", machine.Pin.OUT)

# Conextión a WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Totalplay-6FA5","paldy969900")
ip=""
# Wait for connect or fail
while not (wlan.status() < 0 or wlan.status() >= 3):
    print('waiting for connection...')
    oled.fill(0)
    autoOLEDWrite("Waiting for\nConnection")
    oled.show()
    utime.sleep_ms(50)
    utime.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    ip=wlan.ifconfig()[0]
    print('Connection successful')
    print('IP:', ip)
    oled.fill(0)
    oled.text("Conencted: ", 0, 0)
    oled.text("IP: "+ip, 0, 10)
    oled.show()


def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
        if request == '/':
            for i in range(5):
                led.value(1)
                utime.sleep_ms(50)
                led.value(0)
                utime.sleep_ms(50)

# Open a socket
address = (ip, 80)
connection = socket.socket()
connection.bind(address)
connection.listen(1)
serve(connection)
