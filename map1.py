from dash import Dash, html

def main() -> None:
    app = Dash()
    app.title = "Language Diversity in USA"
    app.layout = create_layout(app)
    create_map(app)
    app.run()

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className = "app-div",
        children = [
            html.H1(app.title),
            html.Hr()
        ]
    )

def US_map(metric_name: str,
                df: pd.DataFrame,
              ) -> go.Figure:

    metric_id = get_metric_key(metric_name)

    fig = px.choropleth(data_frame=df,
                        scope = "usa",
                        locations='State',
                        color=metric_id,
                        hover_name='State',
                        hover_data={'State': False},
                        range_color = [0, data[metric_id].max()],
                        labels={metric_id: metric_name}
                    )
    fig.update_layout(
        margin={
            't': 0, 'b': 0
            },
        coloraxis = {
            'colorbar': {
                'len': 0.7,
                'y': 0.15,
                'yanchor': 'bottom'
                }
            }
            )
    return fig


if __name__ == "__main__":
    main()