import requests
from tkinter import Tk, StringVar, Entry, Button, Label, messagebox, Frame
from PIL import Image, ImageTk
import io

# Constants
API_KEY = "4450649825b5fee22f5bb1d2f35d6714"
URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def get_weather(city):
    """Fetch weather details from the OpenWeather API."""
    try:
        response = requests.get(URL.format(city, API_KEY))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        city_name = data['name']
        country = data['sys']['country']
        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_celsius * 9/5) + 32
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']

        # Fetch weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))

        return {
            "city": city_name,
            "country": country,
            "temp_celsius": round(temp_celsius, 2),
            "temp_fahrenheit": round(temp_fahrenheit, 2),
            "weather_desc": weather_desc.capitalize(),
            "humidity": humidity,
            "wind_speed": wind_speed,
            "icon_image": icon_image
        }
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except KeyError:
        print("Unexpected data format received.")
        return None

def search():
    """Handle the search button click event."""
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl.config(text=f"{weather['city']}, {weather['country']}")
        temperature_label.config(text=f"{weather['temp_celsius']} °C / {weather['temp_fahrenheit']} °F")
        weather_l.config(text=f"Weather: {weather['weather_desc']}")
        humidity_l.config(text=f"Humidity: {weather['humidity']}%")
        wind_l.config(text=f"Wind Speed: {weather['wind_speed']} m/s")
        
        # Update the weather icon
        weather_icon = ImageTk.PhotoImage(weather['icon_image'])
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon
    else:
        messagebox.showerror('Error', f"Cannot find weather information for '{city}'.")

def clear():
    """Clear the input and output fields."""
    city_text.set("")
    location_lbl.config(text="Location")
    temperature_label.config(text="")
    weather_l.config(text="")
    humidity_l.config(text="")
    wind_l.config(text="")
    icon_label.config(image="")

# Main Application
app = Tk()
app.title("Weather App")
app.geometry("475x500")
app.config(bg='#87CEEB')

# Create a frame for better layout control
main_frame = Frame(app, bg='#87CEEB')
main_frame.pack(padx=20, pady=20, fill='both', expand=True)

# UI Elements
city_text = StringVar()
city_entry = Entry(main_frame, textvariable=city_text, width=30, font=('Arial', 14))
city_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

search_btn = Button(main_frame, text="Search Weather", width=20, command=search, font=('Arial', 12))
search_btn.grid(row=1, column=0, padx=10, pady=10)

clear_btn = Button(main_frame, text="Clear", width=20, command=clear, font=('Arial', 12))
clear_btn.grid(row=1, column=1, padx=10, pady=10)

icon_label = Label(main_frame, bg='#87CEEB')
icon_label.grid(row=2, column=0, columnspan=2, pady=10)

location_lbl = Label(main_frame, text="Location", font=('Arial', 18, 'bold'), bg='#87CEEB')
location_lbl.grid(row=3, column=0, columnspan=2, pady=5)

temperature_label = Label(main_frame, text="", font=('Arial', 16), bg='#87CEEB')
temperature_label.grid(row=4, column=0, columnspan=2, pady=5)

weather_l = Label(main_frame, text="", font=('Arial', 14), bg='#87CEEB')
weather_l.grid(row=5, column=0, columnspan=2, pady=5)

humidity_l = Label(main_frame, text="", font=('Arial', 14), bg='#87CEEB')
humidity_l.grid(row=6, column=0, columnspan=2, pady=5)

wind_l = Label(main_frame, text="", font=('Arial', 14), bg='#87CEEB')
wind_l.grid(row=7, column=0, columnspan=2, pady=5)

app.mainloop()
