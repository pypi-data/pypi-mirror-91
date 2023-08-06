#!/usr/bin/python3

import os
import pandas as pd
from pyhard.context import Configuration
from pyhard.instancespace import build_metadata, run_matilda


def main():
    with Configuration() as conf:
        file_path = conf.get('datafile')
        print("Reading input dataset: {0}".format(file_path))
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)

        kwargs = conf.get(['rootdir', 'labels_col', 'measures_list', 'n_folds',
                           'n_iter', 'algo_list', 'parameters', 'verbose', 'matildadir'])

        print("Building metadata.")
        build_metadata(data=df, **kwargs)

        print("Running matilda.")
        run_matilda(rootdir=kwargs['rootdir'], matildadir=kwargs['matildadir'])


if __name__ == "__main__":
    main()
