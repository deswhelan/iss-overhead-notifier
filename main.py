import config
import requests
from datetime import datetime

MY_LAT = config.latitude
MY_LONG = config.longitude

iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()

iss_latitude = float(iss_data["iss_position"]["latitude"])
iss_longitude = float(iss_data["iss_position"]["longitude"])

# Check if ISS position is within +- 5 degrees of user position
def iss_is_overhead(iss_latitude, iss_longitude):
    if (iss_latitude + 5 >= MY_LAT >= MY_LAT - 5) and (iss_longitude + 5 >= MY_LONG >= MY_LONG - 5):
        return True
    return False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



