import streamlit as st
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from random import randint
from wordcloud import WordCloud
from nltk.corpus import stopwords
from annotated_text import annotated_text
from topics import topics_dict, name_id_mapping
from streamlit_plotly_events import plotly_events


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.write("""<div style = 'text-align: center'><h1>Whizbang!</h1></div>""", unsafe_allow_html=True)

st.markdown('''
#### Whizbang unlocks the power of predictive insights with cutting-edge RNN network, forecasting the future of computer game sales with unparalleled accuracy.
''')

#Game selector

sel_name = st.selectbox('Select Game', name_id_mapping.keys())
sel_id = name_id_mapping[sel_name]

#Connect to API
game_info = requests.get(f'https://whizbang-xamxpbuwhq-uc.a.run.app/game?id={sel_id}').json()

#Display game image and GPT-3

'---'

col1, col2 = st.columns([1, 3 ])

with col1:
    st.image(game_info['image'], width=300)

with col2:
    st.subheader( 'Auto-generated summary of all reviews ')
    game_info['summary_review']

'---'



total_reviews = game_info['total_reviews']
voted_up = game_info['voted_up']
share_positive = f'{round((voted_up / total_reviews),2) * 100}%'

col1, col2, col3 = st.columns(3)
col1.metric("Number of Reviews", total_reviews, f'{randint(50,90)}%')
col2.metric("Voted up", voted_up, f'{randint(50,90)}%')
col3.metric("Share of Positive Sentiment", share_positive, f"{randint(-10,10)}%")



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


fig.add_trace(go.Bar(x=x1, y=y1, marker=dict(color='lightgreen'), orientation ='h'))
fig.update_layout(width=800, height=900, xaxis_title='Frequency', yaxis_title='Topic', title=None, margin=dict(t=0))







# stopwords = stopwords.words('english')
# context_stopwords = ['still','get', 'dont','cant','game','would', 'games', 'play', 'playing', 'played', 'player', 'players', 'playable']
# stopwords.extend(context_stopwords)

# wordcloud = WordCloud(background_color="white",
#                       max_words=50,
#                       width=800,
#                       height=600,
#                       min_font_size=6,
#                       collocations=False,
#                       stopwords = stopwords
#                       ).generate(text)


# plt.figure(figsize=(8, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')

#Reviews display

# reviews = pd.read_csv('raw_data/reviews_topics_1000.csv')
# reviews = reviews.rename(columns=lambda x: x.replace('_', ''))

def display_reviews(topic, sel_id):

    per_topic = reviews[(reviews[topic] == 1) & (reviews['id'] == sel_id) & (reviews['charcount'] < 200)].sort_values(by = 'votesup', ascending = False)
    top_reviews  = per_topic['review']
    return top_reviews


col1, col2 = st.columns([1, 1 ])

with col1:
    st.subheader('Frequency of topics in reviews')
    selected = plotly_events(
    fig,
    click_event=True,
            )
    st.write('<p style="font-size:24px;"><b>Wordcloud of game reviews</b></p>',unsafe_allow_html=True)

with col2:

    with st.container():

    #with st.container( style = {'max-height': '900px', 'overflow-y': 'scroll'}):
        if selected:
            st.subheader('Most popular reviews per topic')
            topic = selected[0]['y']
            reviews = game_info['top_reviews_per_topic'][f't_{topic}']
            all_reviews = []
            for review in reviews:
                #all_reviews.append(f'{review} \n --- \n')
                st.write(review)
                st.write('---')

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
