import plotly.graph_objects as go
import pandas as pd

def plot_menu_items_by_category(conn):
    # Function to plot count of menu items by category
    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    category_counts = dataframe['item_category'].value_counts()
    fig = go.Figure([go.Bar(x=category_counts.index, y=category_counts.values)])
    fig.update_layout(title="Count of Menu Items by Category", xaxis_title="Category", yaxis_title="Count")
    fig.show()

def plot_cost_vs_sale_price(conn):
    # Function to plot cost of goods vs sale price
    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    fig = go.figure(data=go.scatter(x=dataframe['cost_of_goods_usd'], y=dataframe['sale_price_usd'], mode='markers', text=dataframe['menu_item_name']))
    fig.update_layout(title="Cost of Goods vs Sale Price", xaxis_title="Cost of Goods (USD)", yaxis_title="Sale Price (USD)")
    fig.show()

def plot_menu_type_distribution(conn):
    # Function to plot distribution of menu types
    dataframe = pd.read_sql("SELECT * FROM menu", conn)
    menu_type_counts = dataframe['menu_type'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=menu_type_counts.index, values=menu_type_counts.values)])
    fig.update_layout(title="Distribution of Menu Types")
    fig.show()
