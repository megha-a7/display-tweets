[["text"]].sample(n=1).iat[0,0]) - returns a value to the query dataframe and since we dont want to return all the data we set sample(n=1) for just one randome tweets and since we want to return actual text of the tweet we pass the indexing function iat(), since we have insured we are returning only one sample we can be confident that our test is stored in the 0 row and 0 column.

select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='1') - key=1 because we don't want streamlit to confuse the state of 'sidebar' widget here with other widgets if we use the 'select' box once again

sentiment_count = data['airline_sentiment'].value_counts() - to count how many of each category/sentiment type is set up in each dataframe

syntax -  st.sidebar.slider("what the slider is",min value, max value)
instead of slider we could use a number input :
hour = st.sidebar.number_input("Hour of day",min_value=0 , max_value = 23)
