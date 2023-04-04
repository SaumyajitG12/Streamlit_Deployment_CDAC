from helper import *


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    layout="wide", page_title='Yelp Data | Overall', page_icon=r'pages\source\red.png')


df = get_data_1()

st.markdown("<h1 style='text-align: center; letter-spacing:12px;font-size: 65px; color: #ffffff;'>Yelp Restaurants</h1>", unsafe_allow_html=True)


st.text('')
st.text('')
st.text('')
st.text('')

c1, c2, c3 = st.columns(3)
tot = df.groupby('is_restaurants')[['business_id']].count().values.flatten().tolist()
new_tot = df.shape[0]
tot_open = df.is_open.value_counts()[1]
with c1:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{new_tot}</span><br><br><span>TOTAL BUSINESSES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c2:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- OVERALL DATA -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot[0]}</span><br><br><span>NON RESTAURANTS </span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c3:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot_open}</span><br><br><span>OPEN BUSINESSES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

c11, c22, c33 = st.columns(3)

restaurants = df[df['is_restaurants']=='Yes']
tt1 = restaurants['business_id'].count()
tt2 = restaurants[restaurants['is_open']==1]['business_id'].count()
tt3 = restaurants[restaurants['stars']==5][['business_id','review_count']]
tt3.review_count = tt3.review_count.astype(int)
tt3 = tt3[tt3['review_count']>10]['business_id'].count()

with c11:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt1)}</span><br><br><span>RESTAURANTS</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c22:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>-RESTAURANT DATA-</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt2)}</span><br><br><span>OPEN RESTAURANTS</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c33:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt3)}</span><br><br><span>5-STAR RESTAURANTS</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

ch = None

cc1, cc2, cc3 = st.columns(3)
with cc2:
    st.text('')
    st.text('')
    ch = st.selectbox('CHOOSE NO OF STARS', ['None','1-Star','2-Star','3-Star','4-Star','5-Star'])
    st.text('')
    st.text('')

col1, col2 = st.columns(2)

with col1:
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 18px; color: #ffffff;'>ALL BUSINESS</h5>", unsafe_allow_html=True)
    st.text('')
    df_map = ready_map_data_tot(df)
    m = get_map(df_map, ch)
    st.plotly_chart(m, width=680, height=810)
        

with col2:
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 18px; color: #ffffff;'>RESTAURANTS</h5>", unsafe_allow_html=True)
    st.text('')
    df_map = ready_map_data_daily(df)
    m = get_map(df_map, ch)
    st.plotly_chart(m, width=650, height=810)


col3, col4 = st.columns(2)
fig1, fig2 = area_scatter(df)

with col3:
    total_bar = count_plot_total(df)
    st.plotly_chart(total_bar, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    total_pie = pie_chart_total(df)
    st.plotly_chart(total_pie, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# values = st.slider(
#     'Limit minimum no of reviews',
#     0, 8000, )
# st.write('Values:', values)
p = violin_plot_tot(df)
st.plotly_chart(p, use_container_width=True)

plot = get_st(df)
st.plotly_chart(plot, use_container_width=True)

st.text('')
st.text('')

c4, c5, c6 = st.columns(3)

state_ch = None
state={'California': 'CA' , 'Missouri':'MO', 'Arizona':'AZ', 'Pennsylvania':'PA', 'Tennessee':'TN', 'Florida':'FL', 'Indiana':'IN', 'Louisiana':'LA', 'Alberta':'AB', 'Nevada':'NV',\
        'Idaho':'ID', 'Delaware':'DE', 'Illinois':'IL', 'New Jersey':'NJ', \
       'Hawaii':'HI', 'North Carolina':'NC', 'Colorado':'CO', 'Washington':'WA', 'South Dakota':'SD', 'Utah':'UT', 'Texas':'TX','XMS':'XMS', 'Montana':'MT', 'Michigan':'MI', \
       'Massachusetts':'MA', 'VI':'VI', 'Vermont':'VT'}
#temp = [state.append(x) for x in df.state.tolist() if x not in state]
with c5:
    state_ch = st.selectbox('CHOOSE STATE', state.keys())
    st.text('')
    state_ch= state[state_ch]

st.text('')
st.text('')
st.text('')

df1 = df.loc[df['state']==state_ch]
tot = df1.groupby('is_restaurants')[['business_id']].count().values.flatten().tolist()
new_tot = df1.shape[0]
tot_open = df1.is_open.value_counts()[1]


c7, c8, c9 = st.columns(3)

with c7:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{new_tot}</span><br><br><span>TOTAL BUSINESSES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c8:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- OVERALL -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot[1]}</span><br><br><span>NON RESTAURANTS</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c9:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot_open}</span><br><br><span>OPEN BUSINESSES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

st.text('')
st.text('')

f1, f2, f3, f4 = pplott(df1, state_ch)

c10, c11, c12, c13 = st.columns([1, 2, 2, 1])

with c11:
    st.plotly_chart(f1, use_container_width=True)

with c12:
    st.plotly_chart(f2, use_container_width=True)

c14, c15 = st.columns(2)

with c14:
    st.plotly_chart(f3, use_container_width=True)

with c15:
    st.plotly_chart(f4, use_container_width=True)


# c71, c81, c91 = st.columns(3)

# with c71:
#     st.text('')
#     st.text('')
#     st.text('')
#     st.text('')
#     st.text('')
#     st.markdown(
#         f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Confirmed']))}</span><br><br><span>CONFIRMED CASES</span></h5>", unsafe_allow_html=True)
#     st.text('')
#     st.text('')
#     st.text('')

# with c81:
#     st.markdown(
#         f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- {date_.split(':')[1].strip().upper()} -</h5>", unsafe_allow_html=True)
#     st.text('')
#     st.text('')
#     st.markdown(
#         f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Recovered']))}</span><br><br><span>RECOVERED CASES</span></h5>", unsafe_allow_html=True)
#     st.text('')
#     st.text('')
#     st.text('')

# with c91:
#     st.text('')
#     st.text('')
#     st.text('')
#     st.text('')
#     st.text('')
#     st.markdown(
#         f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Deceased']))}</span><br><br><span>DECEASED CASES</span></h5>", unsafe_allow_html=True)
#     st.text('')
#     st.text('')
#     st.text('')


# f11, f21 = pplott1(states_recent, state_ch)

# if f11 != 0 and f21 != 0:
#     c111, c121 = st.columns(2)

#     with c111:
#         st.plotly_chart(f11, use_container_width=True)

#     with c121:
#         st.plotly_chart(f21, use_container_width=True)
