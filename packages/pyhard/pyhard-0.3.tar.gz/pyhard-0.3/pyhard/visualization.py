import os
import pandas as pd
import numpy as np
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import interact_manual, interact
import holoviews as hv
from holoviews import opts, dim
from holoviews.plotting.links import DataLink
from bokeh.models import HoverTool
import panel as pn
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import NeighborhoodComponentsAnalysis

_my_path = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(_my_path, '../data')


def scatter_widget(df: pd.DataFrame, width=950, height=650):
    cols = df.columns.to_list()
    cols.append(None)
    w_color = widgets.Dropdown(options=cols, description='Color: ', value=None)
    w_symbol = widgets.Dropdown(options=cols, description='Symbol: ', value=None)
    w_size = widgets.Dropdown(options=cols, description='Size: ', value=None)
    w_hover = widgets.SelectMultiple(options=cols, description='Hover info: ', value=[])

    # w_type = widgets.RadioButtons(options=['2D', '3D'], value='2D', description='Scatter plot: ', disabled=False)

    # def update_signals(*args):
    #     w_signal.options = list(get_metadata_table().query("site == '{0}'".format(w_site.value))['signal'].unique())
    #
    # w_site.observe(update_signals, 'value')

    def plotter(color, symbol, size, hover):
        # if type == '3D':
        #     scatter = px.scatter
        # else:
        #     scatter = px
        df_plot = df.copy()
        if color is not None and df_plot[color].dtype == 'int64':
            df_plot[color] = df_plot[color].astype(str)
        if symbol is not None:
            fig = px.scatter(df_plot, x=cols[0], y=cols[1], color=color, symbol=symbol, size=size, hover_data=hover,
                             symbol_sequence=['circle-open', 'x-thin-open', 'asterisk-thin', 'triangle-up-open'],
                             width=width, height=height, color_continuous_scale='Bluered')
        else:
            fig = px.scatter(df_plot, x=cols[0], y=cols[1], color=color, size=size, hover_data=hover,
                             width=width, height=height, color_continuous_scale='Bluered')
        fig.update_layout(coloraxis_colorbar=dict(yanchor="top", y=1, x=0,
                                                  ticks="outside"))
        fig.show()

    interact(plotter, color=w_color, symbol=w_symbol, size=w_size, hover=w_hover)


def app(df_dataset: pd.DataFrame, df_metadata: pd.DataFrame, df_is: pd.DataFrame):
    hv.extension('bokeh')

    data = df_is.join(df_dataset)
    data = data.join(df_metadata)
    mlist = ['triangle', 'circle', 'square']
    is_kdims = df_is.columns.to_list()[0:2]
    data_dims = df_dataset.columns.to_list()
    data_kdims = data_dims[0:2]
    class_label = data_dims[2]
    meta_dims = df_metadata.columns.to_list()

    # data['class'] = data['class'].apply(lambda x: mlist[x])

    def plotter(c, lim, autorange_on, hover_list, **kwargs):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = 'RdYlBu_r'
        scatter1 = hv.Scatter(data, kdims=data_kdims, vdims=[class_label, c] + meta_dims,
                              label='Original Data').opts(width=480, height=420, color=c,
                                                          cmap=cmap, show_grid=True,
                                                          marker=dim(class_label).categorize(mlist))

        scatter2 = hv.Scatter(data, kdims=is_kdims, vdims=[class_label, c] + meta_dims,
                              label='Instance Space').opts(width=480, height=420, color=c,
                                                           cmap=cmap, show_grid=True,
                                                           marker=dim(class_label).categorize(mlist))

        hover_list = [c] + hover_list
        tooltips = [(s, '@' + s) for s in hover_list]
        hover = HoverTool(tooltips=tooltips)

        dlink = DataLink(scatter1, scatter2)

        return (scatter1 + scatter2).cols(2).opts(opts.Scatter(tools=['box_select', 'lasso_select', hover],
                                                               size=4, framewise=True, colorbar=True, clim=lim),
                                                  opts.Layout(shared_axes=True, shared_datasource=True, framewise=True))

    w_color = pn.widgets.Select(options=[class_label] + meta_dims, value=class_label)
    w_color_range = pn.widgets.IntRangeSlider(start=-10, end=30, value=(0, 30), step=1)
    w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
    w_selector_hover = pn.widgets.CrossSelector(value=data_dims + is_kdims,
                                                options=data.columns.to_list())

    @pn.depends(color=w_color.param.value, lim=w_color_range.param.value,
                autorange_on=w_checkbox.param.value, hover_list=w_selector_hover.param.value)
    def load_color(color, lim, autorange_on, hover_list):
        return plotter(color, lim, autorange_on, hover_list)

    dmap = hv.DynamicMap(load_color)
    out = pn.Column(pn.Row(pn.WidgetBox('### Color', w_color, '#### Color Bar', w_checkbox, w_color_range),
                           pn.WidgetBox('### Hover data', w_selector_hover)),
                    pn.layout.VSpacer(), dmap, sizing_mode='scale_both')

    out.show()


