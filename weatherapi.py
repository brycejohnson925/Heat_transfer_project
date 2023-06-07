import requests
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import calc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import math

n=100 #smoothness of the spline
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"

def getWeather(LATITUDE,LONGITUDE,API_KEY):
    url = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY + "&units=imperial"
    response=requests.get(url).json()

    temp = [] #Fahrenheit
    windspeed = [] #MPH
    for i in range(40):
        temp += [float(response["list"][i]["main"]["temp_min"])/2+float(response["list"][i]["main"]["temp_max"])/2]
        windspeed += [float(response["list"][i]["wind"]["speed"])]

    x = (3/24)*np.linspace(0,39,40)
    temps = calc.spline_interpolation(x,temp,n) #specify how many points to graph
    windspeeds = calc.spline_interpolation(x,windspeed,n) 
    return temps, windspeeds

def getLocation(LATITUDE,LONGITUDE,API_KEY):
    url = "http://api.openweathermap.org/geo/1.0/reverse?" + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&limit=1&appid=" + API_KEY
    response=requests.get(url).json()
    if len(response) > 0:
        return response[0]["name"]
    else:
        return "N/A"
    
def dew_point(temperature, humidity):
    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + math.log(humidity/100.0)
    dew = (b * alpha) / (a - alpha)
    return round(dew, 2)