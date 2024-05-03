import pandas as pd
import plotly.express as px

def plot_tracks(conn):
    df_tracks = pd.read_sql(
        '''SELECT tracks.trackid, genres.name AS genre 
            FROM tracks 
            LEFT JOIN genres on tracks.genreid = genres.genreid
        ''', conn
    )
    tracks_per_genre = df_tracks.groupby('genre').size().reset_index(name='Count')
    fig = px.bar(tracks_per_genre, x='genre', y='Count', title='Number of Tracks per Genre')
    return fig

def plot_customer_states(conn):
    df_tracks = pd.read_sql(
        '''SELECT customerid, state AS state
            FROM customers
        ''', conn
    )
    tracks_per_genre = df_tracks.groupby('state').size().reset_index(name='Count')
    fig = px.bar(tracks_per_genre, x='state', y='Count', title='Number of Customers per Sate')
    return fig

def plot_hired_employees(conn):
    df_employees = pd.read_sql(
        '''SELECT date(strftime('%Y-%m-1', hiredate)) AS hiremonth
        FROM employees
        ''', conn
    )
    hires_per_month = df_employees.groupby('hiremonth').size().reset_index(name='Count')
    fig = px.line(hires_per_month, x='hiremonth', y='Count', title='Number of New Hires')
    return fig