#!/usr/bin/env python3
import argparse
import os
import signal
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, simpledialog
except ImportError:
    tk = None


def which_or_raise(cmd: str) -> str:
    path = shutil.which(cmd)
    if not path:
        raise RuntimeError(
            f"Required tool '{cmd}' was not found in PATH. Install it and try again."
        )
    return path


def is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def root_cmd(cmd):
    if is_root():
        return list(map(str, cmd))

    which_or_raise("sudo")
    return ["sudo", *map(str, cmd)]


def run(cmd, capture_output=False):
    cmd = list(map(str, cmd))

    print("\nRunning:")
    print("  " + " ".join(subprocess.list2cmdline([x]) for x in cmd))

    return subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def pick_file_gui(title="Select input"):
    if tk is None:
        return None

    root = tk.Tk()
    root.withdraw()

    try:
        selected = filedialog.askopenfilename(
            title=title,
            filetypes=[("All files", "*.*")],
        )
        return selected or None
    finally:
        root.destroy()


def ask_choice_gui(title, prompt, options):
    if tk is None:
        return None

    root = tk.Tk()
    root.withdraw()

    try:
        answer = simpledialog.askstring(
            title,
            prompt + "\nOptions: " + ", ".join(options),
        )
        return answer.strip().lower() if answer else None
    finally:
        root.destroy()


def ffmpeg_repair_mp4(input_path: Path, output_path: Path) -> str:
    which_or_raise("ffmpeg")

    input_path = input_path.expanduser().resolve()
    output_path = output_path.expanduser().resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"Input MP4 not found: {input_path}")

    if input_path == output_path:
        raise ValueError("Input and output MP4 must be different files.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    remux_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-err_detect",
        "ignore_err",
        "-i",
        str(input_path),
        "-map",
        "0",
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    try:
        run(remux_cmd)
        return "remux_ok"
    except subprocess.CalledProcessError as remux_error:
        print(
            "\nStream-copy remux failed; trying a full re-encode.",
            file=sys.stderr,
        )

        try:
            output_path.unlink()
        except FileNotFoundError:
            pass

        reencoded = output_path.with_name(
            output_path.stem + "_reencoded" + output_path.suffix
        )

        try:
            reencode_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "warning",
                "-y",
                "-err_detect",
                "ignore_err",
                "-i",
                str(input_path),
                "-map",
                "0:v:0?",
                "-map",
                "0:a:0?",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                str(reencoded),
            ]

            run(reencode_cmd)

            reencoded.replace(output_path)
            return "reencode_ok"

        except Exception:
            try:
                reencoded.unlink()
            except FileNotFoundError:
                pass

            raise RuntimeError(
                "Both MP4 repair attempts failed. "
                "The source may be too damaged for ffmpeg to decode."
            ) from remux_error


def setup_loop_from_img(img_path: Path) -> str:
    which_or_raise("losetup")

    img_path = img_path.expanduser().resolve()

    if not img_path.is_file():
        raise FileNotFoundError(f"Image not found: {img_path}")

    cmd = root_cmd([
        "losetup",
        "--find",
        "--partscan",
        "--show",
        str(img_path),
    ])

    result = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
    )

    loop_dev = result.stdout.strip()

    if not loop_dev:
        raise RuntimeError(
            "losetup succeeded but did not return a loop device."
        )

    print(f"Attached image to: {loop_dev}")
    return loop_dev


def cleanup_loop(loop_dev):
    if not loop_dev:
        return

    try:
        which_or_raise("losetup")
    except RuntimeError:
        return

    try:
        run(root_cmd(["losetup", "-d", loop_dev]))
    except subprocess.CalledProcessError as exc:
        print(
            f"Warning: could not detach {loop_dev}: {exc}",
            file=sys.stderr,
        )


