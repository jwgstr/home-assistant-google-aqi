# Google AQI

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/docs/setup/custom_repositories)
[![GitHub release](https://img.shields.io/github/v/release/jwgstr/home-assistant-google-aqi?style=for-the-badge)](https://github.com/jwgstr/home-assistant-google-aqi/releases)

A fork of @bairnhard's Google AQI HACS custom component.  This is experimental and meant as a starting place for integrating back into his work.  The remainder of the README needs to be udpated.

FIXME: update the README as it currently is the same as @bairnhard's Google AQI HACS custom component (however, it largely is setup in the same way for now)
FIXME: turns out this approach likely won't work and we'll need to baseline off of something else like the Tomorrowio component in core.
FIXME: Going to explore a RESTFul Sensor first as that would likely be less work and add it here in this README if it does

## RESTful Alternative

For now I've setup this alternative which pulls a single day and maps the values from -1 (not availble) to 5 where 0-5 are the valid levels of pollen from the api.  The scan interval is 6 hours.  
The API costs double the AQI api so keep that in mind when setting a value for scan_interval.

```
rest:
  - scan_interval: 21600
    resource: 'https://pollen.googleapis.com/v1/forecast:lookup?key=YOUR_KEY_HERE&location.longitude=YOUR_LONG&location.latitude=YOUR_LAT&days=1'
    sensor:
      - name: "google_pollen_grass"
        value_template: "{{ ((value_json['dailyInfo'][0]['pollenTypeInfo']|selectattr('code', 'equalto', 'GRASS')|first)['indexInfo']|default('-1'))['value']|default('-1') }}"
      - name: "google_pollen_grass_details"
        value_template: >
            {% for i in value_json['dailyInfo'][0]['plantInfo']|selectattr("inSeason", "equalto", true)|selectattr("plantDescription.type", "equalto", "GRASS") %}{{ i['code'] }}: {{i['indexInfo']['value']}}
            {% endfor %}        
      - name: "google_pollen_tree"
        value_template: "{{ ((value_json['dailyInfo'][0]['pollenTypeInfo']|selectattr('code', 'equalto', 'TREE')|first)['indexInfo']|default('-1'))['value']|default('-1') }}"
      - name: "google_pollen_tree_details"
        value_template: >
            {% for i in value_json['dailyInfo'][0]['plantInfo']|selectattr("inSeason", "equalto", true)|selectattr("plantDescription.type", "equalto", "TREE") %}{{ i['code'] }}: {{i['indexInfo']['value']}}
            {% endfor %}
      - name: "google_pollen_weed"
        value_template: "{{ ((value_json['dailyInfo'][0]['pollenTypeInfo']|selectattr('code', 'equalto', 'WEED')|first)['indexInfo']|default('-1'))['value']|default('-1') }}"
      - name: "google_pollen_weed_details"
        value_template: >
            {% for i in value_json['dailyInfo'][0]['plantInfo']|selectattr("inSeason", "equalto", true)|selectattr("plantDescription.type", "equalto", "WEED") %}{{ i['code'] }}: {{i['indexInfo']['value']}}
            {% endfor %}
```


######################



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
3. Add this repository as a custom repository: `https://github.com/jwgstr/home-assistant-google-aqi`.
4. Search for **Google AQI** and install the integration.

### Manual Installation
1. Download the latest release from the [Releases page](https://github.com/jwgstr/home-assistant-google-aqi/releases).
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

