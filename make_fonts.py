#!/usr/bin/env python3

import math
from PIL import Image, ImageFont, ImageDraw

font_path_list = [
    ("/usr/share/fonts/ubuntu/UbuntuMono-R.ttf", "ubuntu-mono"),
    ("/usr/share/fonts/liberation/LiberationMono-Regular.ttf", "liberation-mono-regular"),
    ("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-ExtraLight.otf", "source-code-pro-extralight"),
    ("/usr/share/fonts/gsfonts/NimbusMonoPS-Regular.otf", "nimbus-mono")
]

font_color = "#000000"  # HEX Black

with open('alphabet.txt') as f:
    text = f.readline()

    for font_path in font_path_list:
        for font_size in range(14, 50, 2):
            percent = 0.15
            real_font_size = math.floor(font_size - (font_size * percent))
            font = ImageFont.truetype(font_path[0], real_font_size)

            cell_width = int((font_size * 6 + 5) / 10)
            cell_height = font_size

            image_width = cell_width * 96
            image_height = font_size

            background = Image.new('RGBA', (image_width, image_height))

            char_index = 1
            offset_x = 0
            for char in text:
                offset = (offset_x, 0)
                img = Image.new("RGBA", (cell_width, cell_height))
                draw = ImageDraw.Draw(img)
                draw.text((0, 0), str(char), font=font, fill=font_color)
                background.paste(img, offset)

                #print(char_index, char, offset)
                offset_x += cell_width
                char_index += 1

                output_file_path = f"./fonts/{font_path[1]}-{font_size}.png"
            try:
                background.save(output_file_path)
                print(f"[+] Saved\t{output_file_path}")
            except:
                print(f"[-] Couldn't save:\t{output_file_path}")