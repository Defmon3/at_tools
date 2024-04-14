import argparse
import os
import shutil
from pathlib import Path
from zipfile import ZipFile


def extract_zipfiles(target: str = '.'):
    z_files = list(Path(target).glob('*.zip'))
    print(f"Found {len(z_files)} ZIP files")

    for zf in z_files:
        target_dir = Path(zf.stem)
        with ZipFile(zf) as zip_ref:
            target_dir.mkdir(exist_ok=True)
            zip_ref.extractall(target_dir.name)
            shutil.move(zf, os.path.join(zf.stem, zf))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract ZIP files in the current directory.")
    parser.add_argument('target', metavar='target', type=str, nargs='?', default='.', help='Target directory')
    args = parser.parse_args()

    extract_zipfiles(args.target)
