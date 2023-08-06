import time
import warnings
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from . import metrics


_clf_dict = {
    'linear_svm': SVC,
    'rbf_svm': SVC,
    'random_forest': RandomForestClassifier,
    'gradient_boosting': GradientBoostingClassifier,
    'mlp': MLPClassifier,
    'bagging': BaggingClassifier,
    'naive_bayes': GaussianNB,
    'logistic_regression': LogisticRegression
}


class Classifier:
    def __init__(self, data: pd.DataFrame, cv=10, labels_col=None):
        self.logger = logging.getLogger(__name__)

        if labels_col is None:
            self.labels_col = data.columns[-1]
            self.y = data.iloc[:, -1].values
        else:
            self.labels_col = labels_col
            self.y = data[labels_col].values

        self.data = data.reset_index(drop=True)
        self.X = data.drop(columns=self.labels_col).values
        self.categories = np.unique(self.y).tolist()
        self.N = len(data)
        self.cv = cv

    def cprint(self, msg, flag):
        if flag:
            self.logger.info(msg)

    @staticmethod
    def _call_function(module, name, **kwargs):
        return getattr(module, name)(**kwargs)

    def score(self, metric: str, y_true: np.ndarray, y_pred: np.ndarray, classes_order: np.ndarray = None):
        if classes_order is None:
            n_classes = y_pred.shape[1]
            classes_order = np.array(range(0, n_classes))

        enc = OneHotEncoder(categories=[self.categories])
        y_true = enc.fit_transform(y_true.reshape(-1, 1)).toarray()
        y_true = y_true[:, classes_order.argsort()]
        return self._call_function(module=metrics, name=metric, y_true=y_true, y_pred=y_pred)

    # TODO: grid search optmization
    def run(self, clf, metric='logloss', n_folds=10, n_iter=10, verbose=False, **kwargs):
        if callable(clf):
            clf = clf(**kwargs)
        else:
            clf = _clf_dict[clf](**kwargs)

        kf = KFold(n_splits=n_folds, shuffle=True)

        score = np.zeros((self.N, n_iter))
        clf_name = clf.__class__.__name__
        self.cprint("Running classifier {0}...\nwith parameters {1}".format(clf_name, clf.get_params()),
                    verbose)
        start = time.time()
        for i in range(n_iter):
            for train_index, test_index in kf.split(self.X):
                pipe = Pipeline([('scaler', StandardScaler()), (clf_name, clf)])
                pipe = pipe.fit(self.X[train_index, :], y=self.y[train_index])
                y_pred = pipe.predict_proba(self.X[test_index, :])

                score[test_index, i] = self.score(metric=metric, y_true=self.y[test_index],
                                                  y_pred=y_pred, classes_order=clf.classes_)
        end = time.time()
        self.cprint("Elapsed time: {0}".format(end-start), verbose)

        return score.mean(axis=1)

    def run_all(self, metric='logloss', n_folds=10, n_iter=10, algo_list=None, parameters=None, verbose=False):
        if algo_list is None:
            algo_dict = _clf_dict.copy()
        elif isinstance(algo_list, list):
            keys = sorted(list(set(algo_list) & set(_clf_dict.keys())))
            algo_dict = {k: _clf_dict.get(k) for k in keys}
        else:
            raise TypeError("Expected list type for parameter 'algo_list', not '{0}'".format(type(algo_list)))

        if parameters is None:
            parameters = {}
            warnings.warn("No parameters provided. Using sklearn default values for {0}.".format(algo_dict.keys()))

        # with Configuration() as conf:
        #     params = conf.get('parameters')

        result = {}
        for key, algo in algo_dict.items():
            algo_params = parameters.get(key)
            if algo_params is None:
                algo_params = {}
            result[key] = self.run(algo, metric, n_folds, n_iter, verbose, **algo_params)

        df_result = pd.DataFrame(result)
        return df_result.add_prefix('algo_')
