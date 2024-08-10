import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index().rename(columns={'region': 'Region'})

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Year','Games','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count':col}, inplace=True)

    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset='Medal')

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df_reset = temp_df['Name'].value_counts().reset_index()
    temp_df_reset.columns = ['Name_Index', 'count']
    result = temp_df_reset.head(15).merge(df, left_on='Name_Index', right_on='Name', how='left')[['Name_Index', 'count', 'Sport', 'region']].drop_duplicates()

    result.rename(columns={'Name_Index': 'Name', 'count': 'Medals', 'region': 'Country'}, inplace=True)

    return result

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset='Medal')

    temp_df = temp_df[temp_df['region'] == country]

    temp_df_reset = temp_df['Name'].value_counts().reset_index()
    temp_df_reset.columns = ['Name_Index', 'count']
    result = temp_df_reset.head(15).merge(df, left_on='Name_Index', right_on='Name', how='left')[
        ['Name_Index', 'count', 'Sport']].drop_duplicates()

    result.rename(columns={'Name_Index': 'Name', 'count': 'Medals', 'region': 'Country'}, inplace=True)

    return result