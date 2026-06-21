from PIL import Image

in_path = "input.png"      # change me
out_path = "output_1080x720.png"

target_w, target_h = 1080, 720
pad_color = (255, 255, 255)  # white padding

img = Image.open(in_path).convert("RGBA")

# Fit inside target while preserving aspect ratio
scale = min(target_w / img.width, target_h / img.height)
new_w = int(round(img.width * scale))
new_h = int(round(img.height * scale))
resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

# Create canvas and center
canvas = Image.new("RGBA", (target_w, target_h), pad_color + (255,))
x = (target_w - new_w) // 2
y = (target_h - new_h) // 2
canvas.paste(resized, (x, y), resized)

canvas.save(out_path)
print("Saved:", out_path)
