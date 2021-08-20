from plotly import subplots
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#https://stackoverflow.com/questions/64176184/cant-import-plotly-express-in-py-script-despite-being-installed
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("The application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦 ")
st.sidebar.markdown("The application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦 ")

DATA_URL = r"C:\Users\Dexter\Desktop\streamlit1\Tweets.csv"
#stackoverflow.com/questions/37400974/unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3-trunca


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    print(data)
    #converting to pandas date-time format
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data= load_data()

st.sidebar.subheader("Show randome tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative' ))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])


st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets': sentiment_count.values})
#plotting
#hide visuallization if chosen
if not st.sidebar.checkbox("Hide", True, ):
    st.markdown("### Number of tweets by sentiment ")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

#plotting data in a map (conditions data contains column names :latitude and longitude, and they dont have any missing data in them)
#st.map(data) - produces clustered map of user location
#When and where are the users twitting from? - Using pandas to filter the clustered data in respect to time of day
st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='2'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" %(len(modified_data), hour, (hour+1)%24))
    #hour+1 = 60 min increment 
    #(hour+1)%24 - so that out of bounds values are not shown
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

#breaking airline tweets by sentiments
st.sidebar.subheader("Breakdown airline tweets by sentiments")
#use picks how many airlines they want to compare by allowing them to select one or more airlines at once
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = '3')

if len(choice) >0 :
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', 
        histfunc= 'count', color='airline_sentiment', facet_col='airline_sentiment', 
        labels={'airline_sentiment':'tweets'}, height=600, width=800)
        #splitting the coulmns or faceting the columns by positive, neutral and negative tweets
        #since airline_sentiment is ambiguos we provide label (optional), where 'airline_sentiments' gets renamed as 'tweets'
        #labels={'column-name':'renamed_name'}
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Which sentiment word cloud should be displayed?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key ='4'):
    st.header('Word cloud for %s sentiment' %(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords= STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
   





