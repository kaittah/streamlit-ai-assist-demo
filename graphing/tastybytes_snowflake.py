import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

#  Graphs particular to the Tastybytest Snowflake Sample Dataset

def plot_menu_items_by_category(conn):
    # Function to plot count of menu items by category
    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    dataframe.columns = dataframe.columns.str.lower()
    category_counts = dataframe['item_category'].value_counts()
    fig = go.Figure([go.Bar(x=category_counts.index, y=category_counts.values)])
    fig.update_layout(title="Count of Menu Items by Category", xaxis_title="Category", yaxis_title="Count")
    return fig

def plot_cost_vs_sale_price(conn):
    # Function to plot cost of goods vs sale price

    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    dataframe.columns = dataframe.columns.str.lower()
    fig = go.Figure(data=go.Scatter(x=dataframe['cost_of_goods_usd'], 
                                    y=dataframe['sale_price_usd'], 
                                    mode='markers', 
                                    text=dataframe['menu_item_name']))
    fig.update_layout(title="Cost of Goods vs Sale Price", 
                      xaxis_title="Cost of Goods (USD)", 
                      yaxis_title="Sale Price (USD)")
    
    return fig

def plot_menu_type_distribution(conn):
    # Function to plot distribution of menu types
    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    dataframe.columns = dataframe.columns.str.lower()
    menu_type_counts = (
        dataframe['menu_type']
        .value_counts()
        .rename("count")
        .reset_index()
    )
    fig = px.pie(menu_type_counts, names='menu_type', values='count',
              color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(title="Distribution of Menu Types")
    return fig


def plot_cost_distribution(conn):
    # Function to plot distribution of costs
    dataframe = pd.read_sql("SELECT cost_of_goods_usd FROM menu", conn)
    dataframe.columns = dataframe.columns.str.lower()
    fig = px.histogram(dataframe, x="cost_of_goods_usd", nbins=30)
    fig.update_layout(title="Distribution of Cost of Goods")
    return fig
    return fig