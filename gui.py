import tkinter as tk
from tkinter import ttk
from config import config
from weather_api import get_coordinates, get_weather, display_weather
from knn import knearest


def run_search(city):
    lat, lon = get_coordinates(city)
    if lat is None:
        return

    weather = get_weather(lat, lon)
    display_weather(city, weather)

    nearest = knearest(city)
    update_dropdown(nearest)


def update_dropdown(cities):
    config.input_stream.config(values=[c[1] for c in cities])


def create_gui():
    window = tk.Tk()
    config.window = window

    window.title("Weather App")

    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)

    city_var = tk.StringVar()
    config.secure = tk.StringVar(value="VA")

    ttk.Label(frame, text="City").pack()
    dropdown = ttk.Spinbox(
        frame,
        textvariable=city_var,
        values=config.sample_cities
    )
    dropdown.pack()

    config.input_stream = dropdown

    ttk.Entry(frame, textvariable=config.secure).pack()

    ttk.Button(
        frame,
        text="Search",
        command=lambda: run_search(city_var.get())
    ).pack()

    # Results
    window.temp_label = ttk.Label(frame, text="Temp")
    window.temp_label.pack()

    window.wind_label = ttk.Label(frame, text="Wind")
    window.wind_label.pack()

    window.dir_label = ttk.Label(frame, text="Dir")
    window.dir_label.pack()

    window.mainloop()