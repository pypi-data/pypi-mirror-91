import gower
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from scipy.sparse.csgraph import minimum_spanning_tree

measures_dict = {
    'kDN': 'k_disagreeing_neighbors',
    'DS': 'disjunct_size',
    'DCP': 'disjunct_class_percentage',
    'TD_P': 'tree_depth_pruned',
    'TD_U': 'tree_depth_unpruned',
    'CL': 'class_likeliood',
    'CLD': 'class_likeliood_diff',
    'MV': 'minority_value',
    'CB': 'class_balance',
    'N1': 'borderline_points',
    'N2': 'intra_extra_ratio'
}


class Measures:
    """
    Hardness measures class. It provides separate methods to compute each measure
    :param data: a dataframe where each line is an instace and columns are features. One column should contain the
    labels. The name of the column with labels can be set with parameter 'labels_col'
    :type: pandas DataFrame
    :param labels_col: name of the column that contains the labels of the instances (default 'y')
    :param ccp_alpha: pruning parameter for pruned tree measures. If none is passed, then it attempts to tune
    automatically
    """

    def __init__(self, data: pd.DataFrame, ccp_alpha=None, labels_col='y'):
        self.labels_col = labels_col
        self.data = data.reset_index(drop=True)
        self.X = data.drop(columns=labels_col)
        self.y = data[labels_col]
        self.N = len(data)

        # Decision Tree Classifier
        dtc = tree.DecisionTreeClassifier(min_samples_split=2, criterion='gini')
        self.dtc = dtc.fit(self.X, self.y)

        # Decision Tree Classifier Pruned
        if ccp_alpha is None:
            parameters = {'ccp_alpha': np.linspace(0.001, 0.1, num=100)}
            dtc = tree.DecisionTreeClassifier(criterion='gini')
            clf = GridSearchCV(dtc, parameters)
            clf = clf.fit(self.X, self.y)
            ccp_alpha = clf.best_params_['ccp_alpha']

        self.dtc_pruned = tree.DecisionTreeClassifier(criterion='gini', ccp_alpha=ccp_alpha)
        self.dtc_pruned = self.dtc_pruned.fit(self.X, self.y)

    def _call_method(self, name, **kwargs):
        return getattr(self, name)(**kwargs)

    # TODO: add verbose
    def calculate_all(self, measures_list=None):
        if measures_list is None:
            measures_list = measures_dict.keys()

        results = {}
        for k in measures_list:
            results[k] = self._call_method(measures_dict[k])

        df_measures = pd.DataFrame(results)
        return df_measures.add_prefix('feature_')

    def k_disagreeing_neighbors(self, k=5):
        data = self.data.copy()
        nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm='auto').fit(self.X)
        distances, indices = nbrs.kneighbors(self.X)
        kDN = []
        for i in range(0, len(data)):
            v = data.loc[indices[i]][self.labels_col].values
            kDN.append(np.sum(v[1:] != v[0]) / k)
        return np.array(kDN)

    def disjunct_size(self):
        data = self.data.copy()

        data['leaf_id'] = self.dtc.apply(self.X)
        df_count = data.groupby('leaf_id').count().iloc[:, 0].to_frame('count').subtract(1)
        data = data.join(df_count, on='leaf_id')
        DS = data['count'].divide(data['count'].max())

        return DS.values

    def disjunct_class_percentage(self):
        data = self.data.copy()

        data['leaf_id'] = self.dtc_pruned.apply(self.X)
        dcp = []
        for index, row in data.iterrows():
            df_leaf = data[data['leaf_id'] == row['leaf_id']]
            dcp.append(len(df_leaf[df_leaf[self.labels_col] == row[self.labels_col]]) / len(df_leaf))

        return np.array(dcp)

    def tree_depth_unpruned(self):
        return self.X.apply(lambda x: self.dtc.decision_path([x]).sum() - 1, axis=1, raw=True).values

    def tree_depth_pruned(self):
        return self.X.apply(lambda x: self.dtc_pruned.decision_path([x]).sum() - 1, axis=1, raw=True).values

    def class_likeliood(self):
        n = len(self.y.unique())
        priors = np.ones((n,)) / n

        nb = GaussianNB(priors=priors)
        nb.fit(self.X, self.y)

        prob = nb.predict_proba(self.X)
        labels = self.y.values

        CL = [prob[i, np.argwhere(nb.classes_ == labels[i])[0][0]] for i in range(0, len(labels))]

        return np.array(CL)

    # TODO: implement for discrete variables too
    def class_likeliood_diff(self):
        n = len(self.y.unique())
        priors = np.ones((n,)) / n

        nb = GaussianNB(priors=priors)
        nb.fit(self.X, self.y)

        prob = nb.predict_proba(self.X)
        labels = self.y.values

        CLD = [prob[i, np.argwhere(nb.classes_ == labels[i])[0][0]] -
               np.max(np.delete(prob[i, :], np.argwhere(nb.classes_ == labels[i])[0][0]))
               for i in range(0, len(labels))]

        return np.array(CLD)

    def minority_value(self):
        mv_class = self.data.groupby(self.labels_col).count().iloc[:, 0]
        mv_class = mv_class.divide(mv_class.max())

        labels = self.y
        return labels.apply(lambda c: 1 - mv_class[c]).values

    def class_balance(self):
        cb_class = self.data.groupby(self.labels_col).count().iloc[:, 0]
        cb_class = cb_class.divide(self.N) - 1 / len(self.y.unique())

        labels = self.y
        return labels.apply(lambda c: cb_class[c]).values

    def borderline_points(self):
        X = self.X.values.copy()
        y = self.y.values.copy()

        dist_matrix = gower.gower_matrix(X)
        Tcsr = minimum_spanning_tree(dist_matrix)
        mst = Tcsr.toarray()
        mst = np.where(mst > 0, mst, np.inf)

        N1 = np.zeros(y.shape)
        for i in range(len(y)):
            idx = np.argwhere(np.minimum(mst[i, :], mst[:, i]) < np.inf)
            assert len(idx) > 0
            N1[i] = np.sum(y[idx[:, 0]] != y[i])
        return N1

    def intra_extra_ratio(self, metric='gower'):
        X = self.X.copy()
        y = self.y.copy()

        if metric == 'gower':
            dist_matrix = gower.gower_matrix(X.values)
            indices = np.argsort(dist_matrix, axis=1)
            distances = np.sort(dist_matrix, axis=1)
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=metric).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        N2 = np.zeros(y.values.shape)
        for i, value in y.items():
            nn = y.loc[indices[i, :]]
            intra = nn.eq(value)
            extra = nn.ne(value)
            assert np.all(np.diff(distances[i, intra]) >= 0)
            assert np.all(np.diff(distances[i, extra]) >= 0)
            N2[i] = distances[i, intra][1] / distances[i, extra][0]
        return N2
