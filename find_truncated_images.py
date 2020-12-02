import argparse
import sys
from multiprocessing.dummy import Pool
from pathlib import Path

from PIL import Image
from tqdm import tqdm


def filter_image_files(f: Path):
    ext = f.name[len(f.stem):]
    return ext.lower() in ['.jpg', '.png', '.jpeg']


def get_score(f: Path):
    try:
        _ = Image.open(f).convert('RGB')
        return f, True
    except OSError:
        return f, False


def find_truncated(path):
    path = Path(path)
    files = list(filter(filter_image_files, path.rglob('*')))
    bad_images = []
    with tqdm(total=len(files), desc=path.name, position=0, ncols=128) as t:
        with Pool() as pool:
            for f, b in pool.imap_unordered(get_score, files):
                t.set_postfix_str(f.name)
                t.update()

                if not b:
                    bad_images.append(f)

    return bad_images


def main(args):
    for path in args.paths:
        bad_images = find_truncated(path)
        for f in bad_images:
            print(f)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('paths', nargs='+', type=str)
    args = p.parse_args(sys.argv[1:])
    main(args)
