import network
import urequests
import uasyncio as asyncio
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import ujson
import uos

# Default WiFi configuration
DEFAULT_WIFI_SSID = "your_default_wifi_ssid"
DEFAULT_WIFI_PASSWORD = "your_default_wifi_password"

# Configuration file
CONFIG_FILE = "config.json"

# OpenWeatherMap configuration
WEATHER_API_KEY = "your_weather_api_key"
CITY_NAME = "Cape Town"
WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}"

# Display configuration
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

class WeatherMonitor:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
        self.oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, self.i2c)
        self.temperature = 0

    def connect_wifi(self, ssid, password):
        self.wifi.active(True)
        self.wifi.connect(ssid, password)
        while not self.wifi.isconnected():
            pass

    def fetch_weather_data(self):
        response = urequests.get(WEATHER_API_URL)
        weather_data = response.json()
        response.close()

        temperature = round(weather_data["main"]["temp"] - 273.15, 1)
        self.temperature = temperature

    def update_display(self):
        self.oled.fill(0)
        self.oled.text("Temperature:", 0, 0)
        self.oled.text(str(self.temperature) + "C", 0, 16)
        self.oled.show()

    async def monitor_loop(self):
        while True:
            self.fetch_weather_data()
            self.update_display()
            await asyncio.sleep(10)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        ujson.dump(config, file)

def load_config():
    if CONFIG_FILE in uos.listdir():
        with open(CONFIG_FILE, "r") as file:
            return ujson.load(file)
    else:
        return None

def get_wifi_credentials():
    ssid = input("Enter Wi-Fi SSID: ")
    password = input("Enter Wi-Fi password: ")
    return ssid, password

def main():
    config = load_config()

    if config is None:
        print("No saved Wi-Fi credentials found.")
        ssid, password = get_wifi_credentials()
        config = {"wifi_ssid": ssid, "wifi_password": password}
        save_config(config)
    else:
        ssid = config["wifi_ssid"]
        password = config["wifi_password"]

    monitor = WeatherMonitor()
    monitor.connect_wifi(ssid, password)

    loop = asyncio.get_event_loop()
    loop.create_task(monitor.monitor_loop())
    loop.run_forever()

if __name__ == "__main__":
    main()


