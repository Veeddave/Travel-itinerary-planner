import requests
from openai import OpenAI

client = OpenAI(api_key="")      #enter api key
openweathermap_api_key = ""  # Replace with your OpenWeatherMap API key



def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9 / 5 + 32, 2)


def get_weather_forecast(city):
    # Make a request to the OpenWeatherMap API to get the 3-hour weather forecast
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweathermap_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        # Extract relevant information from the API response
        forecast_items = weather_data.get("list", [])
        forecast_info = []
        for item in forecast_items:
            time = item['dt_txt']
            temperature = kelvin_to_fahrenheit(item['main']['temp'])
            description = item['weather'][0]['description']
            forecast_info.append(f"{time}: {temperature}°F, {description}")
        return "\n".join(forecast_info)
    else:
        return f"Failed to fetch weather information for {city}."


def plan_travel_itinerary(city, duration, interests):
    prompt = f"Plan a {duration}-day trip to {city}. Include places of interest related to {interests}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Plan a trip."},
            {"role": "assistant", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Welcome to the Travel Itinerary Planner!")

    # Assume the user immediately wants to plan a trip
    city = input("Enter the destination city: ")
    duration = input("Enter the duration of your trip (e.g., 3 days): ")
    interests = input("Enter your interests or places you'd like to visit: ")

    # Generate travel itinerary based on user input
    itinerary = plan_travel_itinerary(city, duration, interests)

    # Get the 3-hour weather forecast for the destination city
    weather_forecast = get_weather_forecast(city)

    print("\nGenerated Itinerary:")
    print(itinerary)

    print("\nWeather Forecast:")
    print(weather_forecast)

    # Start the conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        # Continue the conversation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
            ]
        )
        print("Chatbot: ", response.choices[0].message.content.strip())
