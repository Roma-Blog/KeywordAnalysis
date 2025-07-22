from keyword_analysis import ListFile, GlobalData
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

list_file = ListFile()
data = GlobalData(list_file.list_file_data)

# Создание Dash приложения
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='word-dropdown',
        options=[{'label': word, 'value': word} for word in data.data_words['word'].unique()],
        multi=True,
        placeholder='Выберите слова для анализа'
    ),
    dcc.Dropdown(
        id='exclude-word-dropdown', 
        options=[{'label': word, 'value': word} for word in data.data_words['word'].unique()],
        multi=True,
        placeholder='Выберите слова для исключения'
    ),
    dcc.Dropdown(
        id='word-dropdown',
        options=[{'label': word, 'value': word} for word in data.data_words['word'].unique()],
        multi=True,
        placeholder='Выберите слова'
    ),
    dcc.Dropdown(
        id='source-dropdown',
        options=[{'label': source, 'value': source} for source in data.data_words['source'].unique()],
        multi=True,
        placeholder='Выберите источники'
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=data.data_words['date'].min(),
        end_date=data.data_words['date'].max(),
        display_format='YYYY-MM-DD',
        start_date_placeholder_text='Выберите начальную дату',
        end_date_placeholder_text='Выберите конечную дату'
    ),
    dcc.RadioItems(
        id='timeframe-radio',
        options=[
            {'label': 'По дням', 'value': 'daily'},
            {'label': 'По неделям', 'value': 'weekly'}
        ],
        value='daily',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='visits-graph')
])

@app.callback(
    Output('visits-graph', 'figure'),
    Input('word-dropdown', 'value'),
    Input('exclude-word-dropdown', 'value'), 
    Input('source-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('timeframe-radio', 'value')
)

#Обновление графика
def update_graph(selected_words, exclude_words, selected_sources, start_date, end_date, timeframe):
    filtered_df = data.data_words.copy()
    
    if selected_words:
        filtered_df = filtered_df[filtered_df['word'].isin(selected_words)]
    if exclude_words:
        filtered_df = filtered_df[~filtered_df['word'].isin(exclude_words)]
    if selected_sources:
        filtered_df = filtered_df[filtered_df['source'].isin(selected_sources)]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]
    if timeframe == 'weekly':
        grouped_df = filtered_df.resample('W-Mon', on='date').sum().reset_index()
    else:
        grouped_df = filtered_df.groupby('date', as_index=False).sum()

    #Рисование графика
    fig = px.bar(grouped_df, 
                 x='date', 
                 y='visits', 
                 title='Суммарные визиты по выбранным словам и источникам')
    
    fig.update_layout(
        xaxis_title='Дата',
        yaxis_title='Количество визитов',
        hovermode='x unified'
    )
    
    return fig

#Запуск сервера по адресу http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run(debug=True)