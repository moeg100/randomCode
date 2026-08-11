from pathlib import Path

INPUT_FOLDER = input("Enter the path : ")

folder = Path(INPUT_FOLDER).expanduser().resolve()

if not folder.exists() or not folder.is_dir():
    raise FileNotFoundError(INPUT_FOLDER)

files = sorted(
    [f for f in folder.iterdir() if f.is_file()],
    key=lambda f: f.name.lower()
)


number = 1

for file in files:
    suffix = "".join(file.suffixes)
    while (folder / f"{number}{file.suffix}").exists():
        number += 1

    destination = folder / f"{number}{file.suffix}"

    if file != destination:
        file.rename(destination)

    number += 1
