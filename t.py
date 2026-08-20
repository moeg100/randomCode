from PIL import Image
import argparse
from pathlib import Path

target_w, target_h = 1080, 720
pad_color = (255, 255, 255, 255)

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input image path")
parser.add_argument("-o", "--output", help="Output image path")
args = parser.parse_args()

in_path = Path(args.input)

if not in_path.is_file():
    parser.error(f"Input file not found: {in_path}")

out_path = Path(args.output) if args.output else in_path.with_name(
    f"{in_path.stem}_1080x720.png"
)

with Image.open(in_path) as img:
    img = img.convert("RGBA")

    scale = min(target_w / img.width, target_h / img.height)
    new_size = (
        round(img.width * scale),
        round(img.height * scale)
    )

    resized = img.resize(new_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (target_w, target_h), pad_color)

    x = (target_w - resized.width) // 2
    y = (target_h - resized.height) // 2

    canvas.paste(resized, (x, y), resized)
    canvas.save(out_path, "PNG")

print(f"Saved: {out_path}")