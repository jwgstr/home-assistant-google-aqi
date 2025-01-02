# Google AQI

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/docs/setup/custom_repositories)
[![GitHub release](https://img.shields.io/github/v/release/bairnhard/home-assistant-google-aqi?style=for-the-badge)](https://github.com/bairnhard/home-assistant-google-aqi/releases)

A custom integration for Home Assistant to monitor air quality using Google’s Air Quality API. This integration fetches current air quality data and provides forecasts for up to 96 hours in the future.

## Features
- **Real-time Air Quality Monitoring**:
  - Current air quality index (AQI)
  - Pollutants: PM2.5, PM10, CO, NO₂, O₃, SO₂, and more
  - Health recommendations based on AQI levels
- **Forecasting**:
  - Up to 96 hours of hourly air quality forecasts
  - Provides forecasted AQI and dominant pollutants
- **Attributes**:
  - Includes pollutant sources, effects, and additional metadata (configurable)

## Installation

### Using HACS
1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** and click **+ Explore & Download Repositories**.
3. Add this repository as a custom repository: `https://github.com/bairnhard/home-assistant-google-aqi`.
4. Search for **Google AQI** and install the integration.

### Manual Installation
1. Download the latest release from the [Releases page](https://github.com/bairnhard/home-assistant-google-aqi/releases).
2. Extract the contents into your Home Assistant `custom_components/google_aqi/` directory.
3. Restart Home Assistant.

## Configuration

1. Go to **Settings** > **Devices & Services** > **+ Add Integration**.
2. Search for **Google AQI** and click to configure.
3. Enter the following details:
   - **API Key**: Your Google Air Quality API key.
   - **Latitude** and **Longitude**: The location for air quality monitoring. (your home location by default)
   - **Current Update Interval (hours)**: How often to fetch current air quality data (default: 1 hour, range: 1–24 hours).
   - **Forecast Update Interval (hours)**: How often to fetch forecast data (default: 6 hours, range: 1–24 hours).
   - **Forecast Length (hours)**: Number of hours to forecast (default: 24 hours, max: 96 hours).
   - **Get Additional Info?**: Check to include pollutant sources and effects in attributes.

4. Save the configuration.

## Attributes

### Current Data
- **Air Quality Index (AQI)**: Universal AQI based on pollutants.
- **Pollutants**:
  - `pm25`, `pm10`, `co`, `no2`, `o3`, `so2`
  - Attributes: `value`, `unit`, `sources`, `effects` (optional)
- **Indices**:
  - `index_uaqi`: AQI value, category, and dominant pollutant
  - `index_deu_uba` (if applicable): Localized AQI index or any other local index.
- **Metadata**:
  - `region`
  - `last_update`

### Forecast Data
- **Forecast**: A list of dictionaries for up to 96 hours, each containing:
  - `datetime`: Forecast hour (UTC)
  - `aqi`: Forecasted AQI
  - `dominant_pollutant`: Forecasted dominant pollutant

### API Call Timestamps
- **Current API**:
  - `last_current_api_call`
  - `next_current_api_call`
  - `current_api_status`: `successful` or `error`
- **Forecast API**:
  - `last_forecast_api_call`
  - `next_forecast_api_call`
  - `forecast_api_status`: `successful` or `error`

### API Key Setup
1. Go to the Google Cloud Console.
2. Create a project and enable the Air Quality API.
3. Generate an API key and add it to the integration configuration.

### Issues & Feature Requests
If you encounter any issues or have feature requests, please open an issue on the GitHub repository.

### License
This project is licensed under the MIT License.

