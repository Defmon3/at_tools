import os
import shutil
from pathlib import Path
from zipfile import ZipFile


def print_tree(directory, prefix=''):
    """
    Recursively prints the tree structure of the given directory.
    """
    files = list(directory.iterdir())
    for i, file in enumerate(files):
        end = '└──' if i == len(files) - 1 else '├──'
        print(f"{prefix}{end} {file.name}")
        if file.is_dir():
            extension = '    ' if i == len(files) - 1 else '│   '
            print_tree(file, prefix=prefix + extension)


def extract_zipfiles():
    z_files = list(Path('.').glob('*.zip'))
    print(f"Found {len(z_files)} ZIP files")

    for zf in z_files:
        target_dir = Path(zf.stem)
        with ZipFile(zf) as zip_ref:
            target_dir.mkdir(exist_ok=True)
            zip_ref.extractall(target_dir.name)
            shutil.move(zf, os.path.join(zf.stem, zf))
