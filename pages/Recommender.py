import streamlit as st 
import streamlit.components.v1 as stc 
import joblib
import scipy
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
# Load EDA
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
from scipy.spatial.distance import cdist

st.set_page_config(
    layout="wide", page_title='Yelp Data | Recommender', page_icon=r'pages\source\red.png')
# Load Our Dataset
@st.cache_data
def load_data():
	df_business = pd.read_csv(r"source/df_business.csv")
	df_business_only = pd.read_csv(r"source/df_business_only.csv")
	vectorizer_reviews = joblib.load(r'source/vectorizer_reviews.pkl')
	vectorized_reviews=scipy.sparse.load_npz(r"source/vectorized_reviews.npz")
	# vectorized_categories=scipy.sparse.load_npz(r"source/vectorized_categories.npz")
	businessxreview=scipy.sparse.load_npz(r"source/businessxreview.npz")
	return df_business,df_business_only,vectorizer_reviews,vectorized_reviews,businessxreview

# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(df_business_only):
	vectorizer_categories = CountVectorizer(min_df = 1, max_df = 1., tokenizer = lambda x: x.split(', '))
	vectorized_categories = vectorizer_categories.fit_transform(df_business_only['categories'])
	return vectorizer_categories,vectorized_categories



# Recommendation Sys
def get_recommendation(business_choose,df_business,df_business_only,vectorizer_reviews,vectorized_reviews,businessxreview,vectorizer_categories,vectorized_categories):
	new_reviews = df_business.loc[df_business['business_id'] == business_choose, 'text']
	new_categories = df_business_only.loc[df_business_only['business_id'] == business_choose, 'categories']
	dists1 = cdist(vectorizer_reviews.transform(new_reviews).todense().mean(axis=0),vectorized_reviews.T.dot(businessxreview).T.todense(), metric='correlation')
	dists2 = cdist(vectorizer_categories.transform(new_categories).todense().mean(axis=0), vectorized_categories.todense(),metric='correlation')
	dists_together = np.vstack([dists1.ravel(), dists2.ravel()]).T
	dists = dists_together.mean(axis=1)
	closest = dists.argsort().ravel()[:10]
	final_recommended_courses=df_business_only.loc[df_business_only['business_id'].isin(df_business_only['business_id'].iloc[closest]), ['business_id', 'categories', 'name', 'stars']]
	return final_recommended_courses


RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p style="color:blue;"><span style="color:black;">⭐Star Rating::</span>{}</p>
<p style="color:blue;"><span style="color:black;">🔤Name</span><a href="{}",target="_blank">Link</a></p>
<p style="color:blue;"><span style="color:black;">🆔Business_Id:</span>{}</p>
<p style="color:blue;"><span style="color:black;">📊Categories:</span>{}</p>
</div>
"""


def main():

	st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Tampa Restaurant Recommender</h1>", unsafe_allow_html=True)

	menu = ["List of Restaurants","Recommend","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	df_business,df_business_only,vectorizer_reviews,vectorized_reviews,businessxreview = load_data()
	vectorizer_categories,vectorized_categories=vectorize_text_to_cosine_mat(df_business_only)
	

	if choice == "List of Restaurants":
		st.subheader("Home")
		st.dataframe(df_business_only,use_container_width=True)
		text=st.text_input("Enter Restaurant Name", value="", type="default", help="Enter name close to the one you want", placeholder="The Floridian", label_visibility="visible")
		if st.button("Search"):
			if text != '':
				df_result_search = df_business_only[df_business_only['name'].str.contains(text, case=False, na=False)]
				st.dataframe(df_result_search,use_container_width=True)
            

	elif choice == "Recommend":
		st.subheader("Recommend Restaurants")
		search_term = st.text_input("Restaurant ID")
		if st.button("Recommend"):
			if search_term is not None:
				try:
					results = get_recommendation(search_term,df_business,df_business_only,vectorizer_reviews,vectorized_reviews,businessxreview,vectorizer_categories,vectorized_categories)
					results=results.reset_index(drop=True)
					st.dataframe(results)
					with st.expander("Results as JSON"):
						results_json = results.to_dict('index')
						st.write(results_json)

					for index,row in results.iterrows():
						rec_title = row['name']
						rec_score = row['stars']
						rec_url = row['business_id']
						rec_num_sub = row['categories']

						# st.write("Title",rec_title,)
						stc.html(RESULT_TEMP.format(rec_score,rec_title,rec_url,None,rec_num_sub),height=350)
				except Exception as e:
					st.write(e)
					results= "Not Found"
					st.warning(results)



				# How To Maximize Your Profits Options Trading




	else:
		st.subheader("About")
		st.text("Built with Streamlit & Pandas")


if __name__ == '__main__':
	main()
