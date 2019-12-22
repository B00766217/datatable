#interactive datatable-interactivity
# python app.py
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('df_rev_short_nounits.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
  html.H2(["SBKE Group Revenues"], style={'textAlign': "center", "padding-bottom": "30"}),
                                                                                                  
  html.H5(["'filter data...' to select Territory, Entity, Code etc. To sort, use arrows"], className="subtitle padded"),
  dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
            #{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        style_table={
        'maxHeight': '300px',
        #'maxWidth': '90pc',
        'overflowY': 'scroll'
        },
        fixed_rows={'headers': True, 'data': 0},
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        #row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        #page_size= 10,
        #style_cell={'textAlign': 'left'},
        #style_as_list_view=True,
        style_header={
        'backgroundColor': 'rgb(91, 194, 54)',
        'color':'rgb(255, 255, 255)',
        'fontWeight': 'bold'
        },
        style_cell_conditional=[
        {'if': {'column_id': 'Territory'},
         'width': '12%'},
        {'if': {'column_id': 'Entity'},
         'width': '10%'},
        {'if': {'column_id': 'Code'},
         'width': '10%'},
        {'if': {'column_id': 'Description'},
         'width': '12%'},
        {'if': {'column_id': 'Operation'},
         'width': '13%'},
        {'if': {'column_id': '2017A'},
         'width': '10%'},
        {'if': {'column_id': '2018A'},
         'width': '10%'},
        {'if': {'column_id': '2019F'},
         'width': '10%'},
        {'if': {'column_id': '2020B'},
         'width': '10%'},
    ]
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["Territory"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 15, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["2017A", "2018A", "2019F","2020B"] if column in dff
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
