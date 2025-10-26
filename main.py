import requests
from PIL import Image, UnidentifiedImageError
from weather_colour_check import colour_dict
from location_grid import location_grids
from nowcast_weather import nowcast_weather
from alarm_ui import Alarm_UI
# from alarm_ui_mpl import Alarm_UI_MPL
import get_time


# automatic nowcasting based on radar image colouring

# TO-DO
# Light blue can be cloudy
# create conditions for heavy tsra based on issuance of heavy rain warning
# cloudy when there is showers/tsra around otherwise partly cloudy or based on METAR data
# forecasting 2hrs ahead for nearby grids around severe weather based on steering wind direction and speed
# slow down rapidly changing nowcasts


# functions to get and check against colours of
# heavy TSRA: Violet, TSRA: Red, Showers: Orange/Yellow, Rain:Blue/Green
def color_difference(color1, color2) -> int:
    """ calculate the difference between two colors as sum of per-channel differences """
    return sum([abs(component1 - component2) for component1, component2 in zip(color1, color2)])


def get_color_name(color) -> str:
    """ guess color name using the closest match from KNOWN_COLORS """
    differences = [
        [color_difference(color, known_color), known_name]
        for known_name, known_color in colour_dict.items()
    ]
    differences.sort()  # sorted by the first element of inner lists
    return differences[0][1]  # the second element is the name


# get radar images from weather.gov.sg url
while True:
    time_values = get_time.get_time()
    year_now = time_values[0]
    month_now = time_values[1]
    day_now = time_values[2]
    hour_now = time_values[3]
    minute_split = time_values[4]

    # previous_time_values = get_time.get_previous_time()
    # year_previous = previous_time_values[0]
    # month_previous = previous_time_values[1]
    # day_previous = previous_time_values[2]
    # hour_previous = previous_time_values[3]
    # minute_split_previous = previous_time_values[4]

    url = f"http://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_{year_now}{month_now}" \
          f"{day_now}{hour_now}{minute_split[1]}{minute_split[0]}0000dBR.dpsri.png"
    response = requests.get(url)
    image_time = f"{year_now}-{month_now}-{day_now} {hour_now}:{minute_split[1]}{minute_split[0]}"

    try:
        with open("current_radar_image.png", "wb") as f:
            f.write(response.content)
        weather_image = Image.open("current_radar_image.png")
    except UnidentifiedImageError:
        # url = f"http://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_{year_previous}{month_previous}" \
        #       f"{day_previous}{hour_previous}{minute_split_previous[1]}{minute_split_previous[0]}0000dBR.dpsri.png"
        # response_previous = requests.get(url)
        # image_time = f"{year_previous}-{month_previous}-{day_previous} {hour_previous}:{minute_split_previous[1]}"\
        #              f"{minute_split_previous[0]}"
        #
        # with open("previous_radar_image.png", "wb") as f:
        #     f.write(response_previous.content)

        weather_image = Image.open("previous_radar_image.png")
        image_time = image_previous_time
    else:
        weather_image.save("previous_radar_image.png")
        image_previous_time = image_time

    # get median RGB colour of pixels in each grid
    neighborhood_grids = location_grids(weather_image)

    # identify colour of grid as weather
    for key, value in neighborhood_grids.items():
        for k in range(len(value)):
            value[k] = get_color_name(value[k])

    weather_nowcast = {}
    for key, value in neighborhood_grids.items():
        if 'heavy_tsra_colour' in value:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'tsra_colour' in value:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'light_tsra_colour' in value:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'showers_colour' in value:
            weather_nowcast[key] = 'Showers'
        elif 'light_showers_colour' in value:
            weather_nowcast[key] = 'Showers'
        elif 'partly_cloudy' in value:
            weather_nowcast[key] = 'Partly Cloudy'

    # produce nowcast image
    nowcast_weather(weather_nowcast, image_time)
    print("Nowcast Automating...")

    # show image and provide an alarm if there is weather
    weather_alarm = Alarm_UI(weather_nowcast)

    # # produce nowcast image
    # nowcast_weather(weather_nowcast, image_time)
    #
    # # show image and provide an alarm if there is weather
    # nowcast_image = cv2.imread("nowcast_image.png")
    # cv2.imshow("Window", nowcast_image)
    # weather_alarm = Alarm_UI(weather_nowcast)
    # cv2.destroyAllWindows()
