# Weather Forecast Project

This project aims to scrape the 10-day weather forecast from AccuWeather and send it to a recipient via WhatsApp.

## Features

* Scrapes weather data from AccuWeather using BeautifulSoup and requests
* Formats the weather data into a string for sending via WhatsApp
* Sends the weather forecast message via WhatsApp using pywhatkit

## Requirements

* Python 3.x
* requests
* BeautifulSoup
* pywhatkit

## Usage

1. Install the required libraries by running `pip install -r requirements.txt`
2. Replace the `phone_number` variable in `wether_to_me.py` with the recipient's phone number
3. Run the script by executing `python wether_to_me.py`

## Notes

* Make sure to include the country code (e.g., +1 for USA) in the phone number
* The script uses a timeout of 60 seconds to fetch the weather data. You can adjust this value.