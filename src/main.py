import argparse
import os
import sys
import shutil
import csv
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat


class FileExtensionException(Exception):
    pass


def handle_sample(handler, root, sample):
    src, label = sample
    dst = os.path.join(root, label)
    os.makedirs(dst, exist_ok=True)
    handler(src, dst)


def make_datasetfolder(input, output, path_column, label_column, force=False, move=False, threads=None):
    # Create output directory
    try:
        os.mkdir(output)
    except FileExistsError:
        if force:
            print(f'Removing {output}')
            shutil.rmtree(output)
            os.mkdir(output)
        else:
            raise

    try:
        _, ext = os.path.splitext(input)
        if ext == '.csv':
            delimiter = ','
        elif ext == '.tsv':
            delimited = '\t'
        else:
            raise FileExtensionException('Input file type must be .csv or .tsv')

        with open(input) as fin:
            # Sniff the first two lines to infer column names
            firstrow = next(fin)
            secondrow = next(fin)
            has_header = csv.Sniffer().has_header(firstrow + secondrow)

            fin.seek(0)
            reader = csv.reader(fin)
            if has_header:
                headers = list(next(reader))
            if not has_header or path_column not in headers or label_column not in headers:
                path_column = int(path_column)
                label_column = int(label_column)
            else:
                path_column = headers.index(path_column)
                label_column = headers.index(label_column)

            # Create generator of path, label pairs
            samples = ((row[path_column], row[label_column]) for row in reader)

            handler = shutil.move if move else shutil.copy

            # Distribute file operations over available threads
            with ProcessPoolExecutor(max_workers=threads) as executor:
                executor.map(handle_sample, repeat(handler), repeat(output), samples)

    except FileNotFoundError:
        sys.exit(f'{input} does not exist.')
    except ValueError:
        sys.exit('Encountered invalid column name or index.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Path to input .csv or .tsv')
    parser.add_argument('output', type=str, help='Path to output directory.')
    parser.add_argument('-p', '--path-column', type=str, default='0', help='Column name or index with file paths (default: 0).')
    parser.add_argument('-l', '--label-column', type=str, default='1', help='Column name or index with labels (default: 1).')
    parser.add_argument('-m', '--move', action='store_true', help='Move files instead of copying.')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite output directory if it already exists.')
    parser.add_argument('-t', '--threads', help='Number of threads to use (default: number of CPU cores)')
    args = parser.parse_args()

    make_datasetfolder(**vars(args))


if __name__ == '__main__':
    main()