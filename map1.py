from dash import Dash, dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


####### TO-DO  #################
# color bar:
    # what shoul the scale be?
    # how to anchor it and set size?
    # how to make it closer to graph?
# layout:
    # how to set radios next to each other and dropdown below data radio?
    # edit style choices
    
# MAKE SURE IT WORKS FROM GIT HUB

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

app = Dash(__name__)

# Define app layout
app.layout = html.Div(
    style = {'margin' : 'auto',
             'width' : '75%'#,
             #'display': 'flex'
            },
    children = [
    html.P(id='header',
            children = 'Linguistic Diversity in the United States',
            style = {'fontSize': 30, 'fontFamily': "Balto"}
            ),
    html.Hr(),
    html.P(id='data_h',
                children = "Data Selector",
                style = {'fontSize': 20, 'fontFamily': "Balto"}),
    dcc.RadioItems(
        id='data-selector',
        options=[
            {'label': 'Age', 'value': 'Age'},
            {'label': 'Poverty', 'value': 'Poverty'},
            {'label': 'Education', 'value': 'Education'}
                ],
        value='Age',
        labelStyle={'display': 'block'}
        ),
    html.P(id='options',
        children= "Please choose a demographic.",
        style = {'fontSize': 15, 'fontFamily': "Balto"}),
    dcc.Dropdown(id='dropdown',
        clearable=False,
        searchable=False),
    html.P(id='lang_h',
            children = "Language Selector",
            style = {'fontSize': 20, 'fontFamily': "Balto"}),
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
    dcc.Graph(id='heatmap', 
              style={
                    'width': '100%', 
                    'height': '70vh',
                    'margin-top': '0px',
                    'margin-bottom': '0px'
                    },
              config={
                    'displayModeBar': False,
                    'scrollZoom': False,
                    }),
    html.Hr()
    ]
)

@app.callback(
        [Output('dropdown', 'options'),
         Output('dropdown', 'value')],
        Input('data-selector', 'value'))

def dropdown_options(data_value):
    if data_value == 'Age':
        options = [{'label':'Age 5 to 17', 'value': '5 to 17' },
        {'label': 'Age 18 to 64', 'value': '18 to 64'}, 
        {'label':'Age 65+', 'value':'65+'}]
        value = '5 to 17'

    elif data_value == 'Poverty':
        options = [{'label':'Below poverty level', 'value': 'Below poverty level' },
        {'label': 'At or above poverty level', 'value': 'At or above poverty level'}]
        value = 'Below poverty level'

    else: # data_value == "Education":
        cols = ['Less than high school graduate', 'High school graduate',
                'Some college or associate\'s degree', 'Bachelor\'s degree or higher']
        options = [{'label': x, 'value': x} for x in cols]
        value = 'Less than high school graduate'

    return options, value


# Define callback to update the heatmap based on selected data and language
@app.callback(
    Output('heatmap', 'figure'),
    [Input('dropdown', 'value'),
     Input('language-selector', 'value')]
)

def generate_heatmap(dropdown_value, lang_value):
    

    # Filter dataframe based on selected language
    filtered_df = df[df['Language'] == lang_value]

    # Generate heatmap using Plotly Express
    fig = px.choropleth(filtered_df, locations='State', locationmode='USA-states',
                        color=dropdown_value, scope='usa', hover_name='State',
                        title = f'{lang_value} Speakers - {dropdown_value.capitalize()} Heatmap',
                        color_continuous_scale='Viridis'#,
                        #range_color = [0, df[dropdown_value].max()]
                        )

    fig.update_layout(
        coloraxis = {
            'colorbar': {
                'len': 0.7,
                'y': 0.15,
                'yanchor': 'bottom'
                }
            },
        title_font_size = 25,
        title_x= 0.5,
        title_xanchor= 'center',
        title_xref= 'paper',
        font_family = 'Balto'
        )

    return fig

#def update_heatmap(selected_data, selected_language):
 #   return generate_heatmap(selected_data, selected_language)

#def update_m_title(selected_data, selected_language):
 #   return map_title(selected_data, selected_language)

if __name__ == '__main__':
    app.run_server(debug=True)
