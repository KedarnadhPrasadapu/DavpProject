import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load your dataset
# Replace 'your_dataset.csv' with the actual path to your dataset
df = pd.read_csv('data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Electric Vehicle Adoption Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            multi=True,
            placeholder="Select Region"
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.RangeSlider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            marks={str(year): str(year) for year in sorted(df['year'].unique())},
            step=1,
            value=[df['year'].min(), df['year'].max()]
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='histogram'),
])

# Callbacks for interactivity
@app.callback(
    [
        Output('bar-chart', 'figure'),
        Output('line-chart', 'figure'),
        Output('scatter-plot', 'figure'),
        Output('pie-chart', 'figure'),
        Output('histogram', 'figure'),
    ],
    [
        Input('region-dropdown', 'value'),
        Input('year-slider', 'value')
    ]
)
def update_graphs(selected_regions, selected_years):
    # Filter data
    filtered_df = df[
        (df['year'] >= selected_years[0]) & 
        (df['year'] <= selected_years[1])
    ]
    
    if selected_regions:
        filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
    
    # Bar Chart
    bar_fig = px.bar(filtered_df, x='category', y='value', color='region', barmode='group',
                     title="Value by Category and Region")
    
    # Line Chart
    line_fig = px.line(filtered_df, x='year', y='value', color='powertrain',
                       title="Trends Over Years by Powertrain")
    
    # Scatter Plot
    scatter_fig = px.scatter(filtered_df, x='parameter', y='value', color='mode', size='value',
                             title="Parameter vs Value")
    
    # Pie Chart
    pie_fig = px.pie(filtered_df, names='region', values='value',
                     title="Distribution by Region")
    
    # Histogram
    hist_fig = px.histogram(filtered_df, x='value', color='category', nbins=20,
                            title="Value Distribution by Category")
    
    return bar_fig, line_fig, scatter_fig, pie_fig, hist_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
