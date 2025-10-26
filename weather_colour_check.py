from PIL import Image

colour_check = Image.open("colour_check_image.png")
colour_check = colour_check.convert("RGB")

colour_dict = {}
#
# colour_dict["heavy_tsra_colour"] = colour_check.getpixel((488, 162))
# colour_dict["tsra_colour"] = colour_check.getpixel((515, 264))
# colour_dict["light_tsra_colour"] = colour_check.getpixel((194, 455))
# colour_dict["showers_colour"] = colour_check.getpixel((102, 442))
# colour_dict["light_showers_colour"] = colour_check.getpixel((435, 179))
# colour_dict["partly_cloudy"] = (255, 255, 255)

colour_dict["heavy_tsra_colour"] = (255, 0, 50)
colour_dict["tsra_colour"] = (255, 0, 0)
colour_dict["light_tsra_colour"] = (255, 50, 0)
colour_dict["showers_colour"] = (255, 100, 0)
colour_dict["light_showers_colour"] = (255, 255, 0)
colour_dict["partly_cloudy"] = (255, 255, 255)
