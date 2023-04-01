import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
import plotly.express as px

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown(" This application is a Streamlit app used to analyze the sentiment of the tweets 🐦 about US airlines ✈️ ")
st.sidebar.markdown(" This application is a Streamlit app used to analyze the sentiment of the tweets 🐦 about US airlines ✈️ ")

DATA_URL = "https://raw.githubusercontent.com/singhishita/Interactive-Dashboards-With-Streamlit/master/Tweets.csv"
@st.cache_data(persist=True)
def load_data():
     data = pd.read_csv(DATA_URL)
     data['tweet_created'] = pd.to_datetime(data['tweet_created'])
     return data

data = load_data()


st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment type', ('positive','negative','neutral'))
st.sidebar.markdown(data.query('airline_sentiment== @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment type")
select = st.sidebar.selectbox('Vizualization type', ['Histogram', 'Pie Chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment' :sentiment_count.index, 'Tweets' :sentiment_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown("### Number of tweets by Sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are the users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='2'):
    st.markdown("### Tweets location based on the time of the day")
    st.markdown("%i, tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)