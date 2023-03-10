import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from random import randint
from wordcloud import WordCloud
from nltk.corpus import stopwords


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Create API client.

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Load time series data
time_series = pd.read_csv("raw_data/time_series_test.csv")


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=10000)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("""SELECT * FROM `whizbang.whizbang_dataset.topics_1000_grouped`""")

'''
# Whizbang!
'''

st.markdown('''
#### Whizbang unlocks the power of predictive insights with cutting-edge RNN network, forecasting the future of computer game sales with unparalleled accuracy.
''')

# Build df.
df_game = pd.DataFrame(rows)
df_game = df_game.sort_values(by='_comment_count', ascending=False)

sel_id = st.selectbox('**Select Game y**', df_game.id)
fil_df = df_game[df_game.id == sel_id]  # filter

comment_metric = fil_df['_comment_count']
av_comments = round(df_game['_comment_count'].mean(),2)
comment_share = int(int(comment_metric) / av_comments) * 100

voted_up_metric = fil_df['_voted_up']
av_voted_up = round(df_game['_voted_up'].mean(),2)
voted_up_share = int(int(voted_up_metric) / av_voted_up) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Number of Reviews", comment_metric, f'{comment_share}%')
col2.metric("Voted up", voted_up_metric, f'{voted_up_share}%')
col3.metric("Share of Positive Sentiment", f'{randint(50,90)}%', f"{randint(-10,10)}%")

# Build a new df based from filter.
new_df = pd.melt(fil_df, id_vars=['id'], var_name="Game",
                 value_vars=[column for column in df_game.columns[5:]])

new_df = new_df.sort_values(by='value')

logy = True  # to make small values visible
textauto = True  # to write plot label
title = f'Game ID: {sel_id}'


# Create data for the first bar chart
x1 = time_series['month']
y1 = time_series['ts_units_sold']
# Create data for the second bar chart
x2 = time_series['month']
y2 = time_series['ts_discount']
# Create data for the third bar chart
x3 = new_df['value']
y3 = new_df['Game']

# Add the first bar chart to the subplot
fig1 = go.Figure(data=[go.Bar(x=x1, y=y1, marker=dict(color='darkgreen'))])
fig1.update_layout(title='Units Sold per month', xaxis_title='Units Sold', yaxis_title='Month-Year',
                       title_font=dict(
                                    family="Arial",
                                    size=24,
                                    color="black"
                                    ),
                           xaxis=dict(
                                tickfont=dict(
                            size=14
                                )))



fig2 = go.Figure(data=[go.Bar(x=x2, y=y2, marker=dict(color='darkred'))])
fig2.update_layout(width=800, height=400, title='Discount per month', xaxis_title='Discount', yaxis_title='Month-Year',
                                    title_font=dict(
                                    family="Arial",
                                    size=24,
                                    color="black"
                                    ))

# Add the second bar chart to the subplot
fig3 = go.Figure(data=[go.Bar(x=x3, y=y3, marker=dict(color='lightgreen'), orientation ='h')])
fig3.update_layout(width=800, height=800, title=f'Most popular topics for Game {sel_id}', xaxis_title='Topic', yaxis_title='Frequency',
                                    title_font=dict(
                                    family="Arial",
                                    size=24,
                                    color="black"
                                    ))

@st.cache_data(ttl=10000)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

text_per_id = run_query(f"""SELECT * FROM `whizbang.whizbang_dataset.text_per_id_1000`
                        ORDER BY _char_count DESC
                        LIMIT 20""")

text_per_id = pd.DataFrame(text_per_id)
text = text_per_id[text_per_id['_id'] == sel_id]['_clean_text'].values[0]
stopwords = stopwords.words('english')
context_stopwords = ['still','get', 'dont','cant','game','would', 'games', 'play', 'playing', 'played', 'player', 'players', 'playable']
stopwords.extend(context_stopwords)

wordcloud = WordCloud(background_color="white",
                      max_words=50,
                      width=800,
                      height=600,
                      min_font_size=6,
                      collocations=False,
                      stopwords = stopwords
                      ).generate(text)


plt.figure(figsize=(8, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

#Reviews display

def display_reviews(topic, sel_id):

    per_topic = reviews[reviews[topic] == 1].sort_values(by = 'votesup', ascending = False)
    per_id_per_topic = per_topic[per_topic['id'] == sel_id].head(10)
    top_reviews  = per_id_per_topic['review']
    return top_reviews.iloc[0]

# Call the function to create the bar charts

col2, col3 = st.columns([1, 1 ])
#with col1:
#    with st.container():
#        st.plotly_chart(fig1, use_container_width=True)
#    with st.container():
#        st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.plotly_chart(fig3, use_container_width=False)
    st.write('<p style="font-size:24px;"><b>Wordcloud of game reviews</b></p>',unsafe_allow_html=True)
    st.pyplot()
with col3:
    st.write('<p style="font-size:24px;"><b>Uncover most popular reviews per topic</b></p>',unsafe_allow_html=True)
    if st.button('AI'):
        topic = 'ai'
        review = display_reviews(topic, sel_id)
        st.code(f'{review}')




reviews = pd.read_csv('raw_data/reviews_topics_1000.csv')



# col1, col2 = st.columns([1, 1])
# with col1:
#     st.plotly_chart(fig2, use_container_width=True)
# with col2:
#     st.pyplot()


st.write("Look up a raw dataframe for comparison")
st.dataframe(df_game, use_container_width=True)




#Vertical barchart

#fig = px.bar(new_df, x='Game', y='value',
#             height=300, log_y=logy, text_auto=textauto,
#             title=title)

#with st.expander('**Game Info**', expanded=True):
#    st.plotly_chart(fig, use_container_width=True)
