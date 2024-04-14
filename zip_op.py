import argparse
from pathlib import Path
from shutil import move
from zipfile import ZipFile


def extract_zip_files(target: Path):
    z_files = list(target.glob('*.zip'))
    print(f"Found {len(z_files)} ZIP files")

    for zf in z_files:
        target_dir = target / zf.stem
        with ZipFile(zf) as zip_ref:
            target_dir.mkdir(exist_ok=True)
            zip_ref.extractall(target_dir)
            move(zf, target_dir)


def main():
    parser = argparse.ArgumentParser(description="Extract ZIP files in the specified directory.")
    parser.add_argument('target', metavar='TARGET', type=Path, nargs='?', default='.',
                        help='Target directory where ZIP files are located and extracted to')
    args = parser.parse_args()

    extract_zip_files(args.target)


if __name__ == "__main__":
    main()