def wait_for_path(path: Path, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if path.exists():
            return True
        time.sleep(0.2)

    return path.exists()


def get_device_type(device: str):
    which_or_raise("blkid")

    result = subprocess.run(
        root_cmd([
            "blkid",
            "-o",
            "value",
            "-s",
            "TYPE",
            device,
        ]),
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return value or None


def is_mounted(device: str) -> bool:
    if not shutil.which("findmnt"):
        return False

    result = subprocess.run(
        root_cmd(["findmnt", "-rn", "-S", device]),
        text=True,
        capture_output=True,
    )

    return result.returncode == 0 and bool(result.stdout.strip())


def choose_partition(loop_dev: str, partition_number):
    if partition_number is not None:
        part = Path(f"{loop_dev}p{partition_number}")

        if not wait_for_path(part):
            raise RuntimeError(
                f"Partition device not found: {part}"
            )

        return str(part)

    for n in range(1, 129):
        part = Path(f"{loop_dev}p{n}")

        if wait_for_path(part, timeout=0.5):
            fs_type = get_device_type(str(part))

            if fs_type == "ext4":
                return str(part)

    fs_type = get_device_type(loop_dev)

    if fs_type == "ext4":
        return loop_dev

    raise RuntimeError(
        f"Could not find an ext4 partition in {loop_dev}, "
        f"and the loop device itself is not recognized as ext4."
    )


def ext4_recover_from_device(
    partition_dev: str,
    output_dir: Path,
    restore_all: bool,
    restore_file: str | None,
) -> Path:
    which_or_raise("extundelete")

    output_dir.mkdir(parents=True, exist_ok=True)

    out_base = output_dir / "extundelete_output"
    out_base.mkdir(parents=True, exist_ok=True)

    if is_mounted(partition_dev):
        raise RuntimeError(
            f"{partition_dev} appears to be mounted. "
            "Unmount it before recovery."
        )

    if restore_all and restore_file:
        raise ValueError(
            "Choose either --restore-all or --restore-file, not both."
        )

    if not restore_all and not restore_file:
        restore_all = True

    cmd = root_cmd([
        "extundelete",
        partition_dev,
        "--output-dir",
        str(out_base),
    ])

    if restore_file:
        cmd.extend([
            "--restore-file",
            restore_file,
        ])
    else:
        cmd.append("--restore-all")

    run(cmd)

    return out_base


ACTIVE_LOOP_DEVICE = None


def handle_signal(signum, _frame):
    global ACTIVE_LOOP_DEVICE

    print(
        f"\nReceived signal {signum}; cleaning up...",
        file=sys.stderr,
    )

    cleanup_loop(ACTIVE_LOOP_DEVICE)
    ACTIVE_LOOP_DEVICE = None

    raise SystemExit(128 + signum)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Repair MP4 files or recover deleted files from an ext4 "
            "filesystem image."
        )
    )

    parser.add_argument(
        "--input",
        "-i",
        help="Input MP4 or ext4 image.",
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=[
            "recover-ext4-img",
            "repair-mp4",
        ],
        help="Operation to perform.",
    )

    parser.add_argument(
        "--out",
        "-o",
        default="./recovered_output",
        help="Output directory (default: ./recovered_output).",
    )

    parser.add_argument(
        "--output-mp4",
        help="Output MP4 path for repair-mp4.",
    )

    parser.add_argument(
        "--partition",
        type=int,
        help="Partition number inside the image, e.g. 1 for /dev/loopXp1.",
    )

    restore_group = parser.add_mutually_exclusive_group()

    restore_group.add_argument(
        "--restore-all",
        action="store_true",
        help="Restore all recoverable deleted files.",
    )

    restore_group.add_argument(
        "--restore-file",
        help="Restore one specific deleted file path from ext4.",
    )

    return parser


def main():
    global ACTIVE_LOOP_DEVICE

    parser = build_parser()
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    input_path = args.input
    operation = args.type

    if (not input_path or not operation) and tk is not None:
        if not input_path:
            input_path = pick_file_gui(
                "Select input (MP4 or ext4 image)"
            )

        if not operation:
            operation = ask_choice_gui(
                "Choose action",
                "Recover ext4 image or repair MP4?",
                [
                    "recover-ext4-img",
                    "repair-mp4",
                ],
            )

    if not input_path or not operation:
        parser.error(
            "Provide --input and --type, or run where tkinter is available "
            "for the GUI fallback."
        )

    input_path_obj = Path(input_path).expanduser().resolve()

    if not input_path_obj.exists():
        raise FileNotFoundError(input_path_obj)

    if operation == "repair-mp4":
        output_mp4 = (
            Path(args.output_mp4).expanduser().resolve()
            if args.output_mp4
            else out_dir / f"{input_path_obj.stem}_fixed.mp4"
        )

        if input_path_obj == output_mp4:
            raise ValueError("Refusing to overwrite the input MP4.")

        status = ffmpeg_repair_mp4(
            input_path_obj,
            output_mp4,
        )

        print(
            f"\nMP4 repair complete:\n"
            f"  Output: {output_mp4}\n"
            f"  Method: {status}"
        )

        return 0

    if operation == "recover-ext4-img":
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        if args.partition is not None and args.partition < 1:
            raise ValueError(
                "--partition must be 1 or greater."
            )

        loop_dev = None

        try:
            loop_dev = setup_loop_from_img(input_path_obj)
            ACTIVE_LOOP_DEVICE = loop_dev

            partition_dev = choose_partition(
                loop_dev,
                args.partition,
            )

            print(f"\nUsing recovery device: {partition_dev}")

            fs_type = get_device_type(partition_dev)

            if fs_type != "ext4":
                raise RuntimeError(
                    f"{partition_dev} does not appear to be ext4 "
                    f"(detected type: {fs_type!r})."
                )

            if is_mounted(partition_dev):
                raise RuntimeError(
                    f"{partition_dev} is mounted. "
                    "Recovery must be performed on an unmounted filesystem."
                )

            result_dir = ext4_recover_from_device(
                partition_dev=partition_dev,
                output_dir=out_dir,
                restore_all=args.restore_all,
                restore_file=args.restore_file,
            )

            print(
                f"\next4 recovery complete.\n"
                f"  Recovered files: {result_dir}"
            )

            return 0

        finally:
            cleanup_loop(loop_dev)
            ACTIVE_LOOP_DEVICE = None

    raise RuntimeError(f"Unsupported operation: {operation}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
