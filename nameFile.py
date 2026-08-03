from pathlib import Path

INPUT_FOLDER = r"~/" # Here specifiy the path

folder = Path(INPUT_FOLDER)

if not folder.exists():
    raise FileNotFoundError(INPUT_FOLDER)

files = sorted(
    [f for f in folder.iterdir() if f.is_file()],
    key=lambda f: f.name.lower()
)

number = 1

for file in files:
    while (folder / f"{number}{file.suffix}").exists():
        number += 1

    destination = folder / f"{number}{file.suffix}"

    if file != destination:
        file.rename(destination)

    number += 1