#!/usr/bin/python3

import os
import logging
import argparse
import pandas as pd
from pyhard.context import Configuration
from pyhard.instancespace import build_metadata, run_matilda
from pyhard.visualization import app, Dashboard


def main():
    logger = logging.getLogger(__name__)
    _my_path = os.path.abspath(os.path.dirname(__file__))
    _my_path = os.path.join(_my_path, '..')

    with Configuration() as conf:
        for name, path in conf.get(['rootdir', 'matildadir', 'datafile']).items():
            if not os.path.isabs(path):
                abs_path = os.path.join(_my_path, path)
                if os.path.exists(abs_path):
                    conf.set(name, abs_path)
                else:
                    logger.error("Invalid '{0}': '{1}'".format(name, abs_path))
                    raise NotADirectoryError

        file_path = conf.get('datafile')
        if os.path.isfile(file_path):
            logger.info("Reading input dataset: {0}".format(file_path))
            df_dataset = pd.read_csv(file_path)
        else:
            logger.error("Invalid datafile '{0}'".format(file_path))
            raise FileNotFoundError

        kwargs = conf.get_full()

        if args.meta:
            logger.info("Building metadata.")
            df_metadata = build_metadata(data=df_dataset, verbose=args.verbose, **kwargs)

        if args.matilda:
            logger.info("Running matilda.")
            _ = run_matilda(rootdir=kwargs['rootdir'], matildadir=kwargs['matildadir'])

        logger.info("Instance Hardness analysis finished.")

        if args.app:
            rootdir_path = os.path.abspath(kwargs['rootdir'])
            if not args.meta:
                df_metadata = pd.read_csv(os.path.join(rootdir_path, 'metadata.csv'), index_col='instances')
            df_is = pd.read_csv(os.path.join(rootdir_path, 'coordinates.csv'), index_col='Row')
            df_is.index.name = df_metadata.index.name
            df_dataset.index = df_metadata.index
            app(df_dataset, df_metadata, df_is)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Instance Hardness analysis')
    parser.add_argument('--no-meta', dest='meta', action='store_false', help="does not generate a new metadata file; "
                                                                             "uses previously saved instead")
    parser.add_argument('--no-matilda', dest='matilda', action='store_false', help="does not execute matilda")
    parser.add_argument('-s', '--feat-select', dest='select', action='store_true',
                        default=False, help="whether to run feature selection")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="verbose mode")
    parser.add_argument('--app', dest='app', action='store_true', default=False, help="runs app to visualize data")
    parser.add_argument('--demo', dest='demo', action='store_true', default=False, help="runs demo for datasets in "
                                                                                        "'data/' directory")

    args = parser.parse_args()
    if args.demo:
        logging.getLogger().setLevel(logging.WARNING)
        print("Press ^C to exit demo")
        dash = Dashboard()
        pane = dash.display()
        pane.servable()
        pane.show()
    else:
        main()
