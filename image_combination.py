from PIL import Image

timings = ["0720", "0730", "0740", "0750", "0800", "0810", "0820", "0830", "0840", "0850", "0900",
           "0910", "0920", "0930", "0940", "0950", "1000", "1010", "1020", "1030", "1040", "1050",
           "1100", "1110", "1120", "1130", "1140", "1150", "1200"
           ]

for time in timings:
    image_top = Image.open(f"Nowcast Output/nowcast_20230719{time}.png")
    image_bottom = Image.open(f"Rain_areas_for_comparison/rain_areas_2023_07_19_{time}.png")
    images_list = [image_top, image_bottom]

    # If you're using an older version of Pillow, you might have to use .size[0] instead of .width
    # and later on, .size[1] instead of .height
    min_img_width = min(i.width for i in images_list)

    total_height = 0
    for i, img in enumerate(images_list):
        # If the image is larger than the minimum width, resize it
        if img.width > min_img_width:
            images_list[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)))
        total_height += images_list[i].height

    # I have picked the mode of the first image to be generic. You may have other ideas
    # Now that we know the total height of all of the resized images, we know the height of our final image
    img_merge = Image.new(images_list[0].mode, (min_img_width, total_height))
    y = 0
    for img in images_list:
        img_merge.paste(img, (0, y))

        y += img.height
    img_merge.save(f"Combined Images/combined_image_20230719{time}.png", "PNG")

