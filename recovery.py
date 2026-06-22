#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, simpledialog
except ImportError:
    tk = None

def which_or_raise(cmd):
    p = shutil.which(cmd)
    if not p:
        raise RuntimeError(f"Missing required tool: {cmd}. Install it and re-run.")
    return p

def run(cmd):
    print("\nRunning:\n  " + " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)

def pick_file_gui(title="Select input"):
    if tk is None:
        return None
    root = tk.Tk()
    root.withdraw()
    f = filedialog.askopenfilename(title=title, filetypes=[("All files", "*.*")])
    root.destroy()
    return f or None

def ask_choice_gui(title, prompt, options):
    if tk is None:
        return None
    root = tk.Tk()
    root.withdraw()
    ans = simpledialog.askstring(title, prompt + "\nOptions: " + ", ".join(options))
    root.destroy()
    return ans.strip().lower() if ans else None

def ffmpeg_repair_mp4(input_path: Path, output_path: Path):
    which_or_raise("ffmpeg")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd1 = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning",
        "-err_detect", "ignore_err",
        "-i", str(input_path),
        "-c", "copy",
        "-movflags", "+faststart",
        str(output_path),
    ]
    try:
        run(cmd1)
        return "remux_ok"
    except subprocess.CalledProcessError:
        tmp = output_path.with_name(output_path.stem + "_reencoded" + output_path.suffix)
        cmd2 = [
            "ffmpeg", "-hide_banner", "-loglevel", "warning",
            "-err_detect", "ignore_err",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-movflags", "+faststart",
            str(tmp),
        ]
        run(cmd2)
        tmp.replace(output_path)
        return "reencode_ok"

def setup_loop_from_img(img_path: Path) -> str:
    """
    Turns an image file into a loop device with partition scanning.
    Returns the base loop device path like /dev/loop7.
    """
    which_or_raise("losetup")
    img_path = img_path.expanduser().resolve()
    # Create a loop device with --partscan so /dev/loopXpY appears
    cmd = ["sudo", "losetup", "--find", "--partscan", "--show", str(img_path)]
    res = subprocess.check_output(cmd, text=True).strip()
    return res  # e.g. /dev/loop7

def cleanup_loop(loop_dev: str):
    """
    Detach loop device (best effort).
    """
    which_or_raise("losetup")
    try:
        run(["sudo", "losetup", "-d", loop_dev])
    except subprocess.CalledProcessError:
        pass

def choose_partition(loop_dev: str, partition_number: int | None) -> str:
    """
    If partition_number is provided, use /dev/loopXpY.
    Otherwise pick the first existing /dev/loopXpY.
    """
    base = loop_dev  # /dev/loop7
    if partition_number is not None:
        part = f"{base}p{partition_number}"
        if not Path(part).exists():
            raise RuntimeError(f"Partition device not found: {part}")
        return part

    # Auto-pick: find first p1..p20 that exists
    for n in range(1, 21):
        part = f"{base}p{n}"
        if Path(part).exists():
            return part
    raise RuntimeError("Could not find any partition device /dev/loopXpY (p1..p20).")

def ext4_recover_from_device(partition_dev: str, output_dir: Path, restore_arg: str | None):
    # IMPORTANT:
    # - DO NOT mount the partition read-write during recovery.
    which_or_raise("extundelete")
    output_dir.mkdir(parents=True, exist_ok=True)

    out_base = output_dir / "extundelete_output"
    out_base.mkdir(parents=True, exist_ok=True)

    cmd = ["sudo", "extundelete", partition_dev, "--output-dir", str(out_base)]
    cmd.append(restore_arg if restore_arg else "--restore-all")
    run(cmd)
    return out_base

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Repair MP4 or recover ext4 deleted files from an ext4 image using loop + extundelete.")

    ap.add_argument("--input", "-i", help="MP4 file path OR ext4 image file (.img/.raw/.dd)")
    ap.add_argument("--type", "-t", choices=["recover-ext4-img", "repair-mp4"], help="recover-ext4-img=extundelete, repair-mp4=ffmpeg")
    ap.add_argument("--out", "-o", help="Output directory (default: ./recovered_output)")
    ap.add_argument("--restore", help="extundelete option: --restore-all OR --restore-file /path")
    ap.add_argument("--output-mp4", help="Output mp4 path (only for repair-mp4)")
    ap.add_argument("--partition", type=int, help="Partition number inside the image (e.g., 1 means /dev/loopXp1). If omitted, auto-picks first found.")

    args = ap.parse_args()

    # -------- USAGE EXAMPLES (copy/paste) --------
    #
    # Install dependencies:
    #   sudo apt-get update
    #   sudo apt-get install -y extundelete ffmpeg util-linux
    #
    # 1) Recover ALL deleted files from ext4 image:
    #   sudo python3 recover.py --type recover-ext4-img --input disk.img --out recovered_output
    #
    # 2) If your ext4 is partition #2 inside the image:
    #   sudo python3 recover.py --type recover-ext4-img --input disk.img --out recovered_output --partition 2
    #
    # 3) Recover a specific file:
    #   sudo python3 recover.py --type recover-ext4-img --input disk.img --out recovered_output \
    #     --partition 1 --restore "--restore-file /home/user/notes.txt"
    #
    # 4) Repair a damaged MP4:
    #   python3 recover.py --type repair-mp4 --input bad.mp4 --out recovered_output --output-mp4 fixed.mp4
    #
    # ----------------------------------------------

    out_dir = Path(args.out).expanduser().resolve() if args.out else (Path.cwd() / "recovered_output")
    out_dir.mkdir(parents=True, exist_ok=True)

    input_path = args.input
    mode = args.type

    if (not input_path or not mode) and tk is not None:
        if not input_path:
            input_path = pick_file_gui("Select input (MP4 or image)")
        if not mode:
            choice = ask_choice_gui("Choose action", "Recover ext4 image or repair mp4?", ["recover-ext4-img", "repair-mp4"])
            mode = choice
        if not input_path or not mode:
            print("Missing input or action. Exiting.")
            sys.exit(2)

    if not input_path or not mode:
        raise SystemExit("Provide --input and --type (or run with GUI if tkinter exists).")

    if mode == "repair-mp4":
        p = Path(input_path).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(p)
        which_or_raise("ffmpeg")

        output_mp4 = Path(args.output_mp4).expanduser().resolve() if args.output_mp4 else (out_dir / (p.stem + "_fixed.mp4"))
        status = ffmpeg_repair_mp4(p, output_mp4)
        print(f"MP4 repair done: {output_mp4} ({status})")
        return

    if mode == "recover-ext4-img":
        which_or_raise("extundelete")
        img = Path(input_path).expanduser().resolve()
        if not img.exists():
            raise FileNotFoundError(img)

        restore_arg = args.restore.strip() if args.restore else None

        loop_dev = None
        try:
            loop_dev = setup_loop_from_img(img)  # e.g. /dev/loop7
            part_dev = choose_partition(loop_dev, args.partition)
            print(f"Using partition device: {part_dev}")

            # Recovery
            result_dir = ext4_recover_from_device(part_dev, out_dir, restore_arg=restore_arg)
            print(f"ext4 recovery complete. Check: {result_dir}")
        finally:
            if loop_dev:
                cleanup_loop(loop_dev)
        return

if __name__ == "__main__":
    main()
