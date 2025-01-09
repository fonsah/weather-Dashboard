import csv
import os

def save_to_csv(weather_data, city):
    if not weather_data:
        return

    file_exists = os.path.isfile('weather_data.csv')
    with open('weather_data.csv', mode='a', newline='') as csv_file:
        fieldnames = ['city', 'temp', 'feels_like', 'humidity', 'description', 'timestamp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if file doesn't exist
        if not file_exists:
            writer.writeheader()

        row = {
            'city': city,
            'temp': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'description': weather_data['weather'][0]['description'],
            'timestamp': weather_data['timestamp']  # from your code
        }
        writer.writerow(row)
        
import matplotlib.pyplot as plt
import pandas as pd

def plot_temperature_trend(csv_file, city):
    # Load the CSV data into a Pandas DataFrame
    df = pd.read_csv(csv_file)

    # Filter data for the specific city
    city_data = df[df['city'] == city]

    # Convert 'timestamp' to datetime for proper plotting
    city_data['timestamp'] = pd.to_datetime(city_data['timestamp'], format='%Y%m%d-%H%M%S')

    # Sort the data by timestamp to ensure chronological order
    city_data = city_data.sort_values(by='timestamp')

    # Plot Temperature and Feels Like over time
    plt.figure(figsize=(10, 6))
    plt.plot(city_data['timestamp'], city_data['temp'], label='Temperature (°F)', marker='o')
    plt.plot(city_data['timestamp'], city_data['feels_like'], label='Feels Like (°F)', linestyle='--')

    # Add labels, title, and legend
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°F)')
    plt.title(f"Temperature Trends for {city}")
    plt.legend()
    plt.grid(True)  # Optional: Add grid lines for better readability
    plt.tight_layout()

    # Show the plot
    plt.show()

# Call the function for Philadelphia
plot_temperature_trend('weather_data.csv', 'Philadelphia')
