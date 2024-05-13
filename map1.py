from dash import Dash, dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MAP_ID = 'heatmap'
DATA_RADIO = 'data-selector'
LANG_RADIO = "language-selector"
FIG = 'figure'
VAL = 'value'
TITLE           = 'Language Diversity in the United States'

df = pd.read_csv("percent_languages.csv", sep=",")

def abbrev(df, col) -> pd.DataFrame:
    state2abbrev = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY',
        'Puerto Rico': 'PR',
        'Virigin Islands': 'VI'
    }

    df[col] = df[col].str.strip().replace(state2abbrev)
    return df

df = abbrev(df, 'State')

def generate_heatmap(selected_data, selected_language):
    # Select columns based on the selected data
    if selected_data == 'age':
        columns_to_display = ['5 to 17', '18 to 64', '65+']
    elif selected_data == 'poverty':
        columns_to_display = ['Below poverty level', 'At or above poverty level']
    elif selected_data == 'education':
        columns_to_display = ['Less than high school graduate', 'High school graduate',
                              'Some college or associate\'s degree', 'Bachelor\'s degree or higher']

    # Filter dataframe based on selected language
    filtered_df = df[df['Language'] == selected_language]

    # Generate heatmap using Plotly Express
    fig = px.choropleth(filtered_df, locations='State', locationmode='USA-states',
                        color=columns_to_display, scope='usa', hover_name='State',
                        title = f'{selected_language} Speakers - {selected_data.capitalize()} Heatmap',
                        color_discrete_map='Pastel')

    fig.update_layout(
        margin={
            't': 30, 'b': 0
            },
        coloraxis = {
            'colorbar': {
                'len': 0.7,
                'y': 0.15,
                'yanchor': 'bottom'
                }
            },
        title_x = 0.5,
        title_xanchor = 'center',
        title_xref = 'paper'
            )

    return fig
'''
def map_title(selected_data, selected_language)-> str:
    m_title = f'{selected_language} Speakers - {selected_data.capitalize()} Heatmap'
    return m_title
'''

app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1(id='header',
            children = 'Linguistic Diversity in the United States'
            ),
    html.Hr(),
    html.H3(id='data_h',
            children = "Data Selector"),
    dcc.RadioItems(
        id='data-selector',
        options=[
            {'label': 'Age', 'value': 'age'},
            {'label': 'Poverty', 'value': 'poverty'},
            {'label': 'Education', 'value': 'education'}
        ],
        value='age',
        labelStyle={'display': 'block'}
    ),
    html.H3(id='lang_h',
            children = "Language Selector"),
    dcc.RadioItems(
        id='language-selector',
        options=[
            {'label': 'Only English', 'value': 'Only English'},
            {'label': 'Spanish', 'value': 'Spanish'},
            {'label': 'Other Language', 'value': 'Other Language'}
        ],
        value='Only English',
        labelStyle={'display': 'block'}
    ),           
    html.Br(), 
    html.Br(),
    dcc.Graph(id='heatmap', 
              style={
                    'width': '70%', 
                    'height': '70vh',
                    'margin-top': '0px',
                    'margin-bottom': '0px'
                    },
              config={
                    'displayModeBar': False,
                    'scrollZoom': False,
                    #'autosizable': True
                    }),
    html.Hr()
])

# Define callback to update the heatmap based on selected data and language
@app.callback(
    Output('heatmap', 'figure'),
    [Input('data-selector', 'value'),
     Input('language-selector', 'value')]
)
def update_heatmap(selected_data, selected_language):
    return generate_heatmap(selected_data, selected_language)

#def update_m_title(selected_data, selected_language):
 #   return map_title(selected_data, selected_language)

if __name__ == '__main__':
    app.run_server(debug=True)
