import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from scipy.stats import linregress

# Generate random data based on correlation
def generate_data(correlation, n_points=100):
    np.random.seed(42)
    x = np.random.randn(n_points)
    y = correlation * x + (1 - correlation) * np.random.randn(n_points)
    return x, y

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Effect of correlation on simple linear regression"),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='correlation-slider',
                min=-1,
                max=1,
                step=0.01,
                value=0.5,
                marks={i/10: str(i/10) for i in range(-10, 11)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Hr(),
            html.P(id='correlation-value')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='regression-plot')
        ])
    ])
], fluid=True)

@app.callback(
    [Output('regression-plot', 'figure'),
     Output('correlation-value', 'children')],
    [Input('correlation-slider', 'value')]
)
def update_plot(correlation):
    x, y = generate_data(correlation)
    slope, intercept, _, _, _ = linregress(x, y)
    line = slope * x + intercept

    trace_data = [go.Scatter(x=x, y=y, mode='markers', name='Data Points'),
                  go.Scatter(x=x, y=line, mode='lines', name='Regression Line')]
    layout = go.Layout(
        title=f'Simple Linear Regression with correlation {correlation:.2f}',
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        showlegend=True
    )

    return {"data": trace_data, "layout": layout}, f"Correlation: {correlation:.2f}"

if __name__ == '__main__':
    app.run_server(port= 8051)
