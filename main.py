import time
import RPi.GPIO as GPIO
import weather
import display
import gps
import wifi

# Button GPIO pins
RESET_PIN = 17
UP_PIN = 27
DOWN_PIN = 22
POWER_PIN = 23

# Button debounce time (in seconds)
DEBOUNCE_TIME = 0.2

def handle_reset(channel):
    print("Resetting the Raspberry Pi...")
    time.sleep(1)
    GPIO.cleanup()
    subprocess.call("sudo reboot", shell=True)

def handle_up(channel):
    print("Up button pressed")

def handle_down(channel):
    print("Down button pressed")

def handle_power(channel):
    if GPIO.input(POWER_PIN) == GPIO.HIGH:
        print("Power button released")
        # Perform the action for power button release
    else:
        print("Power button pressed")
        # Perform the action for power button press

def handle_wifi_config():
    wifi.handle_wifi_config()

def setup_buttons():
    GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(POWER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(RESET_PIN, GPIO.FALLING, callback=handle_reset, bouncetime=int(DEBOUNCE_TIME * 1000))
    GPIO.add_event_detect(UP_PIN, GPIO.FALLING, callback=handle_up, bouncetime=int(DEBOUNCE_TIME * 1000))
    GPIO.add_event_detect(DOWN_PIN, GPIO.FALLING, callback=handle_down, bouncetime=int(DEBOUNCE_TIME * 1000))
    GPIO.add_event_detect(POWER_PIN, GPIO.BOTH, callback=handle_power, bouncetime=int(DEBOUNCE_TIME * 1000))

def main():
    try:
        # Initialize GPIO buttons
        setup_buttons()

        while True:
            display.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                latitude, longitude = gps.get_current_location()
                weather_data = weather.get_weather_data(latitude, longitude)

                if weather_data is not None:
                    display.update_display(weather_data)

                if display.power_saving:
                    time.sleep(display.UPDATE_INTERVAL_POWER_SAVING)
                else:
                    time.sleep(display.UPDATE_INTERVAL_NORMAL)

            elif choice == "2":
                if display.power_saving:
                    print("Power saving mode is already enabled.")
                else:
                    print("Enabling power saving mode...")
                    display.set_power_saving_mode(True)

            elif choice == "3":
                handle_wifi_config()

            elif choice == "4":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        display.epd7in5.epdconfig.module_exit()
        display.spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
