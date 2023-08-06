from datetime import datetime

weather_codes = {
    0: "Clear night",
    1: "Sunny day",
    2: "Partly cloudy (night)",
    3: "Partly cloudy (day)",
    4: "Not used",
    5: "Mist",
    6: "Fog",
    7: "Cloudy",
    8: "Overcast",
    9: "Light rain shower (night)",
    10: "Light rain shower (day)",
    11: "Drizzle",
    12: "Light rain",
    13: "Heavy rain shower (night)",
    14: "Heavy rain shower (day)",
    15: "Heavy rain",
    16: "Sleet shower (night)",
    17: "Sleet shower (day)",
    18: "Sleet",
    19: "Hail shower (night)",
    20: "Hail shower (day)",
    21: "Hail",
    22: "Light snow shower (night)",
    23: "Light snow shower (day)",
    24: "Light snow",
    25: "Heavy snow shower (night)",
    26: "Heavy snow shower (day)",
    27: "Heavy snow",
    28: "Thunder shower (night)",
    29: "Thunder shower (day)",
    30: "Thunder",
}


def split_days(data):
    new_data = []
    for i in range(0, len(data)):
        if i == 0:
            day = [data[i]]
        else:
            # Get previoues time block day
            previous_day = datetime.strptime(data[i - 1]["time"], "%Y-%m-%dT%H:%MZ").day
            # Get current time block day
            current_day = datetime.strptime(data[i]["time"], "%Y-%m-%dT%H:%MZ").day
            if current_day == previous_day:
                day.append(data[i])
            else:
                new_data.append(day)
                day = []
    return new_data
