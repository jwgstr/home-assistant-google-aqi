from homeassistant.components.air_quality import AirQualityEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from datetime import datetime, timedelta, timezone
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

FORECAST_URL = "https://pollen.googleapis.com/v1/forecast:lookup"


class GooglePollenAirQualityEntity(AirQualityEntity):
    """Representation of a Google Pollen air quality entity."""

    def __init__(
        self,
        hass,
        api_key,
        latitude,
        longitude,
        forecast_interval
    ):
        self.hass = hass
        self._api_key = api_key
        self._latitude = latitude
        self._longitude = longitude
        self._forecast_interval = forecast_interval

        # FIXME: get rid of _state?
        self._state = None
        self._pollens = {}
        self._forecast = []

        # Timestamps and statuses
        self._last_forecast_api_call = None
        self._next_forecast_api_call = None
        self._forecast_api_status = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Google Pollen Sensor"

    @property
    def state(self):
        """Return the date as the state."""
        # FIXME: put the date or null here to indicate the state?
        return 1

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        attributes = {
            "forecast": self._forecast,
            "last_forecast_api_call": self._last_forecast_api_call,
            "next_forecast_api_call": self._next_forecast_api_call,
            "forecast_api_status": self._forecast_api_status,
        }

        return attributes

    @property
    def grass(self):
        """Return the grass value."""
        return self._pollens.get("grass")

    @property
    def tree(self):
        """Return the tree value."""
        return self._pollens.get("tree")

    @property
    def weed(self):
        """Return the weed value."""
        return self._pollens.get("weed")

    async def async_update(self):
        """Fetch forecast data with optimized API calls."""
        now = datetime.now()
        self._next_forecast_api_call = now + timedelta(hours=self._forecast_interval)

        tasks = []

        if (
            not self._last_forecast_api_call
            or now - self._last_forecast_api_call
            > timedelta(hours=self._forecast_interval)
        ):
            tasks.append(self._fetch_forecast_data())

        await asyncio.gather(*tasks)

    async def _fetch_forecast_data(self):
        """Fetch forecast data with correct start and end time calculation."""
        self._last_forecast_api_call = datetime.now()

        params = {"key": self._api_key, 
                  "location.longitude": self._longitude,
                  "location.latitude": self._latitude,
                  "days": 5}

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(
                FORECAST_URL, params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self._process_forecast_data(data)
                    self._last_forecast_update = datetime.now(timezone.utc)
                    self._forecast_api_status = "successful"
                else:
                    error_text = await response.text()
                    _LOGGER.error(
                        f"Failed to fetch forecast data: {response.status} - {error_text}"
                    )
                    self._forecast_api_status = "error"
        except Exception as e:
            _LOGGER.error(f"Error fetching forecast data: {e}")
            self._forecast_api_status = "error"

    def _process_forecast_data(self, data):
        """Process forecast data for pollen."""
        if not data or "dailyInfo" not in data:
            _LOGGER.warning("Received empty or invalid forecast data from API")
            self._forecast = []
            return

        # FIXME: add in additional information from the response
        # FIXME: format the date into the same datetime object as the Google AQI?
        # FIXME: do we need all these 'get' calls?
        self._forecast = [
            {
                "datetime": forecast.get("date"),
                "grass": [p for p in forecast.get("pollenTypeInfo", {}) if p.get("code") == "GRASS"][0].get("indexInfo", {}).get("value"),
                "tree":  [p for p in forecast.get("pollenTypeInfo", {}) if p.get("code") == "TREE"][0].get("indexInfo", {}).get("value"),
                "weed":  [p for p in forecast.get("pollenTypeInfo", {}) if p.get("code") == "WEED"][0].get("indexInfo", {}).get("value")
            }
            for forecast in data["dailyInfo"]
        ]

        # assume for now that the first one is today
        self._pollens = self._forecast[0]

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Google Pollen air quality sensor from a config entry."""
    config = config_entry.data
    async_add_entities(
        [
            GooglePollenAirQualityEntity(
                hass,
                api_key=config["api_key"],
                latitude=config["latitude"],
                longitude=config["longitude"],
                forecast_interval=config.get("forecast_interval", 6)
            )
        ],
        update_before_add=True,
    )
