"""
etl_pipeline.py
================
AnalystLab Africa - Week 7: Data Pipelines & Automation
ETL Pipeline: Extract weather data from the OpenWeather API,
Transform it into a clean structured format, and Load it into a CSV file.

Author: Mtk
Cities analyzed: Lagos, Cotonou, Paris
"""

import requests
import pandas as pd
from datetime import datetime
import os

from config import OPENWEATHER_API_KEY, CITIES

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OUTPUT_DIR = "data"


# ---------------------------------------------------------------------------
# TASK 1: EXTRACT
# ---------------------------------------------------------------------------
def extract_weather_data(cities, api_key):
    """
    Connects to the OpenWeather API and retrieves current weather data
    for a list of cities.

    Returns a list of raw JSON responses (one dict per city).
    """
    raw_records = []

    for city in cities:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Celsius, m/s for wind speed
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            raw_records.append(response.json())
            print(f"[OK] Data extracted for {city}")
        else:
            print(f"[ERROR] Failed to extract data for {city} "
                  f"(status code: {response.status_code}) - {response.text}")

    return raw_records


# ---------------------------------------------------------------------------
# TASK 2: TRANSFORM
# ---------------------------------------------------------------------------
def transform_weather_data(raw_records):
    """
    Transforms raw JSON weather records into a clean, structured
    pandas DataFrame with renamed columns and correct data types.
    """
    cleaned_rows = []

    for record in raw_records:
        cleaned_rows.append({
            "city": record["name"],
            "temperature_celsius": record["main"]["temp"],
            "humidity_percent": record["main"]["humidity"],
            "weather_condition": record["weather"][0]["description"].title(),
            "wind_speed_ms": record["wind"]["speed"],
            "date_time": datetime.utcfromtimestamp(record["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(cleaned_rows)

    # Ensure correct data types
    df["temperature_celsius"] = df["temperature_celsius"].astype(float)
    df["humidity_percent"] = df["humidity_percent"].astype(int)
    df["wind_speed_ms"] = df["wind_speed_ms"].astype(float)
    df["date_time"] = pd.to_datetime(df["date_time"])

    return df


# ---------------------------------------------------------------------------
# TASK 3: LOAD
# ---------------------------------------------------------------------------
def load_weather_data(df, output_dir=OUTPUT_DIR):
    """
    Saves the transformed DataFrame to a timestamped CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"weather_data_{timestamp}.csv")

    df.to_csv(filepath, index=False)
    print(f"[OK] Data saved to {filepath}")

    return filepath


# ---------------------------------------------------------------------------
# TASK 4: BASIC ANALYSIS
# ---------------------------------------------------------------------------
def analyze_weather_data(df):
    """
    Performs a simple comparative analysis on the collected weather data
    and prints a short summary of findings.
    """
    print("\n===== WEATHER ANALYSIS SUMMARY =====\n")

    print("Full dataset:")
    print(df.to_string(index=False))

    hottest = df.loc[df["temperature_celsius"].idxmax()]
    coldest = df.loc[df["temperature_celsius"].idxmin()]
    most_humid = df.loc[df["humidity_percent"].idxmax()]

    print(f"\nHottest city:   {hottest['city']} ({hottest['temperature_celsius']}°C)")
    print(f"Coldest city:   {coldest['city']} ({coldest['temperature_celsius']}°C)")
    print(f"Most humid city: {most_humid['city']} ({most_humid['humidity_percent']}%)")

    print("\nWeather conditions comparison:")
    print(df[["city", "weather_condition"]].to_string(index=False))

    print("\n=====================================\n")


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
def run_pipeline():
    print("Starting ETL pipeline...\n")

    # Extract
    raw_data = extract_weather_data(CITIES, OPENWEATHER_API_KEY)

    if not raw_data:
        print("No data was extracted. Check your API key and city names.")
        return

    # Transform
    df_clean = transform_weather_data(raw_data)

    # Load
    load_weather_data(df_clean)

    # Analyze
    analyze_weather_data(df_clean)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
