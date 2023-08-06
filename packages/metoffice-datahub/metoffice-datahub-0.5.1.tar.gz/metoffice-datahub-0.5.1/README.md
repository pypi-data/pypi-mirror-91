# DataHub Python Library

Work in progress Python library for MetOffice DataHub (replacing datapoint)

## Usage
```
import datahub
conn = datahub.connection("clientID", "clientSecret")

forecast = conn.get_forecast(frequency="daily|hourly|three-hourly", latitude="latitude", longitude="longitude")
print(forecast.days)
```