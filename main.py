import config
import requests
import smtplib
import threading
from datetime import datetime

ALERT_CHECK_INTERVAL = 60
MY_EMAIL = config.email
MY_PASSWORD = config.password
SMTP_SERVER = config.smtp_server
RECIPIENT_EMAIL = config.recipient_email

MY_LAT = config.latitude
MY_LONG = config.longitude
IS_DARK_PARAMETERS = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

def get_current_iss_position():
    """Returns a tuple representing the current latitude/longitude of the ISS"""
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    return(iss_latitude, iss_longitude)

def iss_is_overhead(iss_position):
    """Returns a boolean representing whether or not the ISS is currently positioned within +- 5 degrees of latitude/longitude of user's location"""
    if (iss_position[0] + 5 >= MY_LAT >= MY_LAT - 5) and (iss_position[1] + 5 >= MY_LONG >= MY_LONG - 5):
        return True
    return False

def send_email_alert():
    with smtplib.SMTP(SMTP_SERVER) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL
            , to_addrs=RECIPIENT_EMAIL
            , msg="Subject: ISS is overhead NOW!"
        )

def is_dark():
    """Returns a boolean representing whether or not it is currently dark in the user's locality"""
    current_local_time = datetime.now().hour

    sunlight_response = requests.get("https://api.sunrise-sunset.org/json", params=IS_DARK_PARAMETERS)
    sunlight_response.raise_for_status()
    sunlight_data = sunlight_response.json()

    local_sunrise_time = int(sunlight_data["results"]["sunrise"].split("T")[1].split(":")[0])
    local_sunset_time = int(sunlight_data["results"]["sunset"].split("T")[1].split(":")[0])

    return not local_sunrise_time <= current_local_time < local_sunset_time

def iss_overhead_alert():
    if iss_is_overhead(get_current_iss_position()) and is_dark():
        print("ISS is overhead - sending alert!")
        send_email_alert()
    else:
        print("ISS is NOT overhead")

    # check every minute
    threading.Timer(ALERT_CHECK_INTERVAL, iss_overhead_alert).start()

iss_overhead_alert()



