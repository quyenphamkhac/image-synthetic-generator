from os import path
from PIL import Image, ImageDraw
import random
import utils
import json
from pathlib import Path

BG_PATH = "train/backgrounds"
ID_CARD_PATH = "train/id-cards"
OUTPUT_IMAGE_PATH = "export/data_sample"
OUTPUT_MASK_PATH = "export/ground_truth"
GROUND_TRUTH_DIR = "ground_truth"
CARD_SAMPLE_WIDTH = 1280
CARD_SAMPLE_HEIGHT = 814
DATASET_PREFIX = ["DG", "DX", "LG", "LX"]
VERSION = 31
COUNT_ITEM = 30
DELTA = 15
SCALE_MIN = 40
SCALE_MAX = 60


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
    bg_with_color = Image.new("RGB", size=bg_size, color=bg_color)
    return bg_with_color


def choose_new_obj_size(bg_size: tuple[int, int], orig_obj_size: tuple[int, int]) -> tuple[int, int]:
    bg_width, _ = bg_size
    org_obj_width, org_obj_height = orig_obj_size
    scale_ratio = random.randint(SCALE_MIN, SCALE_MAX) / 100
    new_width = int(scale_ratio * bg_width)
    new_height = int((new_width / org_obj_width) * org_obj_height)

    return (new_width, new_height)


def random_rotate_angle() -> int:
    rotate_angle = random.randint(0, 360)
    return rotate_angle


def random_transform_perspective(img: Image.Image) -> Image.Image:
    w, h = img.size
    random_x1 = int(round((random.randint(0, DELTA) / 100) * w))
    random_y1 = int(round((random.randint(0, DELTA) / 100) * h))
    random_x2 = int(round((random.randint(0, DELTA) / 100) * w))
    random_y2 = int(round((random.randint(0, DELTA) / 100) * h))
    random_x3 = int(round((random.randint(0, DELTA) / 100) * w))
    random_y3 = int(round((random.randint(0, DELTA) / 100) * h))
    random_x4 = int(round((random.randint(0, DELTA) / 100) * w))
    random_y4 = int(round((random.randint(0, DELTA) / 100) * h))
    xy = [(0, 0), (w, 0), (w, h), (0, h)]
    new_xy = [(random_x1, random_y1), (w+random_x2, random_y2),
              (w+random_x3, h+random_y3), (random_x4, h+random_y4)]
    M = utils.get_pil_perspective_transform(xy, new_xy)

    delta_x = random_x1 + random_x2 + random_x3 + random_x4
    delta_y = random_y1 + random_y2 + random_y3 + random_y4
    new_img = img.transform(
        (w + delta_x, h + delta_y), Image.Transform.PERSPECTIVE, M, Image.Resampling.BICUBIC)
    return new_img


def generate_synthetic_img(bg_img: Image.Image, obj_img: Image.Image, output_name: str):
    bg_img_size = bg_img.size

    bg_resized = resize_img(img=bg_img, new_size=bg_img_size)
    result_bg = create_color_bg(bg_size=bg_img_size)

    obj_transformed = random_transform_perspective(obj_img)
    rotate_angle = random_rotate_angle()

    obj_rotated = obj_transformed.rotate(rotate_angle, expand=True)

    obj_img_size = choose_new_obj_size(
        bg_size=bg_img_size, orig_obj_size=obj_rotated.size)

    obj_resized = resize_img(img=obj_rotated, new_size=obj_img_size)

    result_mask = get_img_mask(obj_resized)

    x_range, y_range = utils.calculate_coordinates(
        bg_size=bg_img_size, obj_size=obj_resized.size)

    x_min, x_max = x_range
    y_min, y_max = y_range

    coordinates = (int(random.randint(x_min, x_max)),
                   int(random.randint(y_min, y_max)))

    bg_resized.paste(obj_resized, coordinates, mask=obj_resized)
    result_bg.paste(result_mask, coordinates, mask=result_mask)

    output_generated_image_path = path.join(
        OUTPUT_IMAGE_PATH, f"{output_name}.png")
    output_generated_mask = path.join(
        OUTPUT_MASK_PATH, f"{output_name}.png")

    bg_resized.save(output_generated_image_path)
    result_bg.save(output_generated_mask)


def get_ground_truth_quad(file_name: str):
    json_file_path = path.join(GROUND_TRUTH_DIR, f"{file_name}.json")
    json_file = open(json_file_path)
    data = json.load(json_file)
    xy = []
    for xy_item in data["quad"]:
        xy.append(tuple(xy_item))
    json_file.close()
    return xy


def create_data_sample(prefix: str, file_name: str):
    orig_img = Image.open(f"import/{prefix}/{file_name}.tif")
    bg_img = create_color_bg(bg_size=orig_img.size)
    xy = get_ground_truth_quad(f"{prefix}/{file_name}")
    d = ImageDraw.Draw(bg_img)
    d.polygon(xy, fill=(255, 255, 255))
    orig_img.save(f"export/data_sample/{file_name}.png")
    bg_img.save(f"export/ground_truth/{file_name}.png")


def load_dataset():
    for prefix in DATASET_PREFIX:
        for i in range(1, COUNT_ITEM + 1):
            print(f"Loading data sample {i} ...")
            create_data_sample(
                prefix=prefix, file_name=f"{prefix}{VERSION}_{i:02d}")


def generate_bulk_data(num_data: int, bg_path: str, output_prefix: str, obj_path: str):
    bg_images = [str(p) for p in Path(bg_path).glob("*.png")]
    obj_images = [str(p) for p in Path(obj_path).glob("*.png")]

    for i in range(1, num_data + 1):
        print(f"Generating data {i:02d} ...")
        random_bg = random.choice(bg_images)
        random_obj = random.choice(obj_images)
        random_bg_img = Image.open(random_bg)
        random_obj_img = Image.open(random_obj)
        generate_synthetic_img(
            bg_img=random_bg_img, obj_img=random_obj_img, output_name=f"{output_prefix}_{i:02d}")


# bg_img = Image.open("train/backgrounds/table/table_07.png")
# obj_img = Image.open("train/jpn_driver_license/jpn_license_01.png")
# bg_images = [str(p) for p in Path("train/backgrounds/table").glob("*.png")]
# print(str(random.choice(bg_images)))

generate_bulk_data(num_data=5, bg_path="train/backgrounds/table",
                   obj_path="train/jpn_driver_license", output_prefix="TABLE")
