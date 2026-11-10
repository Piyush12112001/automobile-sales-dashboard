import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)

MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# TASK 2.1: Create the app with a title
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
]
year_list = list(range(1980, 2024))

# TASK 2.2 + 2.3: Layout with dropdowns and output division
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px',
                   'textAlignLast': 'center'}
        ),
    ]),

    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select year',
        style={'width': '80%', 'padding': '3px', 'fontSize': '20px',
               'textAlignLast': 'center'}
    )),

    html.Div(id='output-container', className='chart-grid',
             style={'display': 'flex', 'flexDirection': 'column'}),
])


# TASK 2.4: Callbacks
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value'))
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'


@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')])
def update_output_container(selected_statistics, input_year):

    # TASK 2.5: Recession Report Statistics
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(
            yearly_rec, x='Year', y='Automobile_Sales',
            title='Average Automobile Sales fluctuation over Recession Period'))

        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            avg_sales, x='Vehicle_Type', y='Automobile_Sales',
            title='Average Number of Vehicles Sold by Vehicle Type'))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
            title='Total Expenditure Share by Vehicle Type during Recessions'))

        unemp = (recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
                 .mean().reset_index())
        R_chart4 = dcc.Graph(figure=px.bar(
            unemp, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
            labels={'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'},
            title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(R_chart1), html.Div(R_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(R_chart3), html.Div(R_chart4)],
                     style={'display': 'flex'}),
        ]

    # TASK 2.6: Yearly Report Statistics
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]

        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas, x='Year', y='Automobile_Sales',
            title='Yearly Automobile Sales (1980-2023)'))

        mas = (yearly_data.groupby('Month')['Automobile_Sales']
               .sum().reindex(MONTH_ORDER).reset_index())
        Y_chart2 = dcc.Graph(figure=px.line(
            mas, x='Month', y='Automobile_Sales',
            title='Total Monthly Automobile Sales in {}'.format(input_year)))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
            title='Total Advertisement Expenditure by Vehicle Type in {}'.format(input_year)))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(Y_chart1), html.Div(Y_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(Y_chart3), html.Div(Y_chart4)],
                     style={'display': 'flex'}),
        ]

    return None


if __name__ == '__main__':
    run = getattr(app, 'run', None) or app.run_server
    run(debug=True)