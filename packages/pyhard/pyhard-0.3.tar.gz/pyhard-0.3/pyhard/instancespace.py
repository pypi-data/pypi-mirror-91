import os
import warnings
import pandas as pd
from .measures import Measures
from .performance import Classifier
from .utils import get_param_names


metadata_file = 'metadata.csv'
options_file = 'options.json'


# TODO: verbose mode
def build_metadata(data, rootdir='', labels_col=None, save=True, **kwargs):
    measures = Measures(data, labels_col=labels_col)
    classifiers = Classifier(data, labels_col=labels_col)

    m_params = {k: kwargs.get(k) for k in get_param_names(measures.calculate_all)}
    df_measures = measures.calculate_all(**m_params)

    c_params = {k: kwargs.get(k) for k in get_param_names(classifiers.run_all)}
    df_algo = classifiers.run_all(**c_params)

    df_metadata = pd.concat([df_measures, df_algo], axis=1)
    n_inst = len(df_metadata)
    df_metadata.insert(0, 'instances', range(1, n_inst+1))
    df_metadata.set_index('instances', inplace=True)

    if save:
        if os.path.isdir(rootdir):
            df_metadata.to_csv(os.path.join(rootdir, metadata_file))
        else:
            warnings.warn("Invalid directory '{0}'. File will not be saved.".format(rootdir))
    return df_metadata


def run_matilda(rootdir, matildadir, metadata=None):
    """
    This is a wrapper function for matilda Matlab routine called via Python.
    :param rootdir: directory that contains the files 'metadata.csv' and 'options.json'. This is also the location of
    all the software outputs.
    :param matildadir: it points to the directory with matilda Matlab source code.
    :param metadata: dataframe (default None). It is saved as 'metadata.csv' in rootdir.
    """
    if not os.path.isdir(rootdir):
        raise NotADirectoryError("Invalid rootdir '{0}'".format(rootdir))
    elif not os.path.isdir(matildadir):
        raise NotADirectoryError("Invalid matildadir '{0}'".format(matildadir))

    file = os.path.join(rootdir, metadata_file)
    if metadata is not None:
        if isinstance(metadata, pd.DataFrame):
            metadata.to_csv(file)
        else:
            raise TypeError("Expected metadata as pandas DataFrame. Received '{0}' instead".format(type(metadata)))
    else:
        if not os.path.isfile(file):
            raise FileNotFoundError("File {0} not found in rootdir '{1}'".format(metadata_file, rootdir))

    options = os.path.join(rootdir, options_file)
    if not os.path.isfile(options):
        warnings.warn("File {0} not found in '{1}'. "
                      "Building default options file with example script...".format(options_file, rootdir))

    import matlab.engine
    eng = matlab.engine.start_matlab()
    eng.cd(matildadir, nargout=0)
    eng.trainIS(rootdir, nargout=0)