class Dashboard:
    list_dir = [name for name in os.listdir(datadir) if os.path.isdir(os.path.join(datadir, name))]
    list_dir.sort()

    w_dir = pn.widgets.Select(options=list_dir, value='overlap')
    w_color = pn.widgets.Select(options=[], value='')
    w_color_range = pn.widgets.IntRangeSlider(start=-10, end=50, value=(0, 30), step=1)
    w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
    w_selector_hover = pn.widgets.MultiChoice(value=[], options=[])
    w_dim = pn.widgets.RadioButtonGroup(options=['LDA', 'NCA', 'PCA'], value='LDA', button_type='default')

    def __init__(self):
        hv.extension('bokeh')

        self.mlist = ['circle', 'triangle', 'square', 'diamond', '+', 'x']
        self.df_data = self.df_metadata = self.df_feat_proc = self.df_is = None
        self.is_kdims = self.data_dims = self.data_kdims = self.class_label = self.meta_dims = []
        self.folder = None

        self.load_data(self.w_dir.value)
        self.update_components()

    def load_data(self, path, dim_method='LDA'):
        if path != self.folder:
            self.folder = path
            path = os.path.join(datadir, path)
            dataset = pd.read_csv(os.path.join(path, 'data.csv'))
            # dataset.iloc[:, -1] = dataset.iloc[:, -1].astype(str)

            if len(dataset.columns) > 3:
                X = dataset.iloc[:, :-1]
                y = dataset.iloc[:, -1]
                X_embedded = reduce_dim(X, y, method=dim_method)
                df = pd.DataFrame(X_embedded, columns=['V1', 'V2'], index=X.index)
                dataset = pd.concat([df, y], axis=1)

            self.df_metadata = pd.read_csv(os.path.join(path, 'metadata.csv'), index_col='instances')
            # self.df_feat_proc = pd.read_csv(os.path.join(path, 'feature_process.csv'), index_col='Row')
            # self.df_feat_proc.index.name = 'instances'
            self.df_is = pd.read_csv(os.path.join(path, 'coordinates.csv'), index_col='Row')
            self.df_is.index.name = 'instances'

            dataset.index = self.df_metadata.index
            self.df_data = self.df_is.join(dataset)
            self.df_data = self.df_data.join(self.df_metadata)

            # TODO: organizar kdims e vdims
            self.is_kdims = self.df_is.columns.to_list()[0:2]
            self.data_dims = dataset.columns.to_list()
            self.data_kdims = self.data_dims[0:2]
            self.class_label = self.data_dims[2]
            self.meta_dims = self.df_metadata.columns.to_list()

    def plotter(self, c, lim, autorange_on, hover_list, **kwargs):
        if not autorange_on:
            lim = (np.nan, np.nan)
        # cmap = 'RdYlBu_r'
        if c == self.class_label:
            cmap = 'Set1'
        else:
            cmap = 'jet'

        hover_list = [c] + hover_list if c not in hover_list else hover_list
        tooltips = [('index', '$index')] + [(s, '@' + s) for s in hover_list]
        hover = HoverTool(tooltips=tooltips)

        scatter1_vdims = [self.data_kdims[1], self.class_label] + self.meta_dims + self.is_kdims
        scatter1 = hv.Scatter(self.df_data, kdims=self.data_kdims[0], vdims=scatter1_vdims,
                              label='Original Data').opts(width=500, height=440, color=c,
                                                          cmap=cmap, show_grid=True,
                                                          marker=dim(self.class_label).categorize(self.mlist),
                                                          framewise=True)

        scatter2_vdims = [self.is_kdims[1], self.class_label] + self.meta_dims + self.data_kdims
        scatter2 = hv.Scatter(self.df_data, kdims=self.is_kdims[0], vdims=scatter2_vdims,
                              label='Instance Space').opts(width=500, height=440, color=c,
                                                           cmap=cmap, show_grid=True,
                                                           marker=dim(self.class_label).categorize(self.mlist),
                                                           framewise=True)

        # dlink = DataLink(scatter1, scatter2)

        return (scatter1 + scatter2).opts(opts.Scatter(tools=['box_select', 'lasso_select', 'tap', hover],
                                                       size=4, colorbar=True, clim=lim),
                                          opts.Layout(shared_axes=True, shared_datasource=True)).cols(2)

    def update_components(self):
        self.w_color.options = self.meta_dims + [self.class_label]
        self.w_selector_hover.options = self.df_data.columns.to_list()
        self.w_selector_hover.value = self.data_dims + self.is_kdims

    def display(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value, hover_list=self.w_selector_hover.param.value,
                    folder=self.w_dir.param.value, method=self.w_dim.param.value)
        def update_plot(color, lim, autorange_on, hover_list, folder, method, **kwargs):
            self.load_data(folder, method)
            self.update_components()
            return self.plotter(color, lim, autorange_on, hover_list)

        dmap = hv.DynamicMap(update_plot)

        row = pn.Row(pn.Column(pn.WidgetBox('## Dataset', self.w_dir,
                                            '### Dimensionality Reduction', self.w_dim,
                                            height=200, width=250, sizing_mode='scale_both'),
                               pn.WidgetBox('## Color', self.w_color,
                                            '### Color Bar', self.w_checkbox, self.w_color_range,
                                            height=250, width=250, sizing_mode='scale_both'),
                               sizing_mode='scale_both'), dmap, sizing_mode='scale_both')  # pn.layout.HSpacer()
        pane = pn.Column(row, '## Hover Info', self.w_selector_hover)
        # pn.WidgetBox(pn.pane.VSpacer(), self.w_selector_hover, sizing_mode='stretch_height')

        # pane.servable()
        # pane.show()
        return pane
        # server = pane._get_server(show=True, port=52423, debug=True, start=True, websocket_origin='localhost:52423')


def reduce_dim(X, y, n_dim=2, method='LDA'):
    method = str.upper(method)
    if method == 'LDA':
        model = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis(n_components=n_dim))
    elif method == 'NCA':
        model = make_pipeline(StandardScaler(), NeighborhoodComponentsAnalysis(n_components=n_dim))
    else:
        model = make_pipeline(StandardScaler(), PCA(n_components=n_dim))

    model.fit(X, y)
    X_embedded = model.transform(X)

    return X_embedded


if __name__ == "__main__":
    dash = Dashboard()
    dash.display()

dash = Dashboard()
p = dash.display()
p.show()
