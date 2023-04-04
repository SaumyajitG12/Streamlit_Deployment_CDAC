import streamlit as st
import base64
import webbrowser
st.set_page_config(
    page_title="Multipage App",
    page_icon=r"source\185979.png",
    layout="wide"
)
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(r"source\back-modified.png")
col1, col2, col3 = st.columns([3,5,1])

with col1:
    st.write("")

with col2:
    st.image(r"source\red.png", caption=None, width=500, use_column_width=False, clamp=False, channels="RGB", output_format="auto")

with col3:
    st.write("")

st.markdown("<h1 style='text-align: center; color: white;'>Welcome to YelpAnalytics</h1>", unsafe_allow_html=True)
st.markdown("The objective of this project is to analyze and draw business insights from the **Yelp dataset** using visualizations and machine learning. \
            The data was stored in **MongoDB** and then a pipeline was created to warehouse the data in **pySpark** for cleaning and pre-processing. \
            The data was stored back in **MongoDB** and then pipelined into **Tableau** and pandas for **Visualizations(Seaborn, plotly, matplotlib, folium)** \
            followed by in-depth business analysis. A **sentiment analysis** machine learning model was built to analyze customer reviews along with a **recommender system** \
            to recommend new restaurants. Then dashboarding and deployment of ML models were achieved using **Streamlit**.")
col1, col2, col3,col4, col5, col6 = st.columns([2,2,1,2,1,2])

with col1:
    st.write("")

with col2:
    st.write("")

with col3:
    url = 'https://www.yelp.com/dataset'
    if st.button('Yelp Dataset'):
        webbrowser.open_new_tab(url)

with col4:
    url2 = 'https://www.yelp.com/dataset/documentation/main'
    if st.button('Documentation'):
        webbrowser.open_new_tab(url2)
with col5:
    st.write("")

with col6:
    st.write("")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")



col1,col2,col3,col4,col5,col6 = st.columns([2,2,1,1,2,1])

with col1:
    st.image(r"source\Apache_Spark_logo.svg.png", caption=None, width=150, use_column_width=False, clamp=False, channels="RGB", output_format="auto")
with col2:
    st.image(r"source\MongoDB_Logo.svg.png", caption=None, width=200, use_column_width=False, clamp=False, channels="RGB", output_format="auto")   
with col3:
    st.image(r"source\pythonlogo.png", caption=None, width=150, use_column_width=False, clamp=False, channels="RGB", output_format="auto")
with col4:
    st.write("")
with col5:
    st.image(r"source\Tableau-Logo.png", caption=None, width=200, use_column_width=False, clamp=False, channels="RGB", output_format="auto")
with col6:
    st.image(r"source\1200px-Scikit_learn_logo_small.svg.png", caption=None, width=150, use_column_width=False, clamp=False, channels="RGB", output_format="auto")

                

footer="""<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with passion by  PG-DBDA Group-2, guided by - Krishnanjan Sir <a style='display: block; text-align: center;' href="https://www.cdac.in/index.aspx?id=acts" target="_blank">Centre for Development of Advanced Computing</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
st.sidebar.success("Select a page above.")