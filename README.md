# make-datasetfolder
A utility to create a PyTorch DatasetFolder from any .csv or .tsv file with file path and class data.

## Installation
From PyPI: `pip install make-datasetfolder`
From GitHub:
```
git clone https://github.com/eczy/make-datasetfolder
pip install -e make-datasetfolder
```

## Use Case
In PyTorch, the `DataFolder` and `ImageFolder` classes provide a convenient interface for computer vision datasets structured as such:

```
root/class_x/xxx.ext
root/class_x/xxy.ext
root/class_x/xxz.ext

root/class_y/123.ext
root/class_y/nsdf3.ext
root/class_y/asd932_.ext
```

This utility transforms any dataset with a table containing file paths and class labels into this format.

## Example
Suppse you have `dataset.csv` of the form:
```
sample,class,some_feature,another_feature
img-0001.jpg,0,foo,bar
some/relative/directory/img-0002.jpg,1,foo,bar
...
```

Running `make-dataset-folder -p sample -l class dataset.csv output` will create a folder `output` with the following structure:

```
output/0/img-0001.jpg
output/1/img-0002.jpg
...
```

Using the `-m` flag will move images rather than copy them. This could be useful for large datasets that shouldn't be duplicated on disk.

## Usage
```
usage: make-datasetfolder [-h] [-p PATH_COLUMN] [-l LABEL_COLUMN] [-m] [-f]
                          [-t THREADS]
                          input output

positional arguments:
  input                 Path to input .csv or .tsv
  output                Path to output directory.

optional arguments:
  -h, --help            show this help message and exit
  -p PATH_COLUMN, --path-column PATH_COLUMN
                        Column name or index with file paths (default: 0).
  -l LABEL_COLUMN, --label-column LABEL_COLUMN
                        Column name or index with labels (default: 1).
  -m, --move            Move files instead of copying.
  -f, --force           Overwrite output directory if it already exists.
  -t THREADS, --threads THREADS
                        Number of threads to use (default: number of CPU
                        cores)
```
