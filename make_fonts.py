#!/usr/bin/env python3

import math
import itertools
from PIL import Image, ImageFont, ImageDraw, ImageFilter

font_path_list = [
    ("/usr/share/fonts/ubuntu/UbuntuMono-R.ttf", "ubuntu-mono"),
    ("/usr/share/fonts/liberation/LiberationMono-Regular.ttf", "liberation-mono-regular"),
    ("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-ExtraLight.otf",
     "source-code-pro-extralight"),
    ("/usr/share/fonts/gsfonts/NimbusMonoPS-Regular.otf", "nimbus-mono")
]

font_color = "#000000"  # HEX Black
shadow_color = "#444444"  # HEX Gray

with open('alphabet.txt') as f:
    text = f.readline()

    for font_path in font_path_list:
        for font_size in range(14, 50, 2):
            percent = 0.15
            real_font_size = math.floor(font_size - (font_size * percent))

            shadow_x = math.ceil(font_size * 0.0625)
            shadow_y = math.ceil(font_size * 0.1041)

            font = ImageFont.truetype(font_path[0], real_font_size)

            cell_width = int((font_size * 6 + 5) / 10)
            cell_height = font_size

            image_width = cell_width * 96
            image_height = font_size

            background = Image.new('RGBA', (image_width, image_height))
            background_blur = Image.new('RGBA', (image_width, image_height))

            char_index = 1
            offset_x = 0
            for char in text:
                offset = (offset_x, 0)

                img_char = Image.new("RGBA", (cell_width, cell_height))

                for i, j in itertools.product((-shadow_x, 0, shadow_x), (-shadow_y, 0, shadow_y)):
                    ImageDraw.Draw(img_char).text((0 + i, 0 + j), str(char), font=font, fill=shadow_color)

                img_char = img_char.filter(ImageFilter.BLUR)
                '''
                n = 0
                while n < 3:
                    img_char = img_char.filter(ImageFilter.BLUR)
                    n += 1
                '''

                ImageDraw.Draw(img_char).text((0, 0), str(char), font=font, fill=font_color)

                background.paste(img_char, offset)

                #print(char_index, char, offset)
                offset_x += cell_width
                char_index += 1

            output_file_path = f"./fonts/{font_path[1]}-{font_size}.png"
            try:
                background.save(output_file_path)
                print(f"[+] Saved\t{output_file_path}")
            except:
                print(f"[-] Couldn't save:\t{output_file_path}")
