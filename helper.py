import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient
from os.path import exists
import warnings
warnings.filterwarnings("ignore")


@st.cache_data
def mongo_fetch():
    client = MongoClient('mongodb://localhost:27017')
    db = client['project']
    print(db)
    business_joined = db['business_cleaned']
    print(business_joined)
    cursor = business_joined.find()
    print(cursor)
    def batched(cursor, batch_size):
        batch = []
        for doc in cursor:
            batch.append(doc)
            if batch and not len(batch) % batch_size:
                yield batch
                batch = []

        if batch:   # last documents
            yield batch

    df = pd.DataFrame()
    for batch in batched(cursor, 10000):
        df = df.append(batch, ignore_index=True)
    df.to_json("business_cleaned.json")
    return df    

@st.cache_data
def get_data_1():
    if exists(r'source/business_cleaned.json'):
        df1 = pd.read_json(r"source/business_cleaned.json")
    else:
        df1 = mongo_fetch()
    df1['name'] = df1.name.str.replace('"','')
    df1['address'] = df1.address.str.replace('"','')
    df1.rename(columns = {'Categories':'Cuisines'}, inplace = True)
    return df1

@st.cache_data
def ready_map_data_tot(df):
    restaurants_reviews=df
    list_coor=restaurants_reviews[['name','latitude','longitude','stars']].drop_duplicates(keep='last')

    return list_coor

@st.cache_data
def ready_map_data_daily(df):
    restaurants_reviews=df
    list_coor=restaurants_reviews[['name','latitude','longitude','stars','is_restaurants']].drop_duplicates(keep='last')
    list_coor=list_coor[list_coor['is_restaurants']=='Yes']
    return list_coor[['name','latitude','longitude','stars']]

def filter_ch(ch):
    if ch=='1-Star':
        return (1,1.5)
    if ch=='2-Star':
        return (2,2.5)
    if ch=='3-Star':
        return (3,3.5)
    if ch=='4-Star':
        return (4,4.5)
    else:
        return (0,0)

@st.cache_resource
def get_map(t, ch):
    color_scale = [(0, 'red'), (1,'green')]
    ch_b,ch_end = filter_ch(ch)
    if ch!='None':
        if ch=='5-Star':
            t=t[t['stars']==5]
        else:    
            t=t[(t['stars']==ch_b) | (t['stars']==ch_end)]
    fig = px.scatter_mapbox(t, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name="name", 
                            hover_data=["name", "stars"],
                            color="stars",
                            color_continuous_scale=color_scale,
                            zoom=3)
    
                           
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis_colorbar_x=-0.15)
    return fig


def count_plot_total(df):
    df = df.city.value_counts()[:10]
    df = df.reset_index()
    return px.bar(df,x='index', y='city', color='city', color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])


def pie_chart_total(df):
    df = df.groupby('stars')['business_id'].count()
    df = df.reset_index()
    return px.pie(data_frame=df, values='business_id', names='stars', hole=0.5, color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])


def area_scatter(df):
    df_temp = df.state.value_counts()[:10]
    df_temp = df_temp.reset_index()
    grouped = df[['name','review_count','state','city','stars']].sort_values(by='review_count', ascending=False)[:10]
    fig1 = px.area(df_temp, x='index', y='state', color='state',
                   color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    # fig2 = px.scatter(grouped, x='name', y='review_count', color='review_count', size='review_count',
    #                   color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    fig2 = px.treemap(grouped, path=[px.Constant("world"), 'state', 'city','name','stars'], values='review_count',
                  color='review_count', hover_data=['name','stars'],
                  color_continuous_scale='RdBu')
                  #color_continuous_midpoint=np.average(df['review_count'], weights=df['stars']))
    fig2.update_traces(root_color="lightgrey")
    fig2.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig1, fig2

def violin_plot_tot(df):
    df= df.loc[df['is_restaurants']=='Yes']
    date_state = df[['stars','review_count']]
    x1 = date_state[(date_state['stars'] == 1) | (date_state['stars'] == 1.5)]['review_count']
    x2 = date_state[(date_state['stars'] == 2) | (date_state['stars'] == 2.5)]['review_count']
    x3 = date_state[(date_state['stars'] == 3) | (date_state['stars'] == 3.5)]['review_count']
    x4 = date_state[(date_state['stars'] == 4) | (date_state['stars'] == 4.5)]['review_count']
    x5 = date_state[(date_state['stars'] == 5)]['review_count']
    fig = go.Figure()
    fig.add_trace(go.Violin(y=x1, points='all',
                            box_visible=True, name='1-Star', line_color='#43bccd'))
    fig.add_trace(go.Violin(y=x2, points='all',
                            box_visible=True, name='2-Star', line_color='#662e9b'))
    fig.add_trace(go.Violin(y=x3, points='all',
                            box_visible=True, name='3-Star', line_color='#ea3546'))
    fig.add_trace(go.Violin(y=x4, points='all',
                            box_visible=True, name='4-Star', line_color='#8df542'))
    fig.add_trace(go.Violin(y=x5, points='all',
                            box_visible=True, name='5-Star', line_color='#f5a142'))
    fig.update_layout(
    title=go.layout.Title(
        text="Restaurant Count",
        x=0.5
    ))
    
    return fig


