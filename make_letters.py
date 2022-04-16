from PIL import Image, ImageDraw, ImageFont
import shutil
from pathlib import Path
import colorsys
import jinja2
import qrcode

WIDTH = 480
WX = 2
HEIGHT = 640
HX = 2

IMG_WIDTH = WIDTH*WX
IMG_HEIGHT = HEIGHT*HX

TEXT = "NEUF CENT VINGT SIX"
TEXT = "N"

FONT = 'font/texas_bold.otf'

OUT_FOLDER = Path('out')
STATIC_SITE = Path('docs')
TEMPLATES = Path('templates')

if STATIC_SITE.exists():
    shutil.rmtree(STATIC_SITE)
STATIC_SITE.mkdir(parents=True)


def fits(w, h) -> bool:
    return w < IMG_WIDTH and h < IMG_HEIGHT


def font_that_fits(letter: str) -> ImageFont:
    fontsize = 600
    INCREMENT = 200
    while (fits(*ImageFont.truetype(FONT, fontsize).getsize(letter))):
        fontsize += INCREMENT
    print("found size", fontsize-INCREMENT)
    return ImageFont.truetype(FONT, fontsize-INCREMENT)


def offsets_to_center(fnt: ImageFont, letter: str):
    w, h = fnt.getsize(letter)
    off_w = (IMG_WIDTH - w)//2
    off_h = (IMG_HEIGHT - h)//2 - 200
    return off_w, off_h


def letter_color(letter_ix: int):
    h = letter_ix / len(TEXT)
    s, v = 1, 1
    r, g, b = [int(256*val) for val in colorsys.hsv_to_rgb(h, s, v)]
    return r, g, b




def split_letters():
    if OUT_FOLDER.exists():
        shutil.rmtree(OUT_FOLDER)
    OUT_FOLDER.mkdir()
    for letter_ix, letter in enumerate(TEXT):
        img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color=(73, 109, 137))

        fnt = font_that_fits(letter)
        d = ImageDraw.Draw(img)
        offsets = offsets_to_center(fnt, letter)
        color = letter_color(letter_ix)
        d.text(offsets,
            letter, font=fnt, fill=color,
            )

        img.save(OUT_FOLDER/f'{letter_ix}_{letter}.png')

        for i in range(WX):
            for j in range(HX):
                cell_folder = STATIC_SITE/'imgs'/f"{i}{j}"
                cell_folder.mkdir(parents=True, exist_ok=True)
                top = HEIGHT*j
                left = WIDTH*i
                box = (left, top, left+WIDTH, top+HEIGHT)
                cropped_img = img.crop(box)
                cropped_img.save(cell_folder/f'{letter_ix}.png')

names={
    '00': 'mo',
    '01': 'np',
    '10': 'ro',
    '11': 'jet'
}

if STATIC_SITE.exists():
    shutil.rmtree(STATIC_SITE)
STATIC_SITE.mkdir(parents=True)

shutil.copy(TEMPLATES/'main.js', STATIC_SITE)

for i in range(WX):
    for j in range(HX):
        subfolder_name = f"{i}{j}"
        subfolder = STATIC_SITE/subfolder_name
        subfolder.mkdir()
        index_template_string = (Path('templates')/'part.html.j2').read_text('utf8')
        rendered = jinja2.Template(index_template_string).render(num_letters = len(TEXT), subfolder=subfolder_name)

        (STATIC_SITE/f"{names[subfolder_name]}.html").write_text(rendered)

split_letters()


SITE = "https://arpafaucon.github.io/escape_game"
for name in names.values():
    file = OUT_FOLDER / f"{name}.png"
    qr = qrcode.QRCode(box_size=10)
    qr.add_data(f"{SITE}/{name}")
    qr.make()
    img = qr.make_image()
    img.save(str(file))