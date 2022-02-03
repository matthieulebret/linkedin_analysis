
import streamlit as st

import altair as alt

import plotly.express as px
# import plotly.graph_objects as go

import numpy as np
import pandas as pd
import datetime as dt
from timeit import default_timer as timer
import calendar
from datetime import date, timedelta,time,datetime
import xlrd
import openpyxl

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

st.set_page_config('LinkedIn app',layout='wide')


st.title('Analysis of LinkedIn data')

def isTitle(string):
    mdlist = ['MD','Managing Director','Head','HEAD','Chief','chief','CEO','Managing','Partner','General','Founder','fondateur','Fondateur','Senior Portfolio Manager','President','Global','Owner','COO','CRO','CFO','CAO','Board','Chairman','Vice Chairman','Gérant','Directeur','head','founder','GENERAL','général','Fondatrice','Associée','Strategic Advisor','Leiter']
    dlist = ['Director','Senior Vice President','SVP','Principal','Lead','lead','Responsable','Senior Manager','Manager','Senior Investment Officer','Senior Financial','Sr Vice','manager','direktor','Direktor']
    vplist = ['Vice President','VP','Vice-President']
    avplist = ['Assistant','AVP']
    anasslist = ['Analyst','Associate']
    if 'Executive Assistant' in string:
        return 'Other'
    elif any([title in string for title in mdlist]) and 'Vice' not in string or string =='Vice Chairman':
        return 'MD'
    elif any([title in string for title in dlist]) and 'Managing' not in string:
        return 'D'
    elif any([title in string for title in vplist]) and 'Senior' not in string:
        return 'VP'
    elif any([title in string for title in avplist]):
        return 'AVP'
    elif any([title in string for title in anasslist]):
        return 'An/Ass'
    else:
        return 'Other'


@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def getdata():
    network = pd.read_csv('C:/Users/matth/Documents/pythonprograms/LinkedIn_post_NordLB/data/Connections.csv',header=3)

    network['Connected On'] = pd.to_datetime(network['Connected On'],errors='coerce')
    network['Connected Year']=pd.DataFrame(network['Connected On']).apply(lambda x: x.dt.year)
    network = network.dropna(subset=['Company'],axis=0)
    network = network.dropna(subset=['Group'],axis=0)
    network['Count']=1

    network['Rank'] = network['Position'].apply(isTitle)

    return network

network = getdata()

selectyear = st.slider('Select years',2005,2022,(2013,2022),step=1)

network = network[(network['Connected Year']>=selectyear[0])&(network['Connected Year']<=selectyear[1])]



col1,col2,col3,col4,col5,col6 = st.columns(6)
with col1:
    st.metric('MD contacts','{:,.2%}'.format(network[network['Rank']=='MD'].count()[0]/network.count()[0]))
with col2:
    st.metric('D contacts','{:,.2%}'.format(network[network['Rank']=='D'].count()[0]/network.count()[0]))
with col3:
    st.metric('VP contacts','{:,.2%}'.format(network[network['Rank']=='VP'].count()[0]/network.count()[0]))
with col4:
    st.metric('AVP contacts','{:,.2%}'.format(network[network['Rank']=='AVP'].count()[0]/network.count()[0]))
with col5:
    st.metric('An/Ass contacts','{:,.2%}'.format(network[network['Rank']=='An/Ass'].count()[0]/network.count()[0]))
with col6:
    st.metric('Other contacts','{:,.2%}'.format(network[network['Rank']=='Other'].count()[0]/network.count()[0]))

st.write(network)

# names = network['Company'].unique().tolist()
# st.write(len(names))

# for compare in names:
#     st.write((names[0],compare,fuzz.ratio(names[0],compare)))
# i=2
#
# socgen = [(names[i],compare,fuzz.ratio(names[i],compare)) for compare in names if fuzz.ratio(names[i],compare)>45]
# st.write(socgen)

fig = px.histogram(network,x='Connected Year', color='Rank',title='My Connections',category_orders=dict(Rank=['MD','D','VP','AVP','An/Ass','Other']))
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)

fig = px.treemap(network,path=['Group','Rank','Position'],values='Count',hover_data=['Last Name','First Name'])
st.plotly_chart(fig)
