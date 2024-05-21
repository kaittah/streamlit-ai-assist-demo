import pandas as pd
import plotly.graph_objs as go
import random

def plot_order_priority_by_year(conn):
    sql = """
    SELECT
        EXTRACT(YEAR FROM O_ORDERDATE) AS ORDER_YEAR,
        O_ORDERPRIORITY,
        COUNT(*) AS ORDER_COUNT
    FROM
        ORDERS
    WHERE EXTRACT(YEAR FROM O_ORDERDATE) >= 1994
    GROUP BY
        EXTRACT(YEAR FROM O_ORDERDATE), O_ORDERPRIORITY
    ORDER BY
        ORDER_YEAR, O_ORDERPRIORITY
    """
    df = pd.read_sql(sql, conn)
    
    # Define a color scheme for the different priorities
    colors = {
        '1-URGENT': 'red',
        '2-HIGH': 'orange',
        '3-MEDIUM': 'yellow',
        '4-LOW': 'green',
        '5-NOT SPECIFIED': 'blue'
    }
    
    fig = go.Figure()
    for priority in df['O_ORDERPRIORITY'].unique():
        df_subset = df[df['O_ORDERPRIORITY'] == priority]
        fig.add_trace(go.Bar(
            x=df_subset['ORDER_YEAR'],
            y=df_subset['ORDER_COUNT'],
            name=priority,
            marker=dict(color=colors.get(priority, 'grey'))  # Use 'grey' for any unspecified priorities
        ))
    
    fig.update_layout(
        barmode='stack',
        title='Order Priority Distribution by Year',
        xaxis_title='Year',
        yaxis_title='Order Count',
        legend_title='Order Priority'
    )
    return fig



def plot_orders_revenue_by_year(conn):
    sql = """
    SELECT
        EXTRACT(YEAR FROM O_ORDERDATE) AS ORDER_YEAR,
        COUNT(*) AS ORDER_COUNT,
        SUM(O_TOTALPRICE) AS TOTAL_REVENUE
    FROM
        ORDERS
    WHERE EXTRACT(YEAR FROM O_ORDERDATE) >= 1994
    GROUP BY
        EXTRACT(YEAR FROM O_ORDERDATE)
    ORDER BY
        ORDER_YEAR
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['ORDER_YEAR'], y=df['ORDER_COUNT'], mode='lines', name='Order Count'))
    fig.add_trace(go.Scatter(x=df['ORDER_YEAR'], y=df['TOTAL_REVENUE'], mode='lines', name='Total Revenue', yaxis='y2'))
    
    fig.update_layout(
        title='Orders and Revenue by Year',
        yaxis=dict(title='Order Count'),
        yaxis2=dict(title='Total Revenue', overlaying='y', side='right')
    )
    return fig


def plot_top_customers_by_revenue(conn):
    sql = """
    SELECT
        C_CUSTKEY,
        C_NAME,
        SUM(O_TOTALPRICE) AS TOTAL_REVENUE
    FROM
        CUSTOMER
        JOIN ORDERS ON C_CUSTKEY = O_CUSTKEY
    WHERE EXTRACT(YEAR FROM O_ORDERDATE) >= 1994
    GROUP BY
        C_CUSTKEY, C_NAME
    ORDER BY
        TOTAL_REVENUE DESC
    LIMIT 10
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Bar(
        x=df['C_NAME'],
        y=df['TOTAL_REVENUE'],
    ))
    
    fig.update_layout(title='Top 10 Customers by Revenue')
    return fig


def plot_order_price_distribution(conn):
    sql = """
    SELECT
        O_TOTALPRICE
    FROM
        ORDERS
    WHERE EXTRACT(YEAR FROM O_ORDERDATE) >= 1994
    LIMIT 1000
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Histogram(
        x=df['O_TOTALPRICE'],
        nbinsx=50
    ))
    
    fig.update_layout(title='Distribution of Order Prices')
    return fig

def plot_discount(conn):
    sql = """
    SELECT
        L_DISCOUNT
    FROM
        LINEITEM
    LIMIT 1000
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Histogram(
        x=df['L_DISCOUNT'],
        nbinsx=10,
    ))
    
    fig.update_layout(title='Histogram of Discounts')
    return fig


def plot_ship_mode_by_year(conn):
    sql = """
    SELECT
        EXTRACT(YEAR FROM L_SHIPDATE) AS SHIP_YEAR,
        L_SHIPMODE,
        COUNT(*) AS ITEM_COUNT
    FROM
        LINEITEM
    GROUP BY
        EXTRACT(YEAR FROM L_SHIPDATE), L_SHIPMODE
    ORDER BY
        SHIP_YEAR, L_SHIPMODE
    """
    df = pd.read_sql(sql, conn)
    
    # Generate a random color for each ship mode
    unique_modes = df['L_SHIPMODE'].unique()
    colors = {mode: f'#{random.randint(0, 0xFFFFFF):06x}' for mode in unique_modes}
    
    fig = go.Figure()
    for mode in unique_modes:
        df_subset = df[df['L_SHIPMODE'] == mode]
        fig.add_trace(go.Bar(
            x=df_subset['SHIP_YEAR'],
            y=df_subset['ITEM_COUNT'],
            name=mode,
            marker=dict(color=colors[mode])
        ))
    
    fig.update_layout(
        barmode='stack',
        title='Line Item Ship Mode by Year',
        xaxis_title='Year',
        yaxis_title='Item Count',
        legend_title='Ship Mode'
    )
    return fig



def plot_supplier_costs_revenue(conn):
    sql = """
    SELECT
        S_SUPPKEY,
        SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE,
        SUM(L_EXTENDEDPRICE * L_DISCOUNT) AS COST
    FROM
        LINEITEM
        JOIN SUPPLIER ON L_SUPPKEY = S_SUPPKEY
    GROUP BY
        S_SUPPKEY
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['S_SUPPKEY'], y=df['REVENUE'], mode='lines', name='Revenue'))
    fig.add_trace(go.Scatter(x=df['S_SUPPKEY'], y=df['COST'], mode='lines', name='Cost', yaxis='y2'))
    
    fig.update_layout(
        title='Supplier Costs and Revenue',
        yaxis=dict(title='Revenue'),
        yaxis2=dict(title='Cost', overlaying='y', side='right')
    )
    return fig


def plot_part_types_count(conn):
    sql = """
    SELECT
        P_TYPE,
        COUNT(*) AS TYPE_COUNT
    FROM
        PART
    GROUP BY
        P_TYPE
    ORDER BY
        TYPE_COUNT DESC
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Bar(
        x=df['P_TYPE'],
        y=df['TYPE_COUNT'],
    ))
    
    fig.update_layout(title='Part Types Count')
    return fig


def plot_order_quantity_distribution(conn):
    sql = """
    SELECT
        L_QUANTITY
    FROM
        LINEITEM
    LIMIT 1000
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Histogram(
        x=df['L_QUANTITY'],
        nbinsx=50
    ))
    
    fig.update_layout(title='Order Quantity Distribution')
    return fig


def plot_revenue_vs_discount(conn):
    sql = """
    SELECT
        (L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE,
        L_DISCOUNT
    FROM
        LINEITEM
    LIMIT 1000
    """
    df = pd.read_sql(sql, conn)
    
    fig = go.Figure(go.Scatter(
        x=df['REVENUE'],
        y=df['L_DISCOUNT'],
        mode='markers'
    ))
    
    fig.update_layout(title='Revenue vs. Discount')
    return fig
