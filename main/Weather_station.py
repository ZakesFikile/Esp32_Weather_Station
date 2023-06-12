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


import network
import urequests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Default Wi-Fi credentials
DEFAULT_WIFI_SSID = "your_default_wifi_ssid"
DEFAULT_WIFI_PASSWORD = "your_default_wifi_password"

# OpenWeatherMap configuration
OPENWEATHER_API_KEY = "your_openweather_api_key"
CITY_NAME = "your_city_name"
OPENWEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}"

# Charger I2C address
CHARGER_I2C_ADDRESS = 0x12

# Display configuration
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

class WifiConfigServer:
    def __init__(self):
        self.ssid = DEFAULT_WIFI_SSID
        self.password = DEFAULT_WIFI_PASSWORD

    def save_config(self, ssid, password):
        self.ssid = ssid
        self.password = password
        # Save the config to a file or EEPROM

    def restart(self):
        # Restart the ESP32
        import machine
        machine.reset()

class WeatherFetcher:
    def fetch_weather_data(self):
        response = urequests.get(OPENWEATHER_API_URL)
        weather_data = response.json()
        response.close()
        return weather_data

    def get_temperature(self, weather_data):
        return round(weather_data["main"]["temp"] - 273.15, 1)

    def get_humidity(self, weather_data):
        return weather_data["main"]["humidity"]

    def get_description(self, weather_data):
        return weather_data["weather"][0]["description"]

class ChargerReader:
    def __init__(self):
        self.i2c = I2C(scl=Pin(22), sda=Pin(21))

    def fetch_charger_data(self):
        self.i2c.start()
        self.i2c.writeto(CHARGER_I2C_ADDRESS, b"\x01")
        charger_data = self.i2c.readfrom(CHARGER_I2C_ADDRESS, 4)
        self.i2c.stop()
        return charger_data

    def get_voltage(self, charger_data):
        return charger_data[0] / 10

    def get_current(self, charger_data):
        return charger_data[1] / 1000

class DisplayManager:
    def __init__(self):
        self.oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

    def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()

    def display_text(self, text, x, y):
        self.oled.text(text, x, y)
        self.oled.show()

# Initialize Wi-Fi config server
wifi_config_server = WifiConfigServer()

# Initialize weather fetcher, charger reader, and display manager
weather_fetcher = WeatherFetcher()
charger_reader = ChargerReader()
display_manager = DisplayManager()

# Check if Wi-Fi credentials are saved
if wifi_config_server.ssid == DEFAULT_WIFI_SSID and wifi_config_server.password == DEFAULT_WIFI_PASSWORD:
    display_manager.clear_screen()
    display_manager.display_text("No saved Wi-Fi", 0, 0)
    display_manager.display_text("credentials found.", 0, 16)

else:
    # Connect to Wi-Fi
    display_manager.clear_screen()
    display_manager.display_text("Connecting



