#!/usr/bin/env python3


"""
Программа генерирует png-шрифт из ttf-, otf-шрифтов.

Позволяет использовать тени и размытие теней.
"""

import os
import math
import itertools
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def font_generate(
    filename='alphabet.txt',
    font_color: str = "#000000",
    shadow_color: str = "#444444",
    use_shadow: bool | int = True,
    use_blur: bool | int = False,
    font_path_list: None | list = None) -> None:
    """
    Функция генерации png-шрифтов.

    filename: имя/путь файла с алфавитом.

    font_color: цвет шрифта, обычно черный.

    shadow_color: обычно серый.

    use_shadow: использовать тени или нет. По-умолчанию да. Также указывает на дистанцию тени.
    По-умолчанию шрифт перекрывает большую часть тени.

    use_blur: использовать размытие теней или нет. Обычно нет. Если да, то сколько раз.

    font_path_list: список полных путей к файлам со шрифтами ttf, otf и часть имени выходного png-файла.
    """
    if font_path_list is None:
        font_path_list = [
            ("/usr/share/fonts/ubuntu/UbuntuMono-R.ttf",
            "ubuntu-mono"),

            ("/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
            "liberation-mono-regular"),

            ("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-ExtraLight.otf",
            "source-code-pro-extralight"),

            ("/usr/share/fonts/gsfonts/NimbusMonoPS-Regular.otf",
            "nimbus-mono")
        ]

    with open(filename) as f:
        text = f.readline()

        for font_path in font_path_list:
            for font_size in range(14, 50, 2):
                save_dir = f"./fonts/{int(use_shadow)}"
                if not os.path.exists(save_dir):
                    os.mkdir(save_dir)

                save_file = os.path.join(save_dir, f"{font_path[1]}-{font_size}.png")

                percent = 0.15
                real_font_size = math.floor(font_size - (font_size * percent))

                shadow_x = math.ceil(font_size * 0.015625 * (use_shadow if use_shadow else 1))
                shadow_y = math.ceil(font_size * 0.015625 * (use_shadow if use_shadow else 1))

                font = ImageFont.truetype(font_path[0], real_font_size)

                cell_width = int((font_size * 6 + 5) / 10)
                cell_height = font_size

                image_width = cell_width * 96
                image_height = font_size

                background = Image.new('RGBA', (image_width, image_height))

                offset_x = 0
                for char in text:
                    offset = (offset_x, 0)

                    img_char = Image.new("RGBA", (cell_width, cell_height))

                    if use_shadow:
                        for i, j in itertools.product((0, shadow_x), (0, shadow_y)):
                            ImageDraw.Draw(img_char).text((0 + shadow_x, 0 + shadow_y), str(char), font=font, fill=shadow_color)

                        n = 0
                        while n < use_blur:
                            img_char = img_char.filter(ImageFilter.BLUR)
                            n += 1

                    ImageDraw.Draw(img_char).text((0, 0), str(char), font=font, fill=font_color)

                    background.paste(img_char, offset)

                    offset_x += cell_width
                try:
                    background.save(save_file)
                    print(f"[+] Saved\t{save_file}")
                except:
                    print(f"[-] Couldn't save:\t{save_file}")


if __name__ == "__main__":
    font_generate(use_shadow=False)
    font_generate(use_shadow=1)
    font_generate(use_shadow=2)
    font_generate(use_shadow=3)
    font_generate(use_shadow=4)
