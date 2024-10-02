import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import os

# Constants for BMI categorization
BMI_CATEGORIES = {
    'Underweight': (0, 18.5),
    'Normal weight': (18.5, 24.9),
    'Overweight': (25, 29.9),
    'Obesity': (30, float('inf'))
}

# Data storage file
DATA_FILE = 'bmi_data.json'

# Function to load user data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user data
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")
        
        bmi = weight / (height ** 2)
        bmi_result.set(f"BMI: {bmi:.2f}")
        categorize_bmi(bmi)
        
        # Save the data
        username = username_entry.get()
        user_data = load_data()
        if username not in user_data:
            user_data[username] = []
        user_data[username].append(bmi)
        save_data(user_data)
        
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

# Function to categorize BMI
def categorize_bmi(bmi):
    for category, (lower, upper) in BMI_CATEGORIES.items():
        if lower < bmi <= upper:
            category_result.set(f"Category: {category}")
            return

# Function to visualize BMI history
def visualize_bmi():
    username = username_entry.get()
    user_data = load_data()
    if username in user_data:
        plt.figure(figsize=(10, 5))
        plt.plot(user_data[username], marker='o')
        plt.title(f'BMI Trend for {username}')
        plt.xlabel('Record Number')
        plt.ylabel('BMI')
        plt.axhline(y=18.5, color='blue', linestyle='--', label='Underweight')
        plt.axhline(y=24.9, color='green', linestyle='--', label='Normal')
        plt.axhline(y=29.9, color='orange', linestyle='--', label='Overweight')
        plt.axhline(y=30, color='red', linestyle='--', label='Obesity')
        plt.legend()
        plt.grid()
        plt.show()
    else:
        messagebox.showinfo("No Data", "No BMI data found for this user.")

# Create the main application window
app = tk.Tk()
app.title("BMI Calculator")

# GUI Elements
tk.Label(app, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(app)
username_entry.grid(row=0, column=1)

tk.Label(app, text="Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(app)
weight_entry.grid(row=1, column=1)

tk.Label(app, text="Height (m):").grid(row=2, column=0)
height_entry = tk.Entry(app)
height_entry.grid(row=2, column=1)

bmi_result = tk.StringVar()
category_result = tk.StringVar()

tk.Button(app, text="Calculate BMI", command=calculate_bmi).grid(row=3, columnspan=2)
tk.Label(app, textvariable=bmi_result).grid(row=4, columnspan=2)
tk.Label(app, textvariable=category_result).grid(row=5, columnspan=2)

tk.Button(app, text="View BMI History", command=visualize_bmi).grid(row=6, columnspan=2)

# Start the main event loop
app.mainloop()
