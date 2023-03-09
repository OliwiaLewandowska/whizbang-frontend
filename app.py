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

st.set_page_config(layout="wide")

# Create API client.

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT * FROM `whizbang.whizbang_dataset.topics_1000_grouped`")

'''
# Whizbang!
'''

st.markdown('''
Select Game & explore key metrics
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

# Create horizontal bar chart
fig = go.Figure()
fig.add_trace(go.Bar(
    y=new_df['Game'],
    x=new_df['value'],
    orientation='h'
))
fig.update_layout(
    height=700,
    title=title,
    xaxis_type='log' if logy else 'linear',
    showlegend=False,
    yaxis=dict(title='Game')
)
if textauto:
    fig.update_traces(texttemplate='%{value:.2s}', textposition='inside')

# display the Plotly chart directly in Streamlit
st.plotly_chart(fig)

st.dataframe(df_game, use_container_width=True)

#Vertical barchart

#fig = px.bar(new_df, x='Game', y='value',
#             height=300, log_y=logy, text_auto=textauto,
#             title=title)

#with st.expander('**Game Info**', expanded=True):
#    st.plotly_chart(fig, use_container_width=True)
