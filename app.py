import streamlit as st
import pandas as pd
import preprocessor, helper # type: ignore
import plotly.express as px # type: ignore

import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('1. Athlete_Events.csv')
region_df=pd.read_csv('2. NOC_Regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("OLYMPICS ANALYSIS")
st.sidebar.image('Flag.png')


user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally=helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("RANK (1896-2016)")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " in " + str(selected_year) + " Olympics")

    st.table(medal_tally) #Rather than dataframe function

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("TOP STATISTICS")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig=px.line(nations_over_time, x="Edition", y="region")
    st.title("PARTICIPATING NATIONS")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("EVENTS OVER THE YEARS")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("NUMBER OF ATHLETES OVER THE YEARS")
    st.plotly_chart(fig)

    st.title("NUMBER OF EVENTS OVER THE YEARS")
    fig,ax = plt.subplots(figsize=(30,30))

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)

    st.pyplot(fig)

    st.title("MOST SUCCESSFUL ATHLETES")
    sport_list=df['Sport'].unique().tolist()
    sport_list = [str(sport) for sport in sport_list]
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title("MEDAL TALLY OVER THE YEARS")
    st.plotly_chart(fig)

    st.title("PROGRESS")
    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)

    st.pyplot(fig)

    st.title("TOP 10 ATHLETES OF THE COUNTRY")
    top10_df=helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)