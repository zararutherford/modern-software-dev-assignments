# Weather MCP Server

A Model Context Protocol server providing real-time weather data via the OpenWeatherMap API.

## Quick Start

1. **Get API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api) (free tier: 1,000 calls/day)

2. **Install Dependencies**:
   ```bash
   cd week3/server
   pip install -r requirements.txt
   ```

3. **Set API Key**:
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   ```

4. **Test**:
   ```bash
   python test_server.py  # Verify structure
   python main.py         # Start server
   ```

## Prerequisites

- Python 3.10+
- OpenWeatherMap API key
- Claude Desktop (or MCP-compatible client)

## Configuration

### Environment Setup

Set your API key via environment variable or `.env` file:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

Or copy `.env.example` to `.env` and add your key.

### Claude Desktop Integration

Edit your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/week3/server/main.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Important**: Use the absolute path to `main.py`. Get it with:
```bash
cd week3/server && pwd
```

Restart Claude Desktop. Look for the hammer icon (🔨) to confirm tools are loaded.

## Tools

### get_current_weather

Get current weather conditions for any location.

**Parameters**:
- `location` (required): City name or "City,CountryCode" (e.g., "London,UK")
- `units` (optional): "metric", "imperial", or "standard" (default: "metric")

**Example Input**:
```json
{"location": "Tokyo,JP", "units": "metric"}
```

**Example Output**:
```
Current Weather for Tokyo, JP:

Description: Clear - clear sky
Temperature: 22.3°C (72.1°F)
Feels Like: 21.8°C (71.2°F)
Humidity: 60%
Pressure: 1013 hPa
Wind Speed: 3.1 m/s
Cloudiness: 10%
```

**Expected Behaviors**:
- Success: Returns formatted weather data
- Invalid location: "Location not found. Please check the city name or coordinates."
- Invalid API key: "Invalid API key. Please check your OPENWEATHER_API_KEY."
- Network error: Error message with connection details
- Rate limit: "Rate limit exceeded. Please try again later."

### get_weather_forecast

Get 5-day weather forecast with 3-hour intervals.

**Parameters**:
- `location` (required): City name or "City,CountryCode"
- `units` (optional): "metric", "imperial", or "standard" (default: "metric")

**Example Input**:
```json
{"location": "Paris,FR"}
```

**Example Output**:
```
5-Day Weather Forecast for Paris, FR:

Date/Time: 2024-10-26 12:00:00
Condition: Clouds - scattered clouds
Temperature: 15.2°C (59.4°F)
Min/Max: 14.1°C / 16.3°C (61.3°F)
Humidity: 72%

Date/Time: 2024-10-27 12:00:00
Condition: Rain - light rain
Temperature: 13.8°C (56.8°F)
Min/Max: 12.5°C / 14.2°C (57.6°F)
Humidity: 85%
...
```

**Expected Behaviors**:
- Success: Returns forecast for up to 5 days
- Invalid location: "Location not found. Please check the city name or coordinates."
- No data: "No forecast data available."
- Errors handled same as current weather tool

## Usage in Claude Desktop

Once configured, ask naturally:
- "What's the weather in Seattle?"
- "Get the forecast for Paris this week"
- "Will it rain in London?"

## Implementation Details

**API**: OpenWeatherMap REST API v2.5
- Current weather: `/data/2.5/weather`
- Forecast: `/data/2.5/forecast`

**Transport**: STDIO (local)

**Error Handling**:
- HTTP errors (401/404/429/5xx)
- Network timeouts (10s limit)
- JSON parsing errors
- Input validation

**Rate Limiting**: Tracks requests, logs warnings at 100+ calls

**Logging**: All logs to stderr (MCP requirement)

## Testing

**Automated test**:
```bash
python test_server.py
```

**MCP Inspector** (visual testing):
```bash
npx @modelcontextprotocol/inspector python main.py
```

**Manual test**:
```bash
python main.py  # Ctrl+C to stop
```

## Troubleshooting

**Server not in Claude Desktop**:
- Verify absolute path in config
- Check Python version: `python --version`
- Restart Claude Desktop
- Check logs: `~/Library/Logs/Claude/` (macOS)

**API key errors**:
- New keys take 1-2 minutes to activate
- Verify at https://openweathermap.org/api-keys

**Location not found**:
- Add country code: "London,UK"
- Check spelling

## Project Structure

```
week3/
├── README.md
└── server/
    ├── main.py           # MCP server (315 lines)
    ├── test_server.py    # Automated tests
    ├── requirements.txt  # Dependencies
    └── .env.example      # Config template
```

## Resources

- [MCP Docs](https://modelcontextprotocol.io)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [MCP Quickstart](https://modelcontextprotocol.io/quickstart/server)
