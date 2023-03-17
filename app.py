import streamlit as st
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from random import randint
from wordcloud import WordCloud
from nltk.corpus import stopwords
from annotated_text import annotated_text
from topics import topics_dict, name_id_mapping, plot_yearly_avg_weighted
from streamlit_plotly_events import plotly_events
from PIL import Image
from streamlit.components.v1 import html
import numpy as np
import pandas as pd



st.set_page_config(layout="wide", page_title="Whizbang !", page_icon=Image.open('favicon.png'))
st.set_option('deprecation.showPyplotGlobalUse', False)




#st.write("""<div style = 'text-align: center'><h1>Whizbang!</h1></div>""", unsafe_allow_html=True)

emoji_dict = {"gameplay":"🎮","graphics":"🎨","story":"📚","sound":"🔉","controls":"🕹️","multiplayer":"⛹️‍♀️","crossplay":"🎭","ai":"🤖",
 "performance":"💪","price":"💰","length":"📏","difficulty":"👷","replayability":"🌟","fun":"🦩","immersion":"🌊",
 "art":"🖼️","pacing":"🏃‍♀️","variety":"🔢","balance":"⚖️","bugs":"🐛"}

cola, colb, colc, cold, cole = st.columns([1,3,1,3,1])

with colb:
    image = Image.open('logo.png')
    st.image(image, width=500)

with cold:
    sel_name = st.selectbox('Select Game', name_id_mapping.keys())



#st.markdown('''
#### Whizbang unlocks the power of predictive insights with cutting-edge RNN network, forecasting the future of computer game sales with unparalleled accuracy.
#''')

#Game selector


'---'
sel_id = name_id_mapping[sel_name]

#Connect to API
game_info = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/game?id={sel_id}').json()



#Display game image and GPT-3

col1, col2 = st.columns([1, 3 ])

with col1:
    st.image(game_info['image'], width=300)

with col2:
    st.subheader( 'AI Generated Review')
    game_info['summary_review']

total_reviews = game_info['total_reviews']
voted_up = game_info['voted_up']
share_positive = f'{round((voted_up / total_reviews) * 100, 2)}%'
primary_genre = game_info['genre1']
secondary_genre = game_info['genre2']


col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 2, 2 ])
col1.metric("Primary Genre", primary_genre)
if secondary_genre == 0:
    st.write('')
else:
    col2.metric("Secondary Genre", secondary_genre)
col3.metric("Number of Reviews", total_reviews)
col4.metric("Voted up", voted_up)
col5.metric("Share of Positive Sentiment", share_positive)

'---'


#Display Forecast


st.subheader('Cumulative Sales Over Time & Forecast')

dates = list(game_info['sales_data'].keys())[0:-1]

actual = list(game_info['sales_data'].values())[0:-1]
predicted = list(game_info['sales_data'].values())#.pop(-2)
predicted.pop(-2)

actual_cum = np.cumsum(actual)
predicted_cum = np.cumsum(predicted)

# Find the index of the first non-zero value in y_values
start_index = next((i for i, y in enumerate(actual) if y > 0), len(actual))

# Adjust the x_values to start at the correct index
dates = dates[start_index:]

# Create a Plotly figure
fig = go.Figure()

# Add a trace for the timeseries & add color

fig.add_trace(go.Scatter(x=dates, y=predicted_cum[start_index:], mode='lines', name = 'predicted', line=dict(color='red', dash = 'dash', width = 3)))
fig.add_trace(go.Scatter(x=dates, y=actual_cum[start_index:], mode='lines', name = 'actual', line=dict(color='lightgrey', width = 3)))

# Update the layout
fig.update_layout(
    #title='Sales prediction',
    margin=dict(t=0),
    xaxis_title='Date',
    yaxis_title='Total Sales',
    xaxis_tickformat='<br>%Y'
)


col1, col2 = st.columns([5, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:

    with st.container():
        st.metric("Predicted Sales", '{:,}'.format(int(predicted[-1])))
        '---'
    with st.container():
        st.metric("Actual Sales", '{:,}'.format(int(actual[-1])))


'---'

#Load & transform data for barchart

game_info = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/game?id=4720').json()
df = pd.DataFrame(game_info['ts_reviews'])

df_new = df.iloc[:,2:42]

result = df_new.sum(axis=0)

#Subset only the values that have positive/negative in the name
positive = result[result.index.str.contains('positive')]
negative = result[result.index.str.contains('negative')]

positive.index = positive.index.str.replace('t_','').str.replace('_positive','')
negative.index = negative.index.str.replace('t_','').str.replace('_negative','')

all_numpy = np.array(positive) + np.array(negative)

all = pd.Series(all_numpy, index = positive.index)
all_sorted = all.sort_values(ascending=True)

#Sort positive with the order of all
positive_sorted = positive.reindex(all_sorted.index)
negative_sorted = negative.reindex(all_sorted.index)

categories = list(positive.index)
positive = list(positive_sorted)
negative = list(negative_sorted)

default_topic = categories[-1]

# Create the positive/negative per topics CHART

trace1 = go.Bar(x=positive, y=categories, name='Positive', marker_color='green', orientation='h')
trace2 = go.Bar(x=negative, y=categories, name='Negative', marker_color='red', orientation='h')

# Define the layout
layout = go.Layout(
                   xaxis_title='Frequency of a Topic in Reviews',
                   barmode='relative',
                   width=900,
                   height=900,
                   margin=dict(t=0)
                   )

# Create the figure
fig = go.Figure(data=[trace1, trace2], layout=layout)


col1, col2 = st.columns([1, 1 ])

with col1:
    st.subheader('Frequency of Topics in Reviews')

    selected = plotly_events(
    fig,
    click_event=True,
    override_height=600
            )

with col2:

    with st.container():

        topic = default_topic if not selected else selected[0]['y']
        st.subheader(f'Most Popular Reviews Talking About: {emoji_dict[topic]} {topic.capitalize()}')
        reviews = game_info['top_reviews_per_topic'][f't_{topic}']
        html_string = ""
        for review in reviews:
            #st.write(review.replace("[","<").replace("]","/>"))
            #st.write('---')
            html_string += f'<p style="font-family: \'IBM Plex Sans\', sans-serif;">{review.replace("[","<").replace("]","/>")}</p><br><hr>'
        html(html_string, height=600, scrolling=True)


'---'


#Topics per Genre

genre = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/alldata').json()
df = pd.DataFrame(genre['topic_per_game'])
topics = [column for column in df.columns if column.startswith('t_')]
df_topics = df[topics]

sums = df_topics.sum()
sorted_sums = sums.sort_values(ascending=False)

top_10 = sorted_sums.head(10)

columns_to_keep = list(top_10.index)
columns_to_keep.append('Genre 1')
df_new = df[columns_to_keep]

grouped = df_new.groupby('Genre 1').sum().reset_index()
grouped_sorted = grouped.sort_values(by='t_story', ascending=False)
small_grouped = grouped_sorted.iloc[0:10]

#Topics per Genre VISUALISATION

data = {
    'Genre': list(small_grouped['Genre 1']),
    'Story': list(small_grouped.iloc[:,1]),
    'Fun': list(small_grouped.iloc[:,2]),
    'Gameplay': list(small_grouped.iloc[:,3]),
    'Bugs': list(small_grouped.iloc[:,4]),
    'Price': list(small_grouped.iloc[:,5]),
    'Sound': list(small_grouped.iloc[:,6]),
    'Immersion': list(small_grouped.iloc[:,7]),
    'Art': list(small_grouped.iloc[:,8]),
    'Controls': list(small_grouped.iloc[:,9]),
    'Graphics': list(small_grouped.iloc[:,10])
}
df = pd.DataFrame(data)

# calculate percentages
df_perc = df.set_index('Genre').apply(lambda x: x/x.sum(), axis=1)

# create bar chart
fig3 = go.Figure()
for i, topic in enumerate(df.columns[1:]):
    fig3.add_trace(go.Bar(
        x=df['Genre'],
        y=df_perc[topic],
        name=topic,
        marker_color=px.colors.qualitative.Plotly[i]
    ))

fig3.update_layout(
    xaxis_title='Genre',
    yaxis_title='% of Total',
    barmode='stack',
    margin=dict(t=0)
)

#Sentiment Over time

data_all = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/alldata').json()

topic_per_date = pd.DataFrame(data_all['topic_per_date'])
col1, col2 = st.columns([1, 1 ])
with col1:
    topic = default_topic if not selected else selected[0]['y']
    st.subheader(f'Share of Positive and Negative Sentiment for: {emoji_dict[topic]} {topic.capitalize()}')
    fig2 = plot_yearly_avg_weighted(topic, topic_per_date)
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.subheader(f'Distribution of Topics per Genre')
    st.plotly_chart(fig3, use_container_width=True)

## Most similar games
'---'
st.subheader('Most Similar Games, by Topic Sentiment')
col1, col2, col3 = st.columns([1, 1, 1])
columns = [col1, col2, col3 ]
colindex = 0
for id in game_info["closest_games"].keys():
    game_response = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/game?id={id}').json()
    with columns[colindex]:
        st.write(game_response['name'])
        st.image(game_response['image'], width=200)
        colindex += 1
