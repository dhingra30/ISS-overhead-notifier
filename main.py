import requests
import datetime as dt
import smtplib

MY_LAT = 28.658340
MY_LONG = 77.085470
MY_EMAIL = 'rahuldhingraajd@gmail.com'
MY_PASS = 'xcbjwfvrioofdazw'


def iss_coordinates():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    coordinates_data = response.json()
    iss_lat = float(coordinates_data['iss_position']['latitude'])
    iss_long = float(coordinates_data['iss_position']['longitude'])
    return iss_lat, iss_long


def sunrise_sunset():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
        'tzid': 'Asia/Kolkata',
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_time = (data['results']['sunrise'].split('T'))[1].split('+')[0]
    sunset_time = (data['results']['sunset'].split('T'))[1].split('+')[0]
    return sunrise_time, sunset_time


def send_mail():
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: ISS above you \n\n Look up")
    print("User informed about the location of International Space Station")


def is_near():
    iss_lat, iss_long = iss_coordinates()
    if (MY_LAT - 5) <= iss_lat <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_long <= (MY_LONG + 5):
        return True
    else:
        return False


present_day = dt.datetime.now()
current_time = str(present_day.time())
time_in_format = current_time.split('.')
sunrise, sunset = sunrise_sunset()

iss_above = is_near()

if iss_above and sunset <= time_in_format <= sunrise:
    send_mail()
