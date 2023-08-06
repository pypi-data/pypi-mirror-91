from datahub.Helpers import weather_codes, split_days
from datetime import datetime, timedelta


class Forecast:
    def __init__(self, frequency=None, data=None):
        if frequency is None:
            raise Exception("No frequency provided")
        if data is None:
            raise Exception("No data provided")
        self.frequency = frequency

        self.data = data

        # Format incoming response
        self.days = []
        if frequency == "daily":
            # Format for daily frequency
            for day in self.data["features"][0]["properties"]["timeSeries"]:
                self.days.append(
                    {
                        "time": day["time"],
                        "daySignificantWeather": weather_codes[
                            day["daySignificantWeatherCode"]
                        ],
                        "nightSignificantWeather": weather_codes[
                            day["nightSignificantWeatherCode"]
                        ],
                        # Wind Speed
                        # Midday
                        "middayWindSpeed": day["midday10MWindSpeed"],
                        "middayWindDirection": day["midday10MWindDirection"],
                        "middayWindGust": day["midday10MWindGust"],
                        # Midnight
                        "midnightWindSpeed": day["midnight10MWindSpeed"],
                        "midnightWindDirection": day["midnight10MWindDirection"],
                        "midnightWindGust": day["midnight10MWindGust"],
                        # Visibility
                        # Midday
                        "middayVisibility": day["middayVisibility"],
                        # Midnight
                        "midnightVisibility": day["midnightVisibility"],
                        # Relative Humidity
                        "middayRelativeHumidity": day["middayRelativeHumidity"],
                        "midnightRelativeHumidity": day["midnightRelativeHumidity"],
                        # Pressure (divided by 100 o make it into hPa)
                        "middayPressure": day["middayMslp"] / 100,
                        "midnightPressure": day["midnightMslp"] / 100,
                        # UV
                        "maxUVIndex": day["maxUvIndex"],
                        # Temperatures
                        "maxTemperature": day["dayMaxScreenTemperature"],
                        "minTemperature": day["nightMinScreenTemperature"],
                        "maxFeelsLike": day["dayMaxFeelsLikeTemp"],
                        "minFeelsLike": day["nightMinFeelsLikeTemp"],
                        # Precipitation
                        # Day
                        "dayProbabilityOfPrecipitation": day[
                            "dayProbabilityOfPrecipitation"
                        ],
                        "dayProbabilityOfSnow": day["dayProbabilityOfSnow"],
                        "dayProbabilityOfHeavySnow": day["dayProbabilityOfHeavySnow"],
                        "dayProbabilityOfRain": day["dayProbabilityOfRain"],
                        "dayProbabilityOfHeavyRain": day["dayProbabilityOfHeavyRain"],
                        "dayProbabilityOfHail": day["dayProbabilityOfHail"],
                        # Night
                        "nightProbabilityOfPrecipitation": day[
                            "nightProbabilityOfPrecipitation"
                        ],
                        "nightProbabilityOfSnow": day["nightProbabilityOfSnow"],
                        "nightProbabilityOfHeavySnow": day[
                            "nightProbabilityOfHeavySnow"
                        ],
                        "nightProbabilityOfRain": day["nightProbabilityOfRain"],
                        "nightProbabilityOfHeavyRain": day[
                            "nightProbabilityOfHeavyRain"
                        ],
                        "nightProbabilityOfHail": day["nightProbabilityOfHail"],
                    }
                )
        else:
            # Split hourly and three hourly time series into days
            time_series = self.data["features"][0]["properties"]["timeSeries"]
            self.days = split_days(time_series)

            # Convert mslp to hPa
            for day in self.days:
                for hour in day:
                    # Change "significantWeatherCode" to "significantWeather"
                    hour["mslp"] = hour.pop("mslp") / 100

                    if frequency == "hourly":
                        # Change "significantWeatherCode" to "significantWeather"
                        hour["significantWeather"] = weather_codes[
                            hour.pop("significantWeatherCode")
                        ]

    def at_time(self, target_time=None):
        """Find data for closest to datetime given"""
        if target_time is None:
            # You need to specify a time
            raise Exception("No target_time specified")
        elif not isinstance(target_time, datetime):
            # Time needs to be specified as a datetime
            raise Exception("target_time is not a datetime")

        if self.frequency == "daily":
            # Only a daily frequency - just need to match the day to the target
            for day in self.days:
                day_date = datetime.strptime(day["time"], "%Y-%m-%dT%H:%MZ")
                if day_date.date() == target_time.date():
                    # Matched date
                    return day
        else:
            # Find all steps within 1.5 hours (four hourly) / 3.5 hours (for three hourly)
            potential_responses = []
            for day in self.days:
                for hour in day:
                    hour_time = datetime.strptime(hour["time"], "%Y-%m-%dT%H:%MZ")
                    # 1.5 hour before target & 1.5hour after target if hourly, 3.5hour if three-hourly
                    start = target_time - timedelta(
                        hours=1 if self.frequency == "hourly" else 3, minutes=30
                    )
                    end = target_time + timedelta(
                        hours=1 if self.frequency == "hourly" else 3, minutes=30
                    )

                    if start <= hour_time <= end:
                        hour["delta"] = abs(hour_time - target_time)
                        potential_responses.append(hour)
            # Find all delta values
            seq = [x["delta"] for x in potential_responses]
            # Return potential response with lowest delta
            return potential_responses[seq.index(min(seq))]

    def now(self):
        """Call at_time with datetime.now()"""
        return self.at_time(datetime.now())
