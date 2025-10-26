import numpy as np
from PIL import Image
import cv2


def location_grids(weather_image):
    # overlay onto SG map
    background = Image.open("B&Wbg.png")
    background = background.convert("RGBA")
    # Set figure
    overlay = weather_image
    overlay = overlay.convert("RGBA")
    size = background.size
    overlay = overlay.resize(size)
    background.paste(overlay, (0, 0), overlay)
    background.save("overlay_image.png", 'PNG')

    # Load the image
    im = cv2.imread('overlay_image.png')

    tuas_grids = []

    for i in range(0, 1):
        for j in range(0, 4):
            tuas_grids.append(tuple(np.median(im[336 + 28 * j:364 + 28 * j, 74 + 37 * i:111 + 37 * i],
                                              axis=(0, 1)))
                              )

    for i in range(0, 2):
        for j in range(0, 6):
            tuas_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 111 + 37 * i:148 + 37 * i], axis=(0, 1))))

    neighborhood_grids = {"Tuas": tuas_grids}

    jurong_island_grids = []

    for i in range(0, 5):
        for j in range(0, 5):
            jurong_island_grids.append(
                tuple(np.median(im[308 + 28 * j:336 + 28 * j, 148 + 37 * i:185 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Jurong Island"] = jurong_island_grids

    western_island_grids = []

    for i in range(0, 5):
        for j in range(0, 5):
            western_island_grids.append(
                tuple(np.median(im[392 + 28 * j:420 + 28 * j, 259 + 37 * i:296 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Western Island"] = western_island_grids

    southern_island_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            southern_island_grids.append(
                tuple(np.median(im[420 + 28 * j:448 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Southern Island"] = southern_island_grids

    sentosa_grids = []

    for i in range(0, 3):
        for j in range(0, 3):
            sentosa_grids.append(tuple(np.median(im[364 + 28 * j:392 + 28 * j, 407 + 37 * i:444 + 37 * i],
                                                 axis=(0, 1)))
                                 )

    neighborhood_grids["Sentosa"] = sentosa_grids

    pioneer_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            pioneer_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 148 + 37 * i:185 + 37 * i],
                                                 axis=(0, 1)))
                                 )

    pioneer_grids.append(tuple(np.median(im[222:259, 252:280], axis=(0, 1))))

    neighborhood_grids["Pioneer"] = pioneer_grids

    boon_lay_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            boon_lay_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 222 + 37 * i:259 + 37 * i],
                                                  axis=(0, 1))))

    neighborhood_grids["Boon Lay"] = boon_lay_grids

    jurong_east_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            jurong_east_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 259 + 37 * i:296 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Jurong East"] = jurong_east_grids

    clementi_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            clementi_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 296 + 37 * i:333 + 37 * i],
                                                  axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            clementi_grids.append(tuple(np.median(im[280 + 28 * j:308 + 28 * j, 333 + 37 * i:370 + 37 * i],
                                                  axis=(0, 1))))

    neighborhood_grids["Clementi"] = clementi_grids

    queenstown_grids = []

    for i in range(0, 1):
        for j in range(0, 3):
            queenstown_grids.append(
                tuple(np.median(im[308 + 28 * j:336 + 28 * j, 333 + 37 * i:370 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 4):
            queenstown_grids.append(
                tuple(np.median(im[280 + 28 * j:308 + 28 * j, 370 + 37 * i:407 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 3):
            queenstown_grids.append(
                tuple(np.median(im[280 + 28 * j:308 + 28 * j, 407 + 37 * i:444 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Queenstown"] = queenstown_grids

    bukit_merah_grids = []

    for i in range(0, 3):
        for j in range(0, 3):
            bukit_merah_grids.append(
                tuple(np.median(im[308 + 28 * j:336 + 28 * j, 407 + 37 * i:444 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bukit Merah"] = bukit_merah_grids

    city_grids = []

    for i in range(0, 3):
        for j in range(0, 3):
            city_grids.append(tuple(np.median(im[280 + 28 * j:308 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    neighborhood_grids["City"] = city_grids

    kallang_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            kallang_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 481 + 37 * i:518 + 37 * i],
                                                 axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            kallang_grids.append(tuple(np.median(im[280 + 28 * j:308 + 28 * j, 555 + 37 * i:592 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Kallang"] = kallang_grids

    marine_parade_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            marine_parade_grids.append(
                tuple(np.median(im[280 + 28 * j:308 + 28 * j, 518 + 37 * i:555 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Marine Parade"] = marine_parade_grids

    geylang_grids = []

    for i in range(0, 3):
        for j in range(0, 3):
            geylang_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 518 + 37 * i:555 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Geylang"] = geylang_grids

    bedok_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            bedok_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 592 + 37 * i:629 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            bedok_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 666 + 37 * i:703 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bedok"] = bedok_grids

    tampines_grids = []

    for i in range(0, 1):
        for j in range(0, 3):
            tampines_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 629 + 37 * i:666 + 37 * i],
                                                  axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 4):
            tampines_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 666 + 37 * i:703 + 37 * i],
                                                  axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            tampines_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 703 + 37 * i:740 + 37 * i],
                                                  axis=(0, 1))))

    neighborhood_grids["Tampines"] = tampines_grids

    changi_grids = []

    for i in range(0, 4):
        for j in range(0, 5):
            changi_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 703 + 37 * i:740 + 37 * i], axis=(0, 1))))

    for i in range(0, 2):
        for j in range(0, 1):
            changi_grids.append(tuple(np.median(im[140 + 28 * j:168 + 28 * j, 703 + 37 * i:740 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Changi"] = changi_grids

    tekong_grids = []

    for i in range(0, 4):
        for j in range(0, 5):
            tekong_grids.append(tuple(np.median(im[56 + 28 * j:84 + 28 * j, 777 + 37 * i:814 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Tekong"] = tekong_grids

    jalan_bahar_grids = []

    for i in range(0, 4):
        for j in range(0, 3):
            jalan_bahar_grids.append(
                tuple(np.median(im[168 + 28 * j:196 + 28 * j, 111 + 37 * i:148 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Jalan Bahar"] = jalan_bahar_grids

    jurong_west_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            jurong_west_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 185 + 37 * i:222 + 37 * i], axis=(0, 1))))

    for i in range(0, 2):
        for j in range(0, 1):
            jurong_west_grids.append(
                tuple(np.median(im[196 + 28 * j:224 + 28 * j, 222 + 37 * i:259 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Jurong West"] = jurong_west_grids

    tengah_grids = []

    for i in range(0, 3):
        for j in range(0, 4):
            tengah_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 222 + 37 * i:259 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            tengah_grids.append(tuple(np.median(im[84 + 28 * j:112 + 28 * j, 296 + 37 * i:333 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Tengah"] = tengah_grids

    cck_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            cck_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 296 + 37 * i:333 + 37 * i], axis=(0, 1))))

    neighborhood_grids["CCK"] = cck_grids

    bukit_batok_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            bukit_batok_grids.append(
                tuple(np.median(im[168 + 28 * j:196 + 28 * j, 296 + 37 * i:333 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bukit Batok"] = bukit_batok_grids

    bukit_panjang_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            bukit_panjang_grids.append(
                tuple(np.median(im[140 + 28 * j:168 + 28 * j, 333 + 37 * i:370 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            bukit_panjang_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 370 + 37 * i:407 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bukit Panjang"] = bukit_panjang_grids

    bukit_timah_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            bukit_timah_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 370 + 37 * i:407 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            bukit_timah_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 333 + 37 * i:370 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bukit Timah"] = bukit_timah_grids

    tanglin_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            tanglin_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 407 + 37 * i:444 + 37 * i],
                                                 axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            tanglin_grids.append(tuple(np.median(im[308 + 28 * j:336 + 28 * j, 444 + 37 * i:481 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Tanglin"] = tanglin_grids

    novena_grids = []

    for i in range(0, 2):
        for j in range(0, 1):
            novena_grids.append(tuple(np.median(im[252 + 28 * j:280 + 28 * j, 481 + 37 * i:518 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            novena_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Novena"] = novena_grids

    toa_payoh_grids = []

    for i in range(0, 3):
        for j in range(0, 1):
            toa_payoh_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 481 + 37 * i:518 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Toa Payoh"] = toa_payoh_grids

    hougang_grids = []

    for i in range(0, 1):
        for j in range(0, 4):
            hougang_grids.append(tuple(np.median(im[140 + 28 * j:168 + 28 * j, 555 + 37 * i:592 + 37 * i],
                                                 axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 2):
            hougang_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 592 + 37 * i:629 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Hougang"] = hougang_grids

    paya_lebar_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            paya_lebar_grids.append(
                tuple(np.median(im[168 + 28 * j:196 + 28 * j, 592 + 37 * i:629 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            paya_lebar_grids.append(
                tuple(np.median(im[196 + 28 * j:224 + 28 * j, 555 + 37 * i:592 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            paya_lebar_grids.append(
                tuple(np.median(im[224 + 28 * j:252 + 28 * j, 592 + 37 * i:629 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Paya Lebar"] = paya_lebar_grids

    pasir_ris_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            pasir_ris_grids.append(
                tuple(np.median(im[140 + 28 * j:168 + 28 * j, 629 + 37 * i:666 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            pasir_ris_grids.append(
                tuple(np.median(im[140 + 28 * j:168 + 28 * j, 592 + 37 * i:629 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            pasir_ris_grids.append(
                tuple(np.median(im[196 + 28 * j:224 + 28 * j, 703 + 37 * i:740 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Pasir Ris"] = pasir_ris_grids

    pulau_ubin_grids = []

    for i in range(0, 4):
        for j in range(0, 2):
            pulau_ubin_grids.append(
                tuple(np.median(im[84 + 28 * j:112 + 28 * j, 629 + 37 * i:666 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Pulau Ubin"] = pulau_ubin_grids

    wwc_grids = []

    for i in range(0, 3):
        for j in range(0, 4):
            wwc_grids.append(tuple(np.median(im[84 + 28 * j:112 + 28 * j, 148 + 37 * i:185 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Western Water Catchment"] = wwc_grids

    lck_grids = []

    for i in range(0, 3):
        for j in range(0, 3):
            lck_grids.append(tuple(np.median(im[28 + 28 * j:56 + 28 * j, 222 + 37 * i:259 + 37 * i], axis=(0, 1))))

    neighborhood_grids["LCK"] = lck_grids

    sungei_kadut_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            sungei_kadut_grids.append(
                tuple(np.median(im[56 + 28 * j:84 + 28 * j, 296 + 37 * i:333 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            sungei_kadut_grids.append(
                tuple(np.median(im[140 + 28 * j:168 + 28 * j, 333 + 37 * i:370 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Sungei Kadut"] = sungei_kadut_grids

    cwc_grids = []

    for i in range(0, 2):
        for j in range(0, 4):
            cwc_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 370 + 37 * i:407 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 4):
            cwc_grids.append(tuple(np.median(im[140 + 28 * j:168 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Central Water Catchment"] = cwc_grids

    bishan_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            bishan_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            bishan_grids.append(tuple(np.median(im[224 + 28 * j:252 + 28 * j, 481 + 37 * i:518 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Bishan"] = bishan_grids

    serangoon_grids = []

    for i in range(0, 1):
        for j in range(0, 4):
            serangoon_grids.append(
                tuple(np.median(im[140 + 28 * j:168 + 28 * j, 518 + 37 * i:555 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Serangoon"] = serangoon_grids

    sengkang_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            sengkang_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 518 + 37 * i:555 + 37 * i],
                                                  axis=(0, 1))))

    neighborhood_grids["Sengkang"] = sengkang_grids

    punggol_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            punggol_grids.append(tuple(np.median(im[84 + 28 * j:112 + 28 * j, 555 + 37 * i:592 + 37 * i],
                                                 axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            punggol_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 629 + 37 * i:666 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Punggol"] = punggol_grids

    woodlands_grids = []

    for i in range(0, 2):
        for j in range(0, 3):
            woodlands_grids.append(tuple(np.median(im[28 + 28 * j:56 + 28 * j, 370 + 37 * i:407 + 37 * i],
                                                   axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            woodlands_grids.append(tuple(np.median(im[56 + 28 * j:84 + 28 * j, 333 + 37 * i:370 + 37 * i],
                                                   axis=(0, 1))))

    neighborhood_grids["Woodlands"] = woodlands_grids

    mandai_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            mandai_grids.append(tuple(np.median(im[56 + 28 * j:84 + 28 * j, 407 + 37 * i:444 + 37 * i],
                                                axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            mandai_grids.append(tuple(np.median(im[84 + 28 * j:112 + 28 * j, 370 + 37 * i:407 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Mandai"] = mandai_grids

    yishun_grids = []

    for i in range(0, 2):
        for j in range(0, 1):
            yishun_grids.append(tuple(np.median(im[28 + 28 * j:56 + 28 * j, 481 + 37 * i:518 + 37 * i], axis=(0, 1))))

    for i in range(0, 3):
        for j in range(0, 2):
            yishun_grids.append(tuple(np.median(im[56 + 28 * j:84 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    for i in range(0, 3):
        for j in range(0, 1):
            yishun_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 407 + 37 * i:444 + 37 * i], axis=(0, 1))))

    neighborhood_grids["Yishun"] = yishun_grids

    amk_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            amk_grids.append(tuple(np.median(im[140 + 28 * j:168 + 28 * j, 444 + 37 * i:481 + 37 * i], axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            amk_grids.append(tuple(np.median(im[168 + 28 * j:196 + 28 * j, 518 + 37 * i:555 + 37 * i], axis=(0, 1))))

    neighborhood_grids["AMK"] = amk_grids

    seletar_grids = []

    for i in range(0, 2):
        for j in range(0, 2):
            seletar_grids.append(tuple(np.median(im[84 + 28 * j:112 + 28 * j, 518 + 37 * i:555 + 37 * i],
                                                 axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            seletar_grids.append(tuple(np.median(im[112 + 28 * j:140 + 28 * j, 481 + 37 * i:518 + 37 * i],
                                                 axis=(0, 1))))

    neighborhood_grids["Seletar"] = seletar_grids

    sembawang_grids = []

    for i in range(0, 3):
        for j in range(0, 2):
            sembawang_grids.append(tuple(np.median(im[0 + 28 * j:28 + 28 * j, 407 + 37 * i:444 + 37 * i],
                                                   axis=(0, 1))))

    for i in range(0, 1):
        for j in range(0, 1):
            sembawang_grids.append(tuple(np.median(im[56 + 28 * j:84 + 28 * j, 444 + 37 * i:481 + 37 * i],
                                                   axis=(0, 1))))

    neighborhood_grids["Sembawang"] = sembawang_grids

    return neighborhood_grids
