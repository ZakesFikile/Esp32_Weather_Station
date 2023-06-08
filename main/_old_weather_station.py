import network
import urequests
from machine import Pin, I2C
import framebuf
from ssd1306 import SSD1306_I2C
import time



while True:
    try:  
        # Display configuration
        SCREEN_WIDTH = 128
        SCREEN_HEIGHT = 64
        i2c = I2C(scl=Pin(22), sda=Pin(21))
        oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

        # WiFi configuration
        WIFI_SSID = "HUAWEI_E5577_25A3"
        WIFI_PASSWORD = "Zakes@2143"

        # Connect to WiFi
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            raise  Exception("Wifi not connected!!!")

        # OpenWeatherMap configuration
        WEATHER_API_KEY = "1e87f9560b5f6f7f4b89dc58a0f5d481"
        CITY_NAME = "Tokai"
        WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric"


    
    except Exception as e:
        error_message = str(e)
        print(error_message)
        oled.fill(0)
        oled.text(error_message, 0, 0)
        oled.show()

    # Fetch weather data
    response = urequests.get(WEATHER_API_URL)
    weather_data = response.json()
    print(weather_data)
    response.close()
    # print(u"\u2103")
    # print(u'\xb0')

    #Extract relevant weather information
    temperature = round(weather_data["main"]["temp"], 1)
    humidity = weather_data["main"]["humidity"]
    description = weather_data["weather"][0]["description"]

    #Display weather information on OLED screen
    oled.fill(0)
    oled.text("Temp: " + str(temperature) + "C", 0, 0)
    oled.text("Humidity: "+ str(humidity) + "%", 0, 16)
    oled.text("Wind: "+ str(humidity) + "m/s", 0, 16)
    oled.text(description.upper()+"!!!", 0, 64)
    oled.show()

    time.sleep(60)
