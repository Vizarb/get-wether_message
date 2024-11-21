import requests
from bs4 import BeautifulSoup
import pywhatkit as kit  # WhatsApp sending module

# Constants
URL = "https://www.accuweather.com/en/il/tel-aviv/215854/weather-forecast/215854"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36"}
TIMEOUT = 60  # seconds

def fetch_weather_data(url: str, headers: dict, timeout: int) -> str:
    """Fetch weather data from the AccuWeather website."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        return response.text
    except requests.Timeout:
        raise TimeoutError(f"Request timed out after {timeout} seconds.")
    except requests.RequestException as e:
        raise ConnectionError(f"An error occurred while fetching data: {e}")

def parse_weather_forecast(html: str) -> list:
    """Parse the weather forecast for the next 10 days."""
    soup = BeautifulSoup(html, "html.parser")
    forecast_data = []
    
    forecast_items = soup.find_all("a", class_="daily-list-item")
    if not forecast_items:
        raise ValueError("Failed to find forecast data on the page.")
    
    for item in forecast_items:
        day_data = {}
        
        # Extract date
        date = item.find("div", class_="date")
        if date:
            p_tags = date.find_all("p")
            day_data["day"] = p_tags[0].text.strip() if len(p_tags) > 0 else "Unknown"
            day_data["date"] = p_tags[1].text.strip() if len(p_tags) > 1 else ""
        else:
            day_data["day"] = "Unknown"
            day_data["date"] = ""
        
        # Extract temperature (high and low)
        temp = item.find("div", class_="temp")
        if temp:
            high_temp = temp.find("span", class_="temp-hi")
            low_temp = temp.find("span", class_="temp-lo")
            day_data["high_temp"] = high_temp.text.strip() if high_temp else "N/A"
            day_data["low_temp"] = low_temp.text.strip() if low_temp else "N/A"
        else:
            day_data["high_temp"] = "N/A"
            day_data["low_temp"] = "N/A"
        
        # Extract rain chance
        precip = item.find("div", class_="precip")
        rain_chance = "N/A"  # Default if no rain chance is available
        if precip:
            rain_chance_text = precip.get_text(strip=True)
            if rain_chance_text:
                rain_chance = rain_chance_text.strip()
        
        day_data["rain_chance"] = rain_chance
        
        forecast_data.append(day_data)
    
    return forecast_data

def format_forecast_for_message(forecast: list) -> str:
    """Format the weather forecast into a string for sending via WhatsApp."""
    message = "Here is the 10-day weather forecast:\n\n"
    for day_forecast in forecast:
        message += f"Date: {day_forecast['day']} {day_forecast['date']}\n"
        message += f"High Temp: {day_forecast['high_temp']} | Low Temp: {day_forecast['low_temp']}\n"
        message += f"Rain Chance: {day_forecast['rain_chance']}\n"
        message += "-" * 40 + "\n"
    return message

def send_weather_forecast_via_whatsapp(message: str, phone_number: str):
    """Send the weather forecast message via WhatsApp."""
    # Make sure to include the country code (e.g., +1 for USA)
    kit.sendwhatmsg_instantly(f"+{phone_number}", message)

def scrape_accuweather_forecast():
    """Main function to scrape AccuWeather and send the 10-day forecast via WhatsApp."""
    print("Scraping AccuWeather 10-Day Forecast...")
    
    try:
        # Fetch the weather data
        html = fetch_weather_data(URL, HEADERS, TIMEOUT)
        
        # Parse the 10-day weather forecast
        forecast = parse_weather_forecast(html)
        
        # Format the weather data into a message
        forecast_message = format_forecast_for_message(forecast)
        
        # Send the message via WhatsApp
        phone_number = "xxxxxxxxxxxxxxxxxxxx"  # Replace with the recipient's phone number
        send_weather_forecast_via_whatsapp(forecast_message, phone_number)
    
    except (TimeoutError, ConnectionError, ValueError) as e:
        # Handle different types of errors
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_accuweather_forecast()
