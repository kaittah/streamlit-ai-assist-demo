import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def plot_total_sales_over_time(conn):
    sql = "SELECT DATE(ORDERED_AT) AS ORDER_DATE, SUM(ORDER_TOTAL) AS TOTAL_SALES FROM ORDERS GROUP BY ORDER_DATE ORDER BY ORDER_DATE"
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ORDER_DATE'], y=df['TOTAL_SALES'], mode='lines+markers', name='Total Sales'))
    fig.update_layout(title='Total Sales Over Time', xaxis_title='Order Date', yaxis_title='Total Sales')
    return fig

def plot_avg_order_value_by_customer(conn):
    sql = "SELECT CUSTOMER_ID, AVG(ORDER_TOTAL) AS AVG_ORDER_VALUE FROM ORDERS GROUP BY CUSTOMER_ID ORDER BY 2"
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['CUSTOMER_ID'], y=df['AVG_ORDER_VALUE'], name='Avg Order Value'))
    fig.update_layout(title='Average Order Value by Customer', xaxis_title='Customer ID', yaxis_title='Average Order Value')
    return fig

def plot_num_orders_by_customer(conn):
    sql = "SELECT CUSTOMER_ID, COUNT(*) AS NUM_ORDERS FROM ORDERS GROUP BY CUSTOMER_ID ORDER BY 2"
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['CUSTOMER_ID'], y=df['NUM_ORDERS'], name='Number of Orders'))
    fig.update_layout(title='Number of Orders by Customer', xaxis_title='Customer ID', yaxis_title='Number of Orders')
    return fig

def plot_product_sales_distribution(conn):
    sql = "SELECT PRODUCT_NAME, COUNT(*) AS TOTAL_SALES FROM ORDER_ITEMS GROUP BY PRODUCT_NAME"
    df = pd.read_sql(sql, conn)
    fig = px.pie(df, names='PRODUCT_NAME', values='TOTAL_SALES',
              color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(
        title='Product Sales Distribution',
        title_x=0.5,
    )

    return fig

def plot_top_customers_by_total_sales(conn):
    sql = "SELECT CUSTOMER_ID, SUM(ORDER_TOTAL) AS TOTAL_SALES FROM ORDERS GROUP BY CUSTOMER_ID ORDER BY TOTAL_SALES DESC LIMIT 10"
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['CUSTOMER_ID'], y=df['TOTAL_SALES'], name='Total Sales'))
    fig.update_layout(title='Top 10 Customers by Total Sales', xaxis_title='Customer ID', yaxis_title='Total Sales')
    return fig

def plot_monthly_sales_trend(conn):
    sql = "SELECT DATE_TRUNC('month', ORDERED_AT) AS MONTH, SUM(ORDER_TOTAL) AS TOTAL_SALES FROM ORDERS GROUP BY MONTH ORDER BY MONTH"
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['MONTH'], y=df['TOTAL_SALES'], mode='lines+markers', name='Total Sales'))
    fig.update_layout(title='Monthly Sales Trend', xaxis_title='Month', yaxis_title='Total Sales')
    return fig


def plot_sales_by_product_category(conn):
    sql = """
    SELECT PRODUCT_TYPE, SUM(PRODUCTS.PRODUCT_PRICE) AS TOTAL_SALES 
    FROM ORDER_ITEMS 
    JOIN PRODUCTS ON ORDER_ITEMS.PRODUCT_ID = PRODUCTS.ID 
    GROUP BY PRODUCT_TYPE
    """
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['CATEGORY'], y=df['TOTAL_SALES'], name='Total Sales'))
    fig.update_layout(title='Sales by Product Category', xaxis_title='Category', yaxis_title='Total Sales')
    return fig

def plot_sales_by_region(conn):
    sql = """
    SELECT REGION, SUM(ORDER_TOTAL) AS TOTAL_SALES 
    FROM ORDERS 
    JOIN CUSTOMERS ON ORDERS.CUSTOMER_ID = CUSTOMERS.ID 
    GROUP BY REGION
    """
    df = pd.read_sql(sql, conn)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['REGION'], y=df['TOTAL_SALES'], name='Total Sales'))
    fig.update_layout(title='Sales by Region', xaxis_title='Region', yaxis_title='Total Sales')
    return fig