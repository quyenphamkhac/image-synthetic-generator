from PIL import Image
from pathlib import Path


image_names = [str(p) for p in Path('./import/train/').glob('*.jpg')]

for idx, image_name in enumerate(image_names):
    print(image_name)
    img_jpg = Image.open(image_name)
    img_jpg.save(f'./import/train_png/{idx:02d}.png')
