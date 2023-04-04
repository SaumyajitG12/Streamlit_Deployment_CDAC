import streamlit as st
# NLP Pkgs
import nltk
from textblob import TextBlob
import pandas as pd
import numpy as np
import nltk
import pickle
import xgboost
import plotly.graph_objects as go
from io import StringIO
# Emoji
import emoji
import plotly.express as px


# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Data Viz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

st.set_page_config(
    page_title="Sentiment",
    layout="wide",
    page_icon=r"source/185979.png",
)


model=pickle.load(open(r'source/sentiment_analysis_model.p','rb'))
# Fetch Text From Url
@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text



def main():
	"""Yelp Sentiment Analysis"""

	st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Yelp-Sentiment Analysis</h1>", unsafe_allow_html=True)

	activities = ["Single Review","Text Analysis from CSV","About"]
	choice = st.sidebar.selectbox("Choice",activities)
	
	# Choice = Sentiment
	if choice == 'Single Review':
		result=0.5
		st.subheader("Review Sentiment Analyser")
		raw_text = st.text_area("Enter Your Text","Type Here")
		if st.button("Analyze"):
			result=model.predict([raw_text])[0]
			if result ==1:
				custom_emoji = ':smile:'
				st.markdown('Sentiment :: {}'.format(custom_emoji))
			else:
				custom_emoji = ':disappointed:'
				st.markdown('Sentiment :: {}'.format(custom_emoji))
			fig = go.Figure(go.Indicator(
			domain = {'x': [0, 1], 'y': [0, 1]},
			value = result,	
			mode = "gauge",
			title = {'text': "Sentiment"},
			gauge = {'axis': {'range': [-0.5, 1.5]},
	    		'bar':{'color':'yellow'},
				'steps' : [
					{'range': [-0.5, 0.5], 'color': "red"},
					{'range': [0.5, 1.5], 'color': "green"}],
				'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 0.5}}))
			st.plotly_chart(fig,use_container_width=True)			
		
	
	# Choice Text Analysis
	if choice == 'Text Analysis from CSV':
		st.subheader("Analysis on Text From CSV")
		uploaded_file = st.file_uploader("Choose a file")
		st.info("Please insure your CSV doesn't have index!")
		if uploaded_file is not None:
			new_df = pd.read_csv(uploaded_file,index_col=False)
			st.dataframe(data=new_df, width=800, height=None, use_container_width=True)
			col1, col2, col3 = st.columns([2,1,2])
			if col2.button('Analyse'):
				#Plot
				new_df['prediction']=model.predict(new_df.iloc[:, 0])
				result_avg = new_df['prediction'].value_counts()[1]/new_df['prediction'].count()
				st.write(result_avg)
				st.markdown('##### Majority Sentiment of CSV')
				if result_avg > 0.5:
					custom_emoji = ':smile:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))
				elif result_avg < 0.5:
					custom_emoji = ':disappointed:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))
				else:
					custom_emoji = ':expressionless:'
					st.markdown('Sentiment :: {}'.format(custom_emoji))
				col1,col2 = st.columns([1,1])
				col1.dataframe(data=new_df, width=None, height=None, use_container_width=False)
				with col2:
					fig = px.pie(data_frame=new_df, values=new_df.prediction.value_counts(), names=['positive','negetive']	, hole=0.5, color_discrete_sequence=['#43bccd','#ea3546'])
					st.plotly_chart(fig, use_container_width=True)
					# fig1, ax1 = plt.subplots()
					# ax1.pie(new_df['prediction'].value_counts(), autopct='%1.1f%%',shadow=True, startangle=90)
					# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
					# st.pyplot(fig1)
				def convert_df(df):
					return df.to_csv().encode('utf-8')

				csv = convert_df(new_df)
				col1, col2, col3 = st.columns([2,1,2])
				col2.download_button(
					label="Download data as CSV",
					data=csv,
					file_name='Predicted_df.csv',
					mime='text/csv',
				)

	# Choice Abou
	if choice == 'About':
		st.subheader("About")
		st.markdown("""
			#### Sentiment Analysis Web App
			##### Built with Streamlit

			#### By
			+ Data Preparation & Model by : Charudutta Marne, Jyoti Chaudhary and Sourabh Jamdade
			+ UI and Integration : Saumyajit Guha 

			""")
		

if __name__ == '__main__':
	main()