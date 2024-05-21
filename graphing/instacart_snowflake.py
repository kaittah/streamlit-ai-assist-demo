import pandas as pd
import plotly.graph_objs as go

def plot_top_aisles_by_products(conn):
    query = """
    SELECT A.AISLE, COUNT(P.PRODUCT_ID) AS NUM_PRODUCTS
    FROM PRODUCTS P
    JOIN AISLES A ON P.AISLE_ID = A.AISLE_ID
    GROUP BY A.AISLE
    ORDER BY NUM_PRODUCTS DESC
    LIMIT 10
    """
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Bar(x=df['AISLE'], y=df['NUM_PRODUCTS'])])
    fig.update_layout(title='Top 10 Aisles by Number of Products', xaxis_title='Aisle', yaxis_title='Number of Products')
    return fig


def plot_order_hour_histogram(conn):
    query = "SELECT ORDER_HOUR_OF_DAY FROM ORDERS LIMIT 1000"
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Histogram(x=df['ORDER_HOUR_OF_DAY'], nbinsx=24)])
    fig.update_layout(title='Histogram of Order Hour of Day', xaxis_title='Hour of Day', yaxis_title='Frequency')
    return fig

def plot_order_dow_vs_hour(conn):
    query = "SELECT ORDER_DOW, ORDER_HOUR_OF_DAY FROM ORDERS LIMIT 1000"
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Scatter(x=df['ORDER_DOW'], y=df['ORDER_HOUR_OF_DAY'], mode='markers')])
    fig.update_layout(title='Order Day of Week vs. Order Hour of Day', xaxis_title='Day of Week', yaxis_title='Hour of Day')
    return fig

def plot_reordered_vs_nonreordered(conn):
    query = """
    SELECT REORDERED, COUNT(PRODUCT_ID) AS NUM_PRODUCTS
    FROM ORDERS_PRODUCTS
    GROUP BY REORDERED
    """
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Bar(x=['Non-Reordered', 'Reordered'], y=df['NUM_PRODUCTS'])])
    fig.update_layout(title='Reordered vs. Non-Reordered Products', xaxis_title='Reordered', yaxis_title='Number of Products')
    return fig

def plot_orders_and_avg_days(conn):
    query_orders = "SELECT ORDER_DOW, COUNT(ORDER_ID) AS NUM_ORDERS FROM ORDERS GROUP BY ORDER_DOW ORDER BY ORDER_DOW"
    query_avg_days = "SELECT ORDER_DOW, AVG(DAYS_SINCE_PRIOR_ORDER) AS AVG_DAYS FROM ORDERS GROUP BY ORDER_DOW ORDER BY ORDER_DOW"
    
    df_orders = pd.read_sql(query_orders, conn)
    df_avg_days = pd.read_sql(query_avg_days, conn)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_orders['ORDER_DOW'], y=df_orders['NUM_ORDERS'], mode='lines+markers', name='Number of Orders'))
    
    fig.update_layout(title='Number of Orders by Day of Week', xaxis_title='Day of Week', yaxis_title='Value')
    return fig

def plot_top_departments_by_products(conn):
    query = """
    SELECT D.DEPARTMENT, COUNT(P.PRODUCT_ID) AS NUM_PRODUCTS
    FROM PRODUCTS P
    JOIN DEPARTMENTS D ON P.DEPARTMENT_ID = D.DEPARTMENT_ID
    GROUP BY D.DEPARTMENT
    ORDER BY NUM_PRODUCTS DESC
    LIMIT 10
    """
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Bar(x=df['DEPARTMENT'], y=df['NUM_PRODUCTS'])])
    fig.update_layout(title='Top 10 Departments by Number of Products', xaxis_title='Department', yaxis_title='Number of Products')
    return fig

def plot_days_since_prior_order_histogram(conn):
    query = "SELECT DAYS_SINCE_PRIOR_ORDER FROM ORDERS LIMIT 1000"
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Histogram(x=df['DAYS_SINCE_PRIOR_ORDER'])])
    fig.update_layout(title='Histogram of Days Since Prior Order', xaxis_title='Days Since Prior Order', yaxis_title='Frequency')
    return fig

