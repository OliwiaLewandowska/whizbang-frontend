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
    st.subheader( 'AI Generated review')
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


st.subheader('Cummulative Sales Over Time & Forecast')

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

logy = True  # to make small values visible
textauto = True  # to write plot label
title = f'{sel_name}'

sorted_topics = dict(sorted(game_info['topic_names'].items(), key=lambda x: x[1]))

# Create data for the third bar chart
x1 = list(sorted_topics.values())
y1 = [i.replace('t_', '') for i in list(sorted_topics.keys())]

# Add the second bar chart to the subplot
#fig = go.Figure(data=[go.Bar(x=x1, y=y1, marker=dict(color='lightgreen'), orientation ='h')])
fig = go.Figure()


fig.add_trace(go.Bar(x=x1[5:], y=y1[5:], marker=dict(color='blue'), orientation ='h'))
fig.update_layout(
    width=900,
    height=600,
    xaxis_title='Frequency',
    yaxis_title='Topic',
    title=None,
    margin=dict(t=0),
    plot_bgcolor='rgb(255, 255, 255)',
    paper_bgcolor='rgb(255, 255, 255)',
    # don't display modebar
    modebar=dict(orientation="v"),

)


col1, col2 = st.columns([1, 1 ])

with col1:
    st.subheader('Frequency of topics in reviews')

    selected = plotly_events(
    fig,
    click_event=True,
    override_height=600
            )

with col2:

    with st.container():

        if selected:
            topic = selected[0]['y']
            st.subheader(f'Most popular reviews talking about: {emoji_dict[topic]} {topic.capitalize()}')
            reviews = game_info['top_reviews_per_topic'][f't_{topic}']
            html_string = ""
            for review in reviews:
                #st.write(review.replace("[","<").replace("]","/>"))
                #st.write('---')
                html_string += f'<p style="font-family: \'IBM Plex Sans\', sans-serif;">{review.replace("[","<").replace("]","/>")}</p><br><hr>'
            html(html_string, height=600, scrolling=True)
        else:
            st.subheader('Most popular reviews')
            st.write('Click on a topic to see the most popular reviews for that topic')

#Sentiment Over time

data_all = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/alldata').json()

topic_per_date = pd.DataFrame(data_all['topic_per_date'])

if selected:
        topic = selected[0]['y']
        st.subheader(f'Share of positive and negative sentiment for: {emoji_dict[topic]} {topic.capitalize()}')
        fig2 = plot_yearly_avg_weighted(topic, topic_per_date)
        st.plotly_chart(fig2, use_container_width=True)



    # st.write('<p style="font-size:24px;"><b>Uncover most popular reviews per topic</b></p>',unsafe_allow_html=True)
    # if st.button('AI'):
    #     topic = 'ai'
    #     for i in range(5):
    #         review = display_reviews(topic, sel_id)
    #         #st.write(review.iloc[i])
    #         words = review.iloc[i].split()
    #         annotated_words = []
    #         for i, word in enumerate(words):
    #             if i < len(words) - 1 and words[i].lower() == "ai":
    #                 annotated_words.append((word, "*"))
    #             else:
    #                 annotated_words.append(f"{word} ")
    #         annotated_text(*annotated_words)
    #         st.write("---")


#selected_points = plotly_events(fig, hover_event = True)

#st.session_state.counter = 0



#st.write(selected_points['x'])
#print(selected_points)

# string = "This is a review about ai yes"
# words = string.split()  # split the string into a list of words
# annotated_words = []
# for i, word in enumerate(words):
#     if i < len(words) - 1 and words[i] == "ai":
#         annotated_words.append((word, "*"))
#     else:
#         annotated_words.append(f"{word} ")

# with st.echo():
#     annotated_text(*annotated_words)
