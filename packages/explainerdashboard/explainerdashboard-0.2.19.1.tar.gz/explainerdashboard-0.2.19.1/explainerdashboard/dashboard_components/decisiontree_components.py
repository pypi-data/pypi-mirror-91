__all__ = [
    'DecisionTreesComponent',
    'DecisionPathTableComponent',
    'DecisionPathGraphComponent',
]

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..explainers import RandomForestExplainer, XGBExplainer
from ..dashboard_methods import *
from .classifier_components import ClassifierRandomIndexComponent
from .connectors import IndexConnector, HighlightConnector


class DecisionTreesComponent(ExplainerComponent):
    def __init__(self, explainer, title="Decision Trees", name=None,
                    subtitle="Displaying individual decision trees",
                    hide_title=False,  hide_subtitle=False,
                    hide_index=False, hide_highlight=False,
                    hide_selector=False,
                    pos_label=None, index=None, highlight=None, 
                    higher_is_better=True, description=None, **kwargs):
        """Show prediction from individual decision trees inside RandomForest component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Decision Trees".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            subtitle (str): subtitle
            hide_title (bool, optional): hide title, Defaults to False.
            hide_subtitle (bool, optional): Hide subtitle. Defaults to False.
            hide_index (bool, optional): Hide index selector. Defaults to False.
            hide_highlight (bool, optional): Hide tree highlight selector. Defaults to False.
            hide_selector (bool, optional): hide pos label selectors. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            index ({str, int}, optional): Initial index to display. Defaults to None.
            highlight (int, optional): Initial tree to highlight. Defaults to None.
            higher_is_better (bool, optional): up is green, down is red. If False
                flip the colors. (for gbm models only)
            description (str, optional): Tooltip to display when hover over
                component title. When None default text is shown. 
        """
        super().__init__(explainer, title, name)

        self.index_name = 'decisiontrees-index-'+self.name
        self.highlight_name = 'decisiontrees-highlight-'+self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        
        if isinstance(self.explainer, RandomForestExplainer):
            if self.description is None: self.description = """
            Show the prediction of every individul tree in a random forest.
            This demonstrates how a random forest is simply an average of an
            ensemble of decision trees.
            """
            if self.subtitle == "Displaying individual decision trees":
                self.subtitle += " inside Random Forest"
        elif isinstance(self.explainer, XGBExplainer):
            if self.description is None: self.description = """
            Shows the marginal contributions of each decision tree in an 
            xgboost ensemble to the final prediction. This demonstrates that
            an xgboost model is simply a sum of individual decision trees.
            """
            if self.subtitle == "Displaying individual decision trees":
                self.subtitle += " inside xgboost model"
        else:
            if self.description is None: self.description = ""
        self.register_dependencies("preds", "pred_probas")

    def layout(self):
        return dbc.Card([
            make_hideable(
                dbc.CardHeader([
                    html.Div([
                        html.H3(self.title, id='decisiontrees-title-'+self.name),
                        make_hideable(html.H6(self.subtitle, className='card-subtitle'), hide=self.hide_subtitle),
                        dbc.Tooltip(self.description, target='decisiontrees-title-'+self.name),
                    ]), 
                ]), hide=self.hide_title),
            dbc.CardBody([
                dbc.Row([
                    make_hideable(
                        dbc.Col([
                            dbc.Label(f"{self.explainer.index_name}:", id='decisiontrees-index-label-'+self.name),
                                dbc.Tooltip(f"Select {self.explainer.index_name} to display decision trees for", 
                                            target='decisiontrees-index-label-'+self.name),
                            dcc.Dropdown(id='decisiontrees-index-'+self.name, 
                                options = [{'label': str(idx), 'value':idx} 
                                                for idx in self.explainer.idxs],
                                value=self.index)
                        ], md=4), hide=self.hide_index),
                    make_hideable(
                        dbc.Col([
                            dbc.Label("Highlight tree:", id='decisiontrees-tree-label-'+self.name),
                                dbc.Tooltip(f"Select a specific tree to highlight. You can also "
                                            "highlight by clicking on a specifc bar in the bar chart.", 
                                            target='decisiontrees-tree-label-'+self.name),
                            dbc.Select(id='decisiontrees-highlight-'+self.name, 
                                options = [{'label': str(tree), 'value': tree} 
                                                for tree in range(self.explainer.no_of_trees)],
                                value=self.highlight)
                        ], md=2), hide=self.hide_highlight), 
                    make_hideable(
                            dbc.Col([self.selector.layout()
                        ], width=2), hide=self.hide_selector)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="decisiontrees-graph-"+self.name,
                                    config=dict(modeBarButtons=[['toImage']], displaylogo=False)),  
                    ])
                ]),
            ])   
        ])

    def component_callbacks(self, app):
        @app.callback(
            Output("decisiontrees-graph-"+self.name, 'figure'),
            [Input('decisiontrees-index-'+self.name, 'value'),
             Input('decisiontrees-highlight-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_tree_graph(index, highlight, pos_label):
            if index is not None:
                highlight = None if highlight is None else int(highlight)
                return self.explainer.plot_trees(index, 
                        highlight_tree=highlight, pos_label=pos_label,
                        higher_is_better=self.higher_is_better)
            return {}

        @app.callback(
            Output('decisiontrees-highlight-'+self.name, 'value'),
            [Input("decisiontrees-graph-"+self.name, 'clickData')])
        def update_highlight(clickdata):
            highlight_tree = int(clickdata['points'][0]['text'].split('tree no ')[1].split(':')[0]) if clickdata is not None else None
            if highlight_tree is not None:
                return highlight_tree
            raise PreventUpdate

class DecisionPathTableComponent(ExplainerComponent):
    def __init__(self, explainer, title="Decision path table", name=None,
                    subtitle="Decision path through decision tree",
                    hide_title=False,  hide_subtitle=False,
                    hide_index=False, hide_highlight=False,
                    hide_selector=False,
                    pos_label=None, index=None, highlight=None, description=None,
                    **kwargs):
        """Display a table of the decision path through a particular decision tree

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Decision path table".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            subtitle (str): subtitle
            hide_title (bool, optional): hide title, Defaults to False.
            hide_subtitle (bool, optional): Hide subtitle. Defaults to False.
            hide_index (bool, optional): Hide index selector. 
                        Defaults to False.
            hide_highlight (bool, optional): Hide tree index selector. 
                        Defaults to False.
            hide_selector (bool, optional): hide pos label selectors. 
                        Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            index ({str, int}, optional): Initial index to display decision 
                        path for. Defaults to None.
            highlight (int, optional): Initial tree idx to display decision 
                        path for. Defaults to None.
            description (str, optional): Tooltip to display when hover over
                component title. When None default text is shown. 
        """
        super().__init__(explainer, title, name)

        self.index_name = 'decisionpath-table-index-'+self.name
        self.highlight_name = 'decisionpath-table-highlight-'+self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        
        if self.description is None: self.description = """
        Shows the path that an observation took down a specific decision tree.
        """
        self.register_dependencies("decision_trees")

    def layout(self):
        return dbc.Card([
            make_hideable(
                dbc.CardHeader([
                        html.Div([
                            html.H3(self.title, id='decisionpath-table-title-'+self.name),
                            make_hideable(html.H6(self.subtitle, className='card-subtitle'), hide=self.hide_subtitle),
                            dbc.Tooltip(self.description, target='decisionpath-table-title-'+self.name),
                        ]), 
                ]), hide=self.hide_title),
            dbc.CardBody([
                dbc.Row([
                    make_hideable(
                        dbc.Col([
                            dbc.Label(f"{self.explainer.index_name}:", id='decisionpath-table-index-label-'+self.name),
                            dbc.Tooltip(f"Select {self.explainer.index_name} to display decision tree for", 
                                            target='decisionpath-table-index-label-'+self.name),
                            dcc.Dropdown(id='decisionpath-table-index-'+self.name, 
                                options = [{'label': str(idx), 'value':idx} 
                                                for idx in self.explainer.idxs],
                                value=self.index)
                        ], md=4), hide=self.hide_index),
                        make_hideable(
                        dbc.Col([
                            dbc.Label("Show tree:", id='decisionpath-table-tree-label-'+self.name),
                            dbc.Tooltip(f"Select decision tree to display decision tree path for", 
                                            target='decisionpath-table-tree-label-'+self.name),
                            dbc.Select(id='decisionpath-table-highlight-'+self.name, 
                                options = [{'label': str(tree), 'value': tree} 
                                                for tree in range(self.explainer.no_of_trees)],
                                value=self.highlight)
                        ], md=2), hide=self.hide_highlight),
                        make_hideable(
                            dbc.Col([self.selector.layout()
                        ], md=2), hide=self.hide_selector)
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div(id="decisionpath-table-"+self.name),  
                    ]),
                ]),
            ]),
        ])

    def component_callbacks(self, app):
        @app.callback(
            Output("decisionpath-table-"+self.name, 'children'),
            [Input('decisionpath-table-index-'+self.name, 'value'),
             Input('decisionpath-table-highlight-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_decisiontree_table(index, highlight, pos_label):
            if index is not None and highlight is not None:
                decisionpath_df = self.explainer.decisiontree_summary_df(
                    int(highlight), index, pos_label=pos_label)
                return dbc.Table.from_dataframe(decisionpath_df)
            raise PreventUpdate


class DecisionPathGraphComponent(ExplainerComponent):
    def __init__(self, explainer, title="Decision path graph", name=None,
                    subtitle="Visualizing entire decision tree",
                    hide_title=False,  hide_subtitle=False, hide_index=False, 
                    hide_highlight=False, hide_button=False,
                    hide_selector=False,
                    pos_label=None, index=None, highlight=None, description=None,
                    **kwargs):
        """Display dtreeviz decision path

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Decision path graph".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            subtitle (str): subtitle
            hide_title (bool, optional): hide title
            hide_subtitle (bool, optional): Hide subtitle. Defaults to False.
            hide_index (bool, optional): hide index selector. Defaults to False.
            hide_highlight (bool, optional): hide tree idx selector. Defaults to False.
            hide_button (bool, optional): hide the button, Defaults to False.
            hide_selector (bool, optional): hide pos label selectors. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            index ({str, int}, optional): Initial index to display. Defaults to None.
            highlight ([type], optional): Initial tree idx to display. Defaults to None.
            description (str, optional): Tooltip to display when hover over
                component title. When None default text is shown. 
        """
        super().__init__(explainer, title, name)
        # if explainer.is_regression:
        #     raise ValueError("DecisionPathGraphComponent only available for classifiers for now!")

        self.index_name = 'decisionpath-index-'+self.name
        self.highlight_name = 'decisionpath-highlight-'+self.name
        if self.description is None: self.description = """
        Visualizes the path that an observation took down a specific decision tree,
        by showing the entire decision tree and the path that a specific observation
        took down this tree.
        """

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)

    def layout(self):
        return dbc.Card([
            make_hideable(
                dbc.CardHeader([          
                    html.Div([
                        html.H3(self.title, id='decisionpath-title-'+self.name),
                        make_hideable(html.H6(self.subtitle, className='card-subtitle'), hide=self.hide_subtitle),
                        dbc.Tooltip(self.description, target='decisionpath-title-'+self.name),
                    ]), 
                ]), hide=self.hide_title),
            dbc.CardBody([
                dbc.Row([
                    make_hideable(
                        dbc.Col([
                            dbc.Label(f"{self.explainer.index_name}:", id='decisionpath-index-label-'+self.name),
                                dbc.Tooltip(f"Select {self.explainer.index_name} to display decision tree for", 
                                            target='decisionpath-index-label-'+self.name),
                            dcc.Dropdown(id='decisionpath-index-'+self.name, 
                                options = [{'label': str(idx), 'value':idx} 
                                                for idx in self.explainer.idxs],
                                value=self.index)
                        ], md=4), hide=self.hide_index),
                        make_hideable(
                        dbc.Col([
                            dbc.Label("Show tree:", id='decisionpath-tree-label-'+self.name),
                            dbc.Tooltip(f"Select decision tree to display decision tree for", 
                                            target='decisionpath-tree-label-'+self.name),
                            dbc.Select(id='decisionpath-highlight-'+self.name, 
                                options = [{'label': str(tree), 'value': tree} 
                                                for tree in range(self.explainer.no_of_trees)],
                                value=self.highlight)
                        ], md=2), hide=self.hide_highlight), 
                        make_hideable(
                            dbc.Col([self.selector.layout()
                        ], width=2), hide=self.hide_selector),
                        make_hideable(
                        dbc.Col([
                            dbc.Button("Generate Tree Graph", color="primary", 
                                        id='decisionpath-button-'+self.name),
                            dbc.Tooltip("Generate visualisation of decision tree. "
                                        "Only works if graphviz is properly installed,"
                                        " and may take a while for large trees.",
                                    target='decisionpath-button-'+self.name)
                        ], md=2, align="end"), hide=self.hide_button),           
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Loading(id="loading-decisionpath-"+self.name, 
                            children=html.Img(id="decisionpath-svg-"+self.name)),  
                    ]),
                ]),
            ]),   
        ])

    def component_callbacks(self, app):
        @app.callback(
            Output("decisionpath-svg-"+self.name, 'src'),
            [Input('decisionpath-button-'+self.name, 'n_clicks')],
            [State('decisionpath-index-'+self.name, 'value'),
             State('decisionpath-highlight-'+self.name, 'value'),
             State('pos-label-'+self.name, 'value')]
        )
        def update_tree_graph(n_clicks, index, highlight, pos_label):
            if n_clicks is not None and index is not None and highlight is not None:
                return self.explainer.decision_path_encoded(int(highlight), index)
            raise PreventUpdate