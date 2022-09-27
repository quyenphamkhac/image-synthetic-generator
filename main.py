from os import path
from PIL import Image
import random
import utils

BG_WIDH = 1060
BG_HEIGHT = 706
BG_PATH = 'train/backgrounds'
ID_CARD_PATH = 'train/id-cards'
OUTPUT_IMAGE_PATH = 'train/generated-images'
OUTPUT_MASK_PATH = 'train/masks'
CARD_SAMPLE_WIDTH = 1280
CARD_SAMPLE_HEIGHT = 814


def load_bg_img(bg_name: str) -> Image.Image:
    """Load background image using file name
    Args:
        background_name (str): background image name
    """

    bg_path = path.join(BG_PATH, f"{bg_name}.jpeg")
    bg_img = Image.open(bg_path)

    return bg_img


def load_obj_img(obj_name: str) -> Image.Image:
    """Load id card image using file name
    Args:
       id_card_name (str): id card image name
    """

    obj_img_path = path.join(ID_CARD_PATH, f"{obj_name}.png")
    obj_img = Image.open(obj_img_path)
    return obj_img


def get_img_mask(img: Image.Image) -> Image.Image:
    _, _, _, mask = img.split()
    return mask


def resize_img(img: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    new_img = img.resize(new_size)
    return new_img


def transform_img(img: Image.Image) -> Image.Image:
    return


def show_img(img: Image.Image) -> None:
    img.show()


def create_color_bg(bg_size: tuple[int, int], bg_color: tuple[int, int, int] = (0, 0, 0)) -> Image.Image:
    bg_with_color = Image.new('RGB', size=bg_size, color=bg_color)
    return bg_with_color


def generate_synthetic_img(bg_img: Image.Image, obj_img: Image.Image):
    bg_img_size = (BG_WIDH, BG_HEIGHT)
    obj_img_size = (int(CARD_SAMPLE_WIDTH / 4), int(CARD_SAMPLE_HEIGHT / 4))

    bg_resized = resize_img(image=bg_img, new_size=bg_img_size)
    result_bg = create_color_bg(bg_size=bg_img_size)

    obj_resized = resize_img(image=obj_img, new_size=obj_img_size)
    result_mask = get_img_mask(obj_resized)

    x_range, y_range = utils.calculate_coordinates(
        bg_size=bg_img_size, obj_size=obj_img_size)

    x_min, x_max = x_range
    y_min, y_max = y_range

    coordinates = (int(random.randint(x_min, x_max)),
                   int(random.randint(y_min, y_max)))

    bg_resized.paste(obj_resized, coordinates, mask=obj_resized)
    result_bg.paste(result_mask, coordinates, mask=result_mask)

    current_time_ms = utils.current_ms()
    output_generated_image_path = path.join(
        OUTPUT_IMAGE_PATH, f"{current_time_ms}.jpeg")
    output_generated_mask = path.join(
        OUTPUT_MASK_PATH, f"{current_time_ms}.png")

    bg_resized.save(output_generated_image_path)
    result_bg.save(output_generated_mask)


img = Image.open('train/id-cards/jpn-license-1.png')
m = -0.5
w, h = img.size
xshift = abs(m) * img.width
shear_x = int(round(xshift))
new_w = w + int(round(xshift))
M = utils.get_pil_perspective_transform([(0, 0), (w, 0), (w, h), (0, h)], [
                                        (0, 100), (w, 0), (new_w, h-100), (shear_x, h)])

img_transformed = img.transform((new_w, h), Image.Transform.PERSPECTIVE,
                                M, Image.Resampling.BICUBIC)
img_transformed.show()
