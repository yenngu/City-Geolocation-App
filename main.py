import requests
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
import folium
import webbrowser
import os

# Create Tkinter Window
window = Tk()
window.geometry('400x600') # Size
window.resizable(0, 0) # Set resizable attributes to False
window.title('City Information App') # Set Title 

# Font
textFont = tkFont.Font(family="Helvetica", size=15)

# Weather API Key
weather_api_key = '4dd8ce4b8ee5495711f5357291c89527'

# List for showing cities
city_options = []

# Variable to select city
selected_result = None

# Function to get Lat, Lon coordinates for a city 
def get_coords(city):
    global city_options 
    city_options = [] 
    
    # API Url for geolocation api
    url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=30&language=en&format=json'
    geo_response = requests.get(url) # get response from API
    geo_data = geo_response.json() # Store data in Json format

    # Grab certain data points from json
    if 'results' in geo_data and len(geo_data['results']) > 0:
        for result in geo_data['results']:
            city_name = result.get('name')
            country = result.get('country')
            latitude = result.get('latitude')
            longitude = result.get('longitude')
            elevation = result.get('elevation')
            
            # Append to city options list
            city_options.append((city_name, country, latitude, longitude, elevation))  
        
        # Display to listbox    
        display_city_options() 
    else:
        # If no city is found, clear listbox and tell user to enter a valid city
        listbox.delete(0, END)
        listbox.insert(END, "Result not Found, Enter Valid City")

# Function to display city options to listbox
def display_city_options():
    listbox.delete(0, END)
    for i, (city_name, country, lat, lon, elev) in enumerate(city_options):
        listbox.insert(END, f"{city_name}, {country}")
# Function to select city from listbox
def city_selected(event):
    global selected_result
    index = listbox.curselection()
    if index:
        selected_result = city_options[index[0]]
        show_city_details_screen() # Call show_city_details_screen function to bring user to next screen

# Function to show information about selected city
def show_city_details_screen():
    clear_screen()
    city_name, country, lat, lon, elev = selected_result
    
    # Create section to show information
    location_frame = Frame(window,
                           bg='#e0f7fa')
    location_frame.pack(pady=20,
                        padx=20)

    city_label = Label(location_frame,
                       text=f"City: {city_name},{country}",
                       font=(textFont, 15, 'bold'),
                       bg='#e0f7fa')
    city_label.pack(pady=10)
    
    coords_label = Label(location_frame,
                         text=f"Latitude: {lat}\n Longitude: {lon}\n Elevation: {elev}\n",
                         font=(textFont, 8, 'bold'),
                         bg='#e0f7fa')
    coords_label.pack(pady=10)
    
    weather_label = Label(location_frame,
                          text=f"Weather: {get_weather(lat, lon)}\n",
                          font=(textFont, 8, 'bold'),
                          bg='#e0f7fa')
    weather_label.pack(pady=10)

    map_button = Button(location_frame, 
                        text="Show Map", 
                        command=lambda: create_map(lat, lon, city_name),
                        font=(textFont, 8),
                        bg='lightblue', 
                        relief=FLAT)
    map_button.pack(pady=10)

    back_button = Button(location_frame,
                         text="Back",
                         command=return_to_search,
                         font=(textFont),
                         bg='lightblue',
                         relief=FLAT)
    back_button.pack(pady=10)

# Function to get weather details based on latitude and longitude input
def get_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric'
    weather_response = requests.get(url) # Request response from url
    weather_data = weather_response.json() # Store response in a json data format

    if weather_data.get('weather'):
        weather_desc = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        
        return f"Temperature: {temp}°C\n Feels Like: {feels_like}°C\n Humidity: {humidity}%\n Description: {weather_desc}" 
    else:
        return "Can't get weather information"

# Function that utilizes folium module to generate a map based on lat, lon, and name of city
def create_map(lat, lon, city_name):
    city_map = folium.Map(location=[lat, lon], zoom_start=12) # Center location to latitude and longtitude and zoom in
    folium.Marker([lat, lon], popup=city_name).add_to(city_map) # Place marker on latitude and longtitude

    map_file = f"{city_name}_map.html" # Name File
    city_map.save(map_file) # Save map to file
    webbrowser.open('file://' + os.path.realpath(map_file)) # Open File in Web

def clear_screen():
    for item in window.winfo_children(): # For loop to go through each item
        item.pack_forget() # Clear items

def return_to_search():
    clear_screen() # Clear items
    app() # Call App Function (Home Screen)

def app():
    global background_image, titleLabel, cityEntry, listbox, scrollbar
    
    # Open Background Image
    try:
        image = Image.open("city.jpg")
        background_image = ImageTk.PhotoImage(image)
    
        background = Label(window,
                           image=background_image)
        background.place(relwidth=1,
                         relheight=1)
        
    except Exception as e:
        print(f'Error Loading Background Image: {e}')
    
    # Title Label    
    titleLabel = Label(window,
                       text=f'City Demographics',
                       font=(textFont, 25), 
                       bg='white')
    titleLabel.pack(pady=20)
    
    # Create a section on window frame
    global cityFrame
    cityFrame = Frame(window,
                      bg='lightgrey')
    cityFrame.pack(pady=20)

    # Label to inform user to input a city
    cityLabel = Label(cityFrame,
                      text='Enter a City: ', 
                      font=(textFont),
                      bg='lightgrey')
    cityLabel.grid(row=0,
                   column=0,
                   padx=5)
    
    # City Input Box
    global cityEntry
    cityEntry = Entry(cityFrame,
                      font=(textFont, 12))
    cityEntry.grid(row=0,
                   column=1,
                   padx=5)
    
    # Search Button
    searchButton = Button(cityFrame, 
                          text="Search", 
                          command=lambda: get_coords(cityEntry.get()), 
                          font=(textFont),
                          bg='lightblue',
                          relief=FLAT)
    searchButton.grid(row=1,
                      column=0, 
                      columnspan=2,
                      pady=10)
    
    # Listbox to store cities
    listbox_frame = Frame(window)
    listbox_frame.pack(pady=10)

    global listbox
    listbox = Listbox(listbox_frame,
                      height=10,
                      width=30,
                      font=(textFont),
                      bg='#ffffff', 
                      selectmode=SINGLE)
    
    listbox.pack(side=LEFT,
                 fill=BOTH)

    # Scroll bar for listbox
    scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side=RIGHT,
                   fill=Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox.bind("<Double-Button-1>", city_selected) # Double click to show more information on city

app() # Call App
window.mainloop() 
