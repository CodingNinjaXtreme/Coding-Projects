import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io


def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    api_key = "YOUR_API_KEY"  # Replace it with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", data.get("message", "City not found."))
            return

        # Weather data
        city_name = data['name']
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Weather icon
        icon_id = data['weather'][0]['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@4x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        # Update GUI card
        weather_icon_label.config(image=icon_photo)
        weather_icon_label.image = icon_photo
        weather_info_label.config(
            text=f"{city_name}\n"
                 f"{temp}°C, {desc}\n"
                 f"💧 Humidity: {humidity}%\n"
                 f"🌬 Wind: {wind_speed} m/s"
        )

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"An error occurred: {e}")


# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("320x400")
root.config(bg="#1e1e2f")

# Title
tk.Label(root, text="Weather App", bg="#1e1e2f", fg="white",
         font=("Helvetica", 18, "bold")).pack(pady=10)

# City input
city_entry = tk.Entry(root, width=20, font=("Arial", 14), bg="white", fg="black", justify="center")
city_entry.pack(pady=8)

# Button
tk.Button(root, text="Get Weather", command=get_weather,
          font=("Arial", 12, "bold"), bg="#4a90e2", fg="black",
          relief="flat", padx=10, pady=5).pack(pady=10)

# Card frame
card_frame = tk.Frame(root, bg="#2a2a3d", bd=0, relief="flat")
card_frame.pack(pady=15, padx=10, fill="both", expand=True)

weather_icon_label = tk.Label(card_frame, bg="#2a2a3d")
weather_icon_label.pack(pady=5)

weather_info_label = tk.Label(card_frame, bg="#2a2a3d", fg="white", font=("Arial", 14))
weather_info_label.pack(pady=5)

root.mainloop()
