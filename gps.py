import subprocess
from gps import *

uart = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout=1)
gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

def get_current_location():
    while True:
        try:
            # Read GPS data
            report = gpsd.next()

            if report['class'] == 'TPV':
                if hasattr(report, 'lat') and hasattr(report, 'lon'):
                    latitude = report.lat
                    longitude = report.lon

                    return latitude, longitude

        except KeyboardInterrupt:
            break
        except Exception as e:
            print('GPS Error:', str(e))
            continue
