#!/usr/bin/env python3


"""
Программа генерирует png-шрифт из ttf-, otf-шрифтов.

Позволяет использовать тени и размытие теней.
"""

import os
import sys
import math
import itertools
from tabnanny import check
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def font_generate(
        filename='alphabet.txt',
        font_color: str = "#000000",
        shadow_color: str = "#444444",
        bg_color=(255, 255, 255, 0),
        use_shadow: bool | int = True,
        use_blur: bool | int = False,
        font_path_list: None | list = None,
        save_dir: str | None = None) -> None:
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
        line_max_length = 0
        lines = 0
        text = ''

        for line in f:
            text += line

            line_length = len(line)

            match line[-1]:
                case '\r\n':
                    line_length -= 1
                case '\n':
                    line_length -= 1

            if line_max_length < line_length:
                line_max_length = line_length

            if line.strip():
                lines += 1

        if save_dir is None:
            save_dir = f"fonts/{int(use_shadow)}"

        if not os.path.exists(save_dir):
            check_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            for p in save_dir.split(os.sep):
                check_path = os.path.join(check_path, p)
                print(check_path)

                if not os.path.exists(check_path):
                    os.mkdir(check_path)
                    print('Created', check_path)

        for font_path in font_path_list:
            for font_size in range(14, 50, 2):
                save_file = os.path.join(
                    save_dir, f"{font_path[1]}-{font_size}.png")

                percent = 0.15
                real_font_size = math.floor(font_size - (font_size * percent))

                shadow_x = math.ceil(
                    font_size * 0.015625 * (use_shadow if use_shadow else 1))
                shadow_y = math.ceil(
                    font_size * 0.015625 * (use_shadow if use_shadow else 1))

                font = ImageFont.truetype(font_path[0], real_font_size)

                cell_width = int((font_size * 6 + 5) / 10)
                cell_height = font_size

                image_width = cell_width * line_max_length
                image_height = font_size * lines

                background = Image.new('RGBA', (image_width, image_height))

                offset_x = 0
                offset_y = 0

                for char in text:
                    match char:
                        case '\r\n':
                            offset_x = 0
                            offset_y += cell_height
                            continue
                        case '\n':
                            offset_x = 0
                            offset_y += cell_height
                            continue

                    offset = (offset_x, offset_y)

                    img_char = Image.new(
                        "RGBA", (cell_width, cell_height), color=bg_color)

                    if use_shadow:
                        for i, j in itertools.product((0, shadow_x), (0, shadow_y)):
                            ImageDraw.Draw(img_char).text(
                                (0 + shadow_x, 0 + shadow_y), str(char), font=font, fill=shadow_color)

                        n = 0
                        while n < use_blur:
                            img_char = img_char.filter(ImageFilter.BLUR)
                            n += 1

                    ImageDraw.Draw(img_char).text(
                        (0, 0), str(char), font=font, fill=font_color)

                    background.paste(img_char, offset)

                    offset_x += cell_width
                try:
                    background.save(save_file)
                    print(f"[+] Saved\t{save_file}")
                except:
                    print(f"[-] Couldn't save:\t{save_file}")
