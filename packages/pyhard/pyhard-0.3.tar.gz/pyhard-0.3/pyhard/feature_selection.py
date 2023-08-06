import pandas as pd
import numpy as np
import rankaggregation as ra
from scipy.special import softmax
from sklearn.feature_selection import VarianceThreshold
from .thirdparty import skfeature
from .utils import call_module_func


def _select(F, J, how='cumsum', **kwargs):
    sorted_idx = np.argsort(J)[::-1]
    F_sorted = F[sorted_idx]

    if how == 'cumsum':
        if 'eta' in kwargs:
            eta = kwargs['eta']
        else:
            eta = 0.8
        s_value = softmax(J[sorted_idx])
        p = 0
        selected = []
        for i in range(len(s_value)):
            p += s_value[i]
            selected.append(F_sorted[i])
            if p >= eta:
                break
        return selected

    elif how == 'top':
        if 'N' in kwargs:
            N = kwargs['N']
        else:
            N = len(F) // 2
        return F_sorted[:N]


def _prefilter(X, var_threshold=1e-3):
    sel = VarianceThreshold(threshold=var_threshold)
    sel.fit(X)
    return sel.get_support()


def fs_pipeline(df_metadata: pd.DataFrame, method='icap', var_filter=True, var_threshold=1e-3,  **kwargs):
    df_features = df_metadata.filter(regex='^feature_')
    df_algo = df_metadata.filter(regex='^algo_')

    if var_filter:
        mask = _prefilter(df_features.values, var_threshold)
        df_features = df_features.iloc[:, mask]

    agg = ra.RankAggregator()
    rank = []
    f_list = df_features.columns.to_list()
    N = len(f_list)

    if 'n_selected_features' not in kwargs:
        kwargs['n_selected_features'] = N

    for algo in df_algo:
        args = [df_features.values, df_algo[[algo]].values]
        F, J, _ = call_module_func(skfeature, method, *args, **kwargs)
        assert (np.diff(J) <= 0).all()
        rank.append(_select(F, J, **kwargs))

    rank = [[f_list[i] for i in l] for l in rank]
    return agg.instant_runoff(rank)
