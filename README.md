# Week 7 — Data Pipelines & Automation (ETL)
**AnalystLab Africa Data Analytics Internship — Batch C**

## Project Overview
This project builds a simple ETL (Extract, Transform, Load) pipeline in Python that retrieves real-time weather data from the OpenWeather API for three cities, cleans and structures it with Pandas, stores it as a CSV file, and performs a basic comparative analysis.

## Data Source
- **API:** [OpenWeather API](https://openweathermap.org/api) — Current Weather Data endpoint
- **Cities analyzed:** Lagos (Nigeria), Cotonou (Benin), Paris (France)
- **Fields retrieved:** City Name, Temperature (°C), Humidity (%), Weather Condition, Wind Speed (m/s), Date & Time

## ETL Process

### 1. Extract
The pipeline connects to the OpenWeather API using a personal API key and sends a request for each city, retrieving the current weather data in JSON format.

### 2. Transform
The raw JSON responses are parsed and converted into a structured Pandas DataFrame:
- Columns renamed for clarity (`city`, `temperature_celsius`, `humidity_percent`, `weather_condition`, `wind_speed_ms`, `date_time`)
- Unix timestamp converted into a readable datetime
- Data types enforced (float for temperature/wind speed, int for humidity, datetime for date_time)
- Weather condition text standardized to title case

### 3. Load
The cleaned dataset is saved as a timestamped CSV file inside the `data/` folder (e.g. `data/weather_data_20260813_161500.csv`), so each pipeline run keeps its own snapshot.

### 4. Basic Analysis
The pipeline automatically prints:
- The hottest and coldest city among the three
- The city with the highest humidity
- A side-by-side comparison of weather conditions

## Tools Used
- Python 3
- Requests (API calls)
- Pandas (data transformation)
- Matplotlib (visualizations, in the notebook)
- OpenWeather API

## Project Structure
```
week7_weather_etl/
├── etl_pipeline.py          # Main ETL script (Extract, Transform, Load, Analyze)
├── weather_etl_analysis.ipynb   # Jupyter Notebook version with visualizations
├── config_template.py       # Template for API key configuration (safe to share)
├── config.py                # Your actual API key (NOT committed to GitHub)
├── requirements.txt         # Python dependencies
├── data/                    # Output folder for processed CSV files
├── .gitignore
└── README.md
```

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `config_template.py` to `config.py` and paste your own OpenWeather API key.
3. Run the pipeline:
   ```
   python etl_pipeline.py
   ```
   or open `weather_etl_analysis.ipynb` in Jupyter Notebook.
4. The processed dataset will be saved in the `data/` folder.

## Key Findings
The ETL pipeline successfully extracted, transformed, and loaded real-time weather data for three cities on 20 August 2026:

| City    | Temperature (°C) | Humidity (%) | Weather Condition |
|---------|-------------------|--------------|--------------------|
| Lagos   | 30.16             | 64           | Broken Clouds      |
| Cotonou | 29.99             | 74           | Broken Clouds      |
| Paris   | 24.52             | 46           | Overcast Clouds    |

- **Hottest city:** Lagos (30.16°C), closely followed by Cotonou (29.99°C)
- **Coldest city:** Paris (24.52°C) — nearly 6°C cooler than the West African cities
- **Most humid city:** Cotonou (74%), consistent with its coastal, tropical climate
- Lagos and Cotonou shared similar weather conditions (broken clouds), while Paris showed overcast skies
- These results confirm the expected climatic contrast between tropical West African cities and a temperate European city

## Author
Mtk — AnalystLab Africa Data Analytics Internship, Batch C
