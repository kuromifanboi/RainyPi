import time
import spidev
import epd7in5

# Set up GPIO and SPI
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0, 0)

# Set up the display
epd = epd7in5.EPD()
epd.init()

# Power-saving configuration
UPDATE_INTERVAL_NORMAL = 3600  # Update every hour
UPDATE_INTERVAL_POWER_SAVING = 14400  # Update every 4 hours
power_saving = False

def display_menu():
    print("Menu:")
    print("1. Display Current Weather")
    print("2. Power Saving Mode")
    print("3. Configure WiFi")
    print("4. Exit")

def set_power_saving_mode(state):
    global power_saving
    power_saving = state

def update_display(weather_data):
    temperature, humidity, weather_description = weather_data

    # Clear the display
    epd.Clear()

    # Draw weather information on the display
    epd.draw_text(50, 50, f"Temperature: {temperature}°C", epd7in5.COLORED)
    epd.draw_text(50, 100, f"Humidity: {humidity}%", epd7in5.COLORED)
    epd.draw_text(50, 150, f"Weather: {weather_description}", epd7in5.COLORED)

    # Update the display
    epd.display()
