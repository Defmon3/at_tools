#!/usr/bin/env python
import sys

import pandas as pd

if __name__ == "__main__":
    # Running in stand-alone mode
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Please specify an input CSV or TSV file as an argument.")
        exit(1)


def cleanColumns(name):
    # print("{}\t{}".format(name, ''.join(filter(str.isalnum, name))))
    return ''.join(filter(str.isalnum, name))


filesplit = filename.split(".")
if filesplit[-1] == 'tsv':
    sep = "\t"
else:
    sep = ","

filesplit[-1] = "jsonl"
fileout = ".".join(filesplit)

df = pd.read_csv(filename, sep=sep, header=0, error_bad_lines=False)

# Clean field names
df = df.rename(columns=cleanColumns)
df.info(verbose=True)

df.to_json(fileout, orient='records', lines=True, double_precision=0, date_format='iso')