def get_st(df):
    t = df.groupby(['stars','state'])[['business_id']].count().reset_index()
    t['5stars']=""
    t.loc[(t['stars']==1) | (t['stars']==1.5),'5stars']=1
    t.loc[(t['stars']==2) | (t['stars']==2.5),'5stars']=2
    t.loc[(t['stars']==3) | (t['stars']==3.5),'5stars']=3
    t.loc[(t['stars']==4) | (t['stars']==4.5),'5stars']=4
    t.loc[t['stars']==5,'5stars']=5
    t=t.groupby(['state','5stars'])[['business_id']].sum()
    t=t.reset_index()
    t1=t[t['5stars']==1].sort_values(by='business_id',ascending=False)[:5]
    t2=t[t['5stars']==2].sort_values(by='business_id',ascending=False)[:5]
    t3=t[t['5stars']==3].sort_values(by='business_id',ascending=False)[:5]
    t4=t[t['5stars']==4].sort_values(by='business_id',ascending=False)[:5]
    t5=t[t['5stars']==5].sort_values(by='business_id',ascending=False)[:5]
    fig = make_subplots(rows=1, cols=5)
    fig.add_trace(
        go.Bar(x=t1.state, y=t1.business_id, name='1-Star',
               textangle=0, marker_color='#43bccd'),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=t2.state, y=t2.business_id, name='2-Star', marker_color='#662e9b'),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=t3.state, y=t3.business_id, name='3-Star', marker_color='#ea3546'),
        row=1, col=3
    )
    fig.add_trace(
        go.Bar(x=t4.state, y=t3.business_id, name='4-Star', marker_color='#8df542'),
        row=1, col=4
    )
    fig.add_trace(
        go.Bar(x=t5.state, y=t3.business_id, name='5-Star', marker_color='#f5a142'),
        row=1, col=5
    )
    fig.update_layout(title_text='T O P   5   S T A T E S', title_x=0.5, font=dict(
        family="Courier New, monospace",
        size=15,
        color='white'
    ))
    t=t1=t2=t3=t4=t5=None
    return fig


def pplott(df1, ch):
    df2 = df1.city.value_counts()[:10]
    df2 = df2.reset_index()
    f1= px.bar(df2,x='index', y='city', color='city', color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    df2 = df1.groupby('stars')['business_id'].count()
    df2 = df2.reset_index()
    f2 = px.pie(data_frame=df2, values='business_id', names='stars', hole=0.5, color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    date_state = df1.loc[df1['is_restaurants']=='Yes']
    date_state = date_state[['stars','review_count']]
    x1 = date_state[(date_state['stars'] == 1) | (date_state['stars'] == 1.5)]['review_count']
    x2 = date_state[(date_state['stars'] == 2) | (date_state['stars'] == 2.5)]['review_count']
    x3 = date_state[(date_state['stars'] == 3) | (date_state['stars'] == 3.5)]['review_count']
    x4 = date_state[(date_state['stars'] == 4) | (date_state['stars'] == 4.5)]['review_count']
    x5 = date_state[(date_state['stars'] == 5)]['review_count']
    f3 = go.Figure()
    f3.add_trace(go.Violin(y=x1, points='all',
                           box_visible=True, name='1-Star', marker_color='#43bccd'))
    f3.add_trace(go.Violin(y=x2, points='all',
                           box_visible=True, name='2-Star', marker_color='#662e9b'))
    f3.add_trace(go.Violin(y=x3, points='all',
                           box_visible=True, name='3-Star', marker_color='#ea3546'))
    f3.add_trace(go.Violin(y=x4, points='all',
                            box_visible=True, name='4-Star', line_color='#8df542'))
    f3.add_trace(go.Violin(y=x5, points='all',
                            box_visible=True, name='5-Star', line_color='#f5a142'))

    df_temp = df1.city.value_counts()[:10]
    df_temp = df_temp.reset_index()
    f4 = px.area(df_temp, x='index', y='city', color='city',
                   color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    return f1,f2,f3,f4

# def pplott1(states, ch):
#     st = states.loc[ch]
#     x = ['Confirmed', 'Recovered', 'Deceased']
#     if st.tolist()[0] == 0 and st.tolist()[1] == 0 and st.tolist()[2] == 0:
#         return 0, 0
#     f1 = px.bar(st, x=x, y=st.tolist(), color=x, color_discrete_sequence=[
#                '#43bccd','#ea3546','#662e9b'])
#     f2 = px.pie(st, names=x, values=st.tolist(), color_discrete_sequence=[
#                 '#43bccd','#ea3546','#662e9b'])
#     return f1, f2
