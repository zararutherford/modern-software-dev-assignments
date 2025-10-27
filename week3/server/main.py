#!/usr/bin/env python3
"""
Weather MCP Server

A Model Context Protocol server that provides weather data through OpenWeatherMap API.
Implements two tools: get_current_weather and get_weather_forecast.
"""

import os
import sys
import json
import logging
from typing import Any, Optional
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Configure logging to stderr (not stdout, as stdout is used for MCP communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("weather-mcp-server")

# OpenWeatherMap API configuration
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Rate limiting tracking (simple implementation)
request_count = 0
MAX_REQUESTS_PER_SESSION = 100


def check_rate_limit() -> None:
    """Check if we're approaching rate limits and log warnings."""
    global request_count
    request_count += 1

    if request_count > MAX_REQUESTS_PER_SESSION:
        logger.warning(f"Request count ({request_count}) exceeds session limit. Consider API rate limits.")
    elif request_count % 10 == 0:
        logger.info(f"API request count: {request_count}")


def make_api_request(endpoint: str, params: dict) -> dict:
    """
    Make a request to the OpenWeatherMap API with error handling.

    Args:
        endpoint: API endpoint path (e.g., 'weather', 'forecast')
        params: Query parameters dictionary

    Returns:
        Parsed JSON response as dictionary

    Raises:
        ValueError: If API key is not configured
        Exception: For various API errors with descriptive messages
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")

    check_rate_limit()

    # Add API key to parameters
    params['appid'] = API_KEY

    url = f"{BASE_URL}/{endpoint}?{urlencode(params)}"

    try:
        logger.info(f"Making request to OpenWeatherMap: {endpoint}")
        request = Request(url)
        request.add_header('User-Agent', 'Weather-MCP-Server/1.0')

        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            logger.info(f"Successfully received response from {endpoint}")
            return data

    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        logger.error(f"HTTP error {e.code}: {error_body}")

        if e.code == 401:
            raise Exception("Invalid API key. Please check your OPENWEATHER_API_KEY.")
        elif e.code == 404:
            raise Exception("Location not found. Please check the city name or coordinates.")
        elif e.code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        else:
            raise Exception(f"API error ({e.code}): {error_body}")

    except URLError as e:
        logger.error(f"Network error: {e.reason}")
        raise Exception(f"Network error: Unable to reach OpenWeatherMap API. {e.reason}")

    except TimeoutError:
        logger.error("Request timeout")
        raise Exception("Request timeout: OpenWeatherMap API did not respond in time.")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise Exception("Failed to parse API response.")


def format_current_weather(data: dict) -> str:
    """Format current weather data into a readable string."""
    try:
        location = data.get('name', 'Unknown')
        country = data.get('sys', {}).get('country', '')

        weather = data.get('weather', [{}])[0]
        main = data.get('main', {})
        wind = data.get('wind', {})

        # Convert temperature from Kelvin to Celsius and Fahrenheit
        temp_k = main.get('temp', 0)
        temp_c = temp_k - 273.15
        temp_f = (temp_c * 9/5) + 32

        feels_like_k = main.get('feels_like', 0)
        feels_like_c = feels_like_k - 273.15
        feels_like_f = (feels_like_c * 9/5) + 32

        return f"""Current Weather for {location}, {country}:

Description: {weather.get('main', 'N/A')} - {weather.get('description', 'N/A')}
Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)
Feels Like: {feels_like_c:.1f}°C ({feels_like_f:.1f}°F)
Humidity: {main.get('humidity', 'N/A')}%
Pressure: {main.get('pressure', 'N/A')} hPa
Wind Speed: {wind.get('speed', 'N/A')} m/s
Cloudiness: {data.get('clouds', {}).get('all', 'N/A')}%
"""
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Error formatting weather data: {e}")
        return f"Error formatting weather data: {str(e)}"


def format_forecast(data: dict) -> str:
    """Format forecast data into a readable string."""
    try:
        city = data.get('city', {})
        location = city.get('name', 'Unknown')
        country = city.get('country', '')

        forecast_list = data.get('list', [])

        if not forecast_list:
            return "No forecast data available."

        result = [f"5-Day Weather Forecast for {location}, {country}:\n"]

        # Group by day and take first forecast per day (every 8th item = new day)
        for i in range(0, min(40, len(forecast_list)), 8):
            forecast = forecast_list[i]

            dt_txt = forecast.get('dt_txt', 'N/A')
            weather = forecast.get('weather', [{}])[0]
            main = forecast.get('main', {})

            temp_k = main.get('temp', 0)
            temp_c = temp_k - 273.15
            temp_f = (temp_c * 9/5) + 32

            temp_min_k = main.get('temp_min', 0)
            temp_min_c = temp_min_k - 273.15

            temp_max_k = main.get('temp_max', 0)
            temp_max_c = temp_max_k - 273.15
            temp_max_f = (temp_max_c * 9/5) + 32

            result.append(f"""
Date/Time: {dt_txt}
Condition: {weather.get('main', 'N/A')} - {weather.get('description', 'N/A')}
Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)
Min/Max: {temp_min_c:.1f}°C / {temp_max_c:.1f}°C ({temp_max_f:.1f}°F)
Humidity: {main.get('humidity', 'N/A')}%
""")

        return "\n".join(result)

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Error formatting forecast data: {e}")
        return f"Error formatting forecast data: {str(e)}"


# Create the MCP server instance
server = Server("weather-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available weather tools."""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather conditions for a specific location. Provides temperature, humidity, wind speed, and weather description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'London', 'New York') or city name with country code (e.g., 'London,UK', 'Paris,FR')"
                    },
                    "units": {
                        "type": "string",
                        "description": "Units of measurement: 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin)",
                        "enum": ["metric", "imperial", "standard"],
                        "default": "metric"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_weather_forecast",
            description="Get 5-day weather forecast with 3-hour intervals for a specific location. Useful for planning ahead.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'London', 'New York') or city name with country code (e.g., 'London,UK', 'Paris,FR')"
                    },
                    "units": {
                        "type": "string",
                        "description": "Units of measurement: 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin)",
                        "enum": ["metric", "imperial", "standard"],
                        "default": "metric"
                    }
                },
                "required": ["location"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for weather data."""
    try:
        if name == "get_current_weather":
            location = arguments.get("location")
            units = arguments.get("units", "metric")

            if not location:
                raise ValueError("Location parameter is required")

            logger.info(f"Getting current weather for: {location}")

            params = {
                "q": location,
                "units": units
            }

            data = make_api_request("weather", params)
            formatted = format_current_weather(data)

            return [TextContent(type="text", text=formatted)]

        elif name == "get_weather_forecast":
            location = arguments.get("location")
            units = arguments.get("units", "metric")

            if not location:
                raise ValueError("Location parameter is required")

            logger.info(f"Getting weather forecast for: {location}")

            params = {
                "q": location,
                "units": units
            }

            data = make_api_request("forecast", params)
            formatted = format_forecast(data)

            return [TextContent(type="text", text=formatted)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Run the MCP server using stdio transport."""
    logger.info("Starting Weather MCP Server")

    if not API_KEY:
        logger.error("OPENWEATHER_API_KEY environment variable not set!")
        logger.error("Please set it before running the server.")
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server initialized, ready to handle requests")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
