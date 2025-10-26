from PIL import Image, ImageFont, ImageDraw


def nowcast_weather(weather_situation, nowcast_time):
    im1 = Image.open('SG_nowcast_areas_resized.png')
    thundery_showers_icon = Image.open('weather_icons/thundery_showers_icon.png')
    thundery_showers_icon = thundery_showers_icon.resize((40, 40))
    showers_icon = Image.open('weather_icons/showers_icon.png')
    showers_icon = showers_icon.resize((40, 40))
    rain_icon = Image.open('weather_icons/light_rain_icon.png')
    rain_icon = rain_icon.resize((40, 40))
    partly_cloudy_icon = Image.open('weather_icons/partly_cloudy_icon.png')
    partly_cloudy_icon = partly_cloudy_icon.resize((40, 40))

    weather_nowcast_icon = {}
    for key, value in weather_situation.items():
        if value == "Thundery Showers":
            weather_nowcast_icon[key] = thundery_showers_icon
        elif value == "Showers":
            weather_nowcast_icon[key] = showers_icon
        elif value == "Rain":
            weather_nowcast_icon[key] = rain_icon
        elif value == "Partly Cloudy":
            weather_nowcast_icon[key] = partly_cloudy_icon

    back_im = im1.copy()
    back_im.paste(weather_nowcast_icon["Tuas"], (112, 295))
    back_im.paste(weather_nowcast_icon["Jurong Island"], (228, 350))
    back_im.paste(weather_nowcast_icon["Western Island"], (310, 456))
    back_im.paste(weather_nowcast_icon["Southern Island"], (481, 452))
    back_im.paste(weather_nowcast_icon["Sentosa"], (462, 389))
    back_im.paste(weather_nowcast_icon["Pioneer"], (186, 263))
    back_im.paste(weather_nowcast_icon["Boon Lay"], (233, 281))
    back_im.paste(weather_nowcast_icon["Jurong East"], (297, 243))
    back_im.paste(weather_nowcast_icon["Clementi"], (336, 261))
    back_im.paste(weather_nowcast_icon["Queenstown"], (381, 305))
    back_im.paste(weather_nowcast_icon["Bukit Merah"], (440, 329))
    back_im.paste(weather_nowcast_icon["City"], (485, 303))
    back_im.paste(weather_nowcast_icon["Kallang"], (516, 267))
    back_im.paste(weather_nowcast_icon["Marine Parade"], (566, 295))
    back_im.paste(weather_nowcast_icon["Geylang"], (555, 257))
    back_im.paste(weather_nowcast_icon["Bedok"], (625, 251))
    back_im.paste(weather_nowcast_icon["Tampines"], (661, 207))
    back_im.paste(weather_nowcast_icon["Changi"], (736, 186))
    back_im.paste(weather_nowcast_icon["Tekong"], (851, 105))
    back_im.paste(weather_nowcast_icon["Jalan Bahar"], (178, 205))
    back_im.paste(weather_nowcast_icon["Jurong West"], (240, 217))
    back_im.paste(weather_nowcast_icon["Tengah"], (258, 157))
    back_im.paste(weather_nowcast_icon["CCK"], (312, 152))
    back_im.paste(weather_nowcast_icon["Bukit Batok"], (327, 194))
    back_im.paste(weather_nowcast_icon["Bukit Panjang"], (358, 178))
    back_im.paste(weather_nowcast_icon["Bukit Timah"], (391, 244))
    back_im.paste(weather_nowcast_icon["Tanglin"], (430, 275))
    back_im.paste(weather_nowcast_icon["Novena"], (453, 241))
    back_im.paste(weather_nowcast_icon["Toa Payoh"], (506, 228))
    back_im.paste(weather_nowcast_icon["Hougang"], (560, 180))
    back_im.paste(weather_nowcast_icon["Paya Lebar"], (608, 186))
    back_im.paste(weather_nowcast_icon["Pasir Ris"], (667, 164))
    back_im.paste(weather_nowcast_icon["Pulau Ubin"], (688, 104))
    back_im.paste(weather_nowcast_icon["Western Water Catchment"], (212, 102))
    back_im.paste(weather_nowcast_icon["LCK"], (262, 71))
    back_im.paste(weather_nowcast_icon["Sungei Kadut"], (330, 88))
    back_im.paste(weather_nowcast_icon["Central Water Catchment"], (416, 147))
    back_im.paste(weather_nowcast_icon["Bishan"], (475, 198))
    back_im.paste(weather_nowcast_icon["Serangoon"], (521, 187))
    back_im.paste(weather_nowcast_icon["Sengkang"], (568, 140))
    back_im.paste(weather_nowcast_icon["Punggol"], (590, 110))
    back_im.paste(weather_nowcast_icon["Woodlands"], (384, 55))
    back_im.paste(weather_nowcast_icon["Mandai"], (428, 78))
    back_im.paste(weather_nowcast_icon["Yishun"], (475, 80))
    back_im.paste(weather_nowcast_icon["AMK"], (475, 156))
    back_im.paste(weather_nowcast_icon["Seletar"], (529, 104))
    back_im.paste(weather_nowcast_icon["Sembawang"], (439, 32))

    dm = ImageDraw.Draw(back_im)
    mf = ImageFont.truetype('arial.ttf', 20)
    bbox = dm.textbbox((16, 19), f"Nowcast for {nowcast_time}", font=mf)
    dm.rectangle(bbox, fill="white")
    dm.text((16, 19), f"Nowcast for {nowcast_time}", fill="black", font=mf, bg="white")

    back_im.save("nowcast_image.png", "PNG")
