# Wbudowane biblioteki
import time                         # czas

# Zewnetrzne biblioteki
import Adafruit_DHT                 # czytnik temperatury i wilgotnosci
import board                        # piny
import digitalio                    # sygnal cyfrowy i/o
import requests                     # requesty HTTP
import RPi.GPIO as GPIO             # GPIO na Raspberry Pi
from mfrc522 import SimpleMFRC522   # czytnik kart RFID

URL = 'https://rasp-rfid.azurewebsites.net/api/HttpTrigger2?' #Azure Funkcja

reader = SimpleMFRC522()
ledZielone = digitalio.DigitalInOut(board.D13)
ledZielone.direction = digitalio.Direction.OUTPUT
ledCzerwone = digitalio.DigitalInOut(board.D6)
ledCzerwone.direction = digitalio.Direction.OUTPUT
ledZolte = digitalio.DigitalInOut(board.D15)
ledZolte.direction = digitalio.Direction.OUTPUT

try:
    # Czytanie karty
    card_num, _ = reader.read()
    print(f"Przeczytano karte: {card_num}")

    # Czytanie temperatury i wilgotnosci
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    # HTTP request
    body = {"Nr_karty": str(card_num)}
    req = requests.post(URL, json=body)
    print(req.status_code)

    # Komunikat do uzytkownika
    ledZolte.value = True
    print(f"Temp: {temperature} C  Humidity: {humidity} %")

    # Poprawny status HTTP
    if(req.status_code == 202):
        ledZolte.value = False
        ledZielone.value = True
        print("Uzyskano dostęp")
        time.sleep(4)
        ledZielone.value = False
    
    # Niepoprawny status HTTP
    else:
        
        ledZolte.value = False
        ledCzerwone.value = True
        print("Brak dostępu")
        time.sleep(4)
        ledCzerwone.value = False

except Exception as e:
    print(f"Blad podczas czytania karty: {e}")
        
finally:
    GPIO.cleanup()
