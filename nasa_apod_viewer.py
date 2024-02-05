import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import ttk
from datetime import datetime

api_key = input("enter api key: ")
root = tk.Tk()
root.geometry("800x600")

label = tk.Label(root, text="NASA Astronomy Picture of the Day:")
label.pack()

# function to get today's picture
def get_today_picture():
    image_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(image_url)     
    if response.status_code == 200:
        data = response.json()
        img_url = data.get("url")  # Extract the image URL
        if img_url:
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_data = img_response.content
                image = Image.open(BytesIO(img_data))
                photo = ImageTk.PhotoImage(image=image)
                image_label.config(image=photo)
                image_label.image = photo
         
# allows only dates with images to be selected      
def is_valid_date(year, month, day):
    current_date = datetime.now()
    selected_date = datetime(int(year), months.index(month) + 1, int(day))

    if selected_date < datetime(1995, 6, 1):
        return False  # Dates before June 16, 1995, are invalid
    elif selected_date > current_date:
        return False  # Dates in the future are also invalid
    return True

# processes the selected date into a format that nasa api can take
def process_date():
    month = month_var.get()
    day = day_var.get()
    year = year_var.get()
    if is_valid_date(year, month, day):
        formatted_date = f"{year}-{months.index(month) + 1:02d}-{day.zfill(2)}"
        print(formatted_date)
        get_other_picture(formatted_date)
        date_result_label.config(text="")  # Clear any previous error message
    else:
        date_result_label.config(text="Invalid date selection")

# function to get a picture for a specific date
def get_other_picture(date):
    image_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
    response = requests.get(image_url)     
    if response.status_code == 200:
        data = response.json()
        img_url = data.get("url")
        if img_url:
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_data = img_response.content
                image = Image.open(BytesIO(img_data))
                photo = ImageTk.PhotoImage(image=image)
                image_label.config(image=photo)
                image_label.image = photo

# lists for the dropdowns
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
days = [str(i).zfill(2) for i in range(1, 32)]
years = [str(i) for i in range(1995, 2024)]

# variables to store the selected date values
month_var = tk.StringVar()
day_var = tk.StringVar()
year_var = tk.StringVar()

# comboboxes for month, day, and year
month_dropdown = ttk.Combobox(root, textvariable=month_var, values=months)
day_dropdown = ttk.Combobox(root, textvariable=day_var, values=days)
year_dropdown = ttk.Combobox(root, textvariable=year_var, values=years)

month_dropdown.pack()
day_dropdown.pack()
year_dropdown.pack()

# button to submit the selected date
submit_button = tk.Button(root, text="Submit", command=process_date)
submit_button.pack()

# label to display the result
date_result_label = tk.Label(root, text="")
date_result_label.pack()

# label to display the image
image_label = tk.Label(root)
image_label.pack()

# button to get today's picture
today_button = tk.Button(root, text="Get Today's Image", command=get_today_picture)
today_button.pack()

root.mainloop()
