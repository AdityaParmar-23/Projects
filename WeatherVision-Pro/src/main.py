import customtkinter as ctk
from tkinter import messagebox

from weather_api import get_weather

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



class WeatherApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("WeatherVision Pro 🌦️")

        self.geometry("1000x750")

        self.resizable(False, False)

        self.temperature_history = []

        self.create_ui()



    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="🌦️ WeatherVision Pro",
            font=("Segoe UI",35,"bold")
        )

        title.pack(pady=20)



        self.city_entry = ctk.CTkEntry(
            self,
            width=400,
            height=45,
            placeholder_text="Enter City Name"
        )

        self.city_entry.pack(pady=10)



        ctk.CTkButton(
            self,
            text="Get Weather",
            width=250,
            height=45,
            command=self.search_weather
        ).pack(pady=10)



        self.weather_box = ctk.CTkTextbox(
            self,
            width=700,
            height=250,
            font=("Segoe UI",18)
        )

        self.weather_box.pack(pady=20)



        self.graph_frame = ctk.CTkFrame(
            self,
            width=800,
            height=300
        )

        self.graph_frame.pack(pady=20)




    def search_weather(self):

        city = self.city_entry.get().strip()


        if city == "":

            messagebox.showwarning(
                "Input Error",
                "Please enter city name"
            )

            return



        try:

            data = get_weather(city)


            # API returned nothing

            if not data:

                messagebox.showerror(
                    "Error",
                    "No data received"
                )

                return



            # API error response

            if "error" in data:

                messagebox.showerror(
                    "Weather Error",
                    data.get("error")
                )

                return



            temperature = data.get(
                "temperature",
                None
            )



            if temperature is None:

                messagebox.showerror(
                    "Error",
                    "Temperature data missing"
                )

                return



            self.temperature_history.append(
                temperature
            )


            self.display_weather(data)

            self.display_graph()



        except Exception as e:

            messagebox.showerror(
                "Application Error",
                str(e)
            )





    def display_weather(self,data):


        self.weather_box.delete(
            "0.0",
            "end"
        )



        text=f"""

📍 City:
{data.get('city','N/A')}


🌡 Temperature:
{data.get('temperature','N/A')} °C


🔥 Feels Like:
{data.get('feels','N/A')} °C


☁ Condition:
{data.get('condition','N/A')}


💧 Humidity:
{data.get('humidity','N/A')} %


💨 Wind Speed:
{data.get('wind','N/A')} m/s


Pressure:
{data.get('pressure','N/A')} hPa

"""


        self.weather_box.insert(
            "end",
            text
        )





    def display_graph(self):


        for widget in self.graph_frame.winfo_children():

            widget.destroy()



        figure,axis = plt.subplots(
            figsize=(7,3)
        )


        axis.plot(
            self.temperature_history,
            marker="o"
        )


        axis.set_title(
            "Live Temperature History"
        )


        axis.set_xlabel(
            "Search"
        )


        axis.set_ylabel(
            "Temperature °C"
        )



        canvas = FigureCanvasTkAgg(
            figure,
            self.graph_frame
        )


        canvas.draw()


        canvas.get_tk_widget().pack()





if __name__=="__main__":

    app = WeatherApp()

    app.mainloop()