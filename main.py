import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import weatherapi
import calc

class Grapher:
    def __init__(self, master):
        goAhead=0
        with open('stored_location.txt', 'r') as f:
            line = f.readline()
            if line:
                words = line.split(' ', maxsplit=2)
                LATITUDE = words[0]
                LONGITUDE = words[1]
                location = words[2] if len(words) > 2 else ''
                goAhead=1
            else:
                LONGITUDE = "N/A"
                LATITUDE = "N/A"
                location = "N/A"
        with open("api_key.txt", "r") as g:
            API_KEY = g.readline()

        self.master = master
        master.title("Energy Use Forecast Tool")

        # Create label and input entry for user-defined frequency
        self.latitude = tk.Label(master, text="Location latitude:")
        self.latitude.grid(row=0, column=0)
        self.lat_entry = tk.Entry(master)
        self.lat_entry.insert(0, LATITUDE)
        self.lat_entry.grid(row=0, column=1)

        self.longitude = tk.Label(master, text="Location longitude:")
        self.longitude.grid(row=1, column=0)
        self.long_entry = tk.Entry(master)
        self.long_entry.insert(0, LONGITUDE)
        self.long_entry.grid(row=1, column=1)

        self.setTemp = tk.Label(master, text="Interior set temperature (Fahrenheit)")
        self.setTemp.grid(row=2,column=0)
        self.temp_entry = tk.Entry(master)
        self.temp_entry.grid(row=2,column=1)

        self.location=tk.Label(master, text="Showing for location: " +location)
        self.location.grid(row=4,column=0,columnspan=2)
        self.displat=tk.Label(master, text="Latitude = " +LATITUDE)
        self.displat.grid(row=5,column=0,columnspan=2)
        self.displong=tk.Label(master, text="Longitude =" +LONGITUDE)
        self.displong.grid(row=6,column=0,columnspan=2)

        self.dispEnergy=tk.Label(master, text="Total Energy Used = ",font=("Arial, 20"))
        self.dispEnergy.grid(row=9,column=0,columnspan=2)

        # Create a button to generate and display the graph
        self.graph_button = tk.Button(master, text="Update", command=self.generate_graph)
        self.graph_button.grid(row=3, column=0, columnspan=2)

        # Create a figure and an axis to plot the graph on
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.plot_axis1 = self.figure.add_subplot(221)
        self.plot_axis2 = self.figure.add_subplot(222)
        self.plot_axis3 = self.figure.add_subplot(212)

        # Create a canvas to embed the graph in the GUI window
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)
        
        if goAhead == 1:
            #generate plot
            temps,windspeeds = weatherapi.getWeather(LATITUDE,LONGITUDE,API_KEY)
            self.plot_axis1.plot(temps[0],temps[1],"#f80")
            self.plot_axis1.plot([0],[0])
            self.plot_axis2.plot(windspeeds[0],windspeeds[1])
            self.plot_axis2.plot([0],[0])
            self.plot_axis3.plot([0,5],[0,0],"r--")

            # Set the plot title and axis labels
            self.plot_axis1.set_title("Temperature Forecast for the Next Five Days")
            self.plot_axis1.set_xlabel("Days")
            self.plot_axis1.set_ylabel("Temperature F")

            self.plot_axis2.set_title("Windspeed Forecast for the Next Five Days")
            self.plot_axis2.set_xlabel("Days")
            self.plot_axis2.set_ylabel("Windspeed MPH")

            # Draw the plot on the canvas
            self.canvas.draw()

    def generate_graph(self):
        with open("api_key.txt", "r") as g:
            API_KEY = g.readline()
        LATITUDE = str(self.lat_entry.get())
        LONGITUDE = str(self.long_entry.get())
        T_IN = float(self.temp_entry.get())
        
        if 90<float(LATITUDE) or -90>float(LATITUDE):
            messagebox.showinfo("Warning", "Latitude/longitude is out of range")
        elif 180<float(LONGITUDE) or -180>float(LONGITUDE):
            messagebox.showinfo("Warning", "Latitude/longitude is out of range")
        else:
            self.plot_axis1.clear()
            self.plot_axis2.clear()
            self.plot_axis3.clear()

            # generate plots
            temps,windspeeds = weatherapi.getWeather(LATITUDE,LONGITUDE,API_KEY)

            Q=[]
            for i in range(100):
                temp = calc.calcQ(T_IN,temps[1][i],windspeeds[1][i])
                if temp < 0:
                    temp = 0
                Q += [temp]
            
            total_energy=calc.midpoint_riemann_sum(86400*temps[0],Q)

            self.plot_axis1.plot(temps[0],temps[1],"#f80")
            self.plot_axis1.plot([0],[0])
            self.plot_axis2.plot(windspeeds[0],windspeeds[1])
            self.plot_axis2.plot([0],[0])
            self.plot_axis3.plot(temps[0],Q)
            self.plot_axis3.plot([0,5],[0,0],"r--")

            # Set the plot title and axis labels
            self.plot_axis1.set_title("Temperature Forecast for the Next Five Days")
            self.plot_axis1.set_xlabel("Days")
            self.plot_axis1.set_ylabel("Temperature F")

            self.plot_axis2.set_title("Windspeed Forecast for the Next Five Days")
            self.plot_axis2.set_xlabel("Days")
            self.plot_axis2.set_ylabel("Windspeed MPH")

            self.plot_axis3.set_title("Energy Use Forecast for the Next Five Days")
            self.plot_axis3.set_xlabel("Days")
            self.plot_axis3.set_ylabel("Energy Use in Kilowatts")
            
            # Draw the plot on the canvas
            self.canvas.draw()
            
            # Update text labels
            location = weatherapi.getLocation(LATITUDE,LONGITUDE,API_KEY)
            self.location.configure(text="Showing for location: "+ location)
            self.displat.configure(text="Latitude = "+ LATITUDE)
            self.displong.configure(text="Longitude = "+ LONGITUDE)
            total_fuel=round(total_energy*9.08/1000000,2)
            total_energy=round(total_energy/1000000,2)
            self.dispEnergy.configure(text="Total Energy Used = "+str(total_energy)+" GJ"+" ~= " + str(total_fuel)+" gallons fuel")

            # Store inputs to txt file
            with open('stored_location.txt', 'w') as f:
                f.write(LATITUDE+" "+LONGITUDE+" "+location)

# Create the main GUI window
root = tk.Tk()
grapher = Grapher(root)
root.mainloop()
