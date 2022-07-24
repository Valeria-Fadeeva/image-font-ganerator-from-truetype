
from PIL import Image, ImageFont, ImageDraw

# use a truetype font (.ttf)
# font file from fonts.google.com (https://fonts.google.com/specimen/Courier+Prime?query=courier)

font_path_list = [
    ("/usr/share/fonts/ubuntu/UbuntuMono-R.ttf", "ubuntu-mono"),
    ("/usr/share/fonts/liberation/LiberationMono-Regular.ttf", "liberation-mono-regular"),
    ("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-ExtraLight.otf", "source-code-pro-extralight"),
    ("/usr/share/fonts/gsfonts/NimbusMonoPS-Regular.otf", "nimbus-mono")
]

font_color = "#000000"  # HEX Black

text = " !\"#\$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\`abcdefghijklmnopqrstuvwxyz{|}~?"

for font_path in font_path_list:
    for font_size in range(14, 50, 2):
        font = ImageFont.truetype(font_path[0], font_size)

        _, __, width, height = font.getbbox(text)

        img = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(img)

        draw.text((-2, 0), str(text), font=font, fill=font_color)

        try:
            img.save(f"./fonts/{font_path[1]}-{font_size}.png")
        except:
            print(f"[-] Couldn't Save:\t{text}")
