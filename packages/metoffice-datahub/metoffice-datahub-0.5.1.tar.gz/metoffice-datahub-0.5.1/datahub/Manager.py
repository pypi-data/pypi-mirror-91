import requests
from datahub.Forecast import Forecast


class Manager:
    def __init__(self, client_id=None, client_secret=None):
        if client_id is None:
            raise Exception("No Client ID Provided")
        if client_secret is None:
            raise Exception("No Client Secret Provided")

        self.headers = {
            "X-IBM-Client-Id": client_id,
            "X-IBM-Client-Secret": client_secret,
        }
        # API Info
        self.base_url = "https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/{}?excludeParameterMetadata=true&includeLocationName=true&latitude={}&longitude={}"

    def get_forecast(self, latitude=None, longitude=None, frequency="daily"):
        if latitude is None:
            raise Exception("No latitude provided")
        if longitude is None:
            raise Exception("No longitude provided")

        url = self.base_url.format(frequency, latitude, longitude)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response not OK")
        data = response.json()
        return Forecast(frequency=frequency, data=data)
