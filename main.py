from os import path
from PIL import Image
import random
import time

BG_WIDH = 1060
BG_HEIGHT = 706
BG_PATH = 'train/backgrounds'
ID_CARD_PATH = 'train/id-cards'
OUTPUT_IMAGE_PATH = 'train/generated-images'
OUTPUT_MASK_PATH = 'train/masks'
CARD_SAMPLE_WIDTH = 1280
CARD_SAMPLE_HEIGHT = 814


def load_background(background_name: str) -> Image.Image:
    """Load background image using file name
    Args:
        background_name (str): background image name
    """

    background_path = path.join(BG_PATH, f"{background_name}.jpeg")
    background_image = Image.open(background_path)

    return background_image


def load_id_card(id_card_name: str) -> Image.Image:
    """Load id card image using file name
    Args:
       id_card_name (str): id card image name
    """

    id_card_file = path.join(ID_CARD_PATH, f"{id_card_name}.png")
    id_card_image = Image.open(id_card_file)
    return id_card_image


def get_image_mask(img: Image.Image) -> Image.Image:
    _, _, _, mask = img.split()
    return mask


def resize_image(image: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    new_image = image.resize(new_size)
    return new_image


def show_image(image: Image.Image) -> None:
    image.show()


def create_new_bg(bg_size: tuple[int, int], bg_color: tuple[int, int, int] = (0, 0, 0)) -> Image.Image:
    new_bg = Image.new('RGB', size=bg_size, color=bg_color)
    return new_bg


def generate_synthetic_image(bg: Image.Image, obj: Image.Image):
    bg_size = (BG_WIDH, BG_HEIGHT)
    obj_size = (int(CARD_SAMPLE_WIDTH / 4), int(CARD_SAMPLE_HEIGHT / 4))

    bg_resized = resize_image(image=bg, new_size=bg_size)
    result_bg = create_new_bg(bg_size=bg_size)

    obj_resized = resize_image(image=obj, new_size=obj_size)
    result_mask = get_image_mask(obj_resized)

    x_range, y_range = calculate_coordinates(
        bg_size=bg_size, obj_size=obj_size)

    x_min, x_max = x_range
    y_min, y_max = y_range

    coordinates = (int(random.randint(x_min, x_max)),
                   int(random.randint(y_min, y_max)))

    bg_resized.paste(obj_resized, coordinates, mask=obj_resized)
    result_bg.paste(result_mask, coordinates, mask=result_mask)

    current_time_ms = current_ms()
    output_generated_image_path = path.join(
        OUTPUT_IMAGE_PATH, f"{current_time_ms}.jpeg")
    output_generated_mask = path.join(
        OUTPUT_MASK_PATH, f"{current_time_ms}.png")

    bg_resized.save(output_generated_image_path)
    result_bg.save(output_generated_mask)


def calculate_coordinates(bg_size: tuple[int, int], obj_size: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    bg_x, bg_y = bg_size
    obj_x, obj_y = obj_size
    x_range = (int(obj_x / 2), int(bg_x - obj_x / 2))
    y_range = (int(obj_y / 2), int(bg_y - obj_y / 2))
    return (x_range, y_range)


def current_ms() -> int:
    return round(time.time() * 1000)


bg = load_background("bg-tablecloth-1")
obj = load_id_card("jpn-drvlic-1")
generate_synthetic_image(bg=bg, obj=obj)
