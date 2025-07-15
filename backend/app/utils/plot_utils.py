import plotly.graph_objects as go
import pandas as pd

def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """
    Creates a line chart using Plotly.

    Args:
        df: DataFrame containing the data.
        x_col: The name of the column to be used for the x-axis.
        y_col: The name of the column to be used for the y-axis.
        title: The title of the chart.

    Returns:
        A Plotly Figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers'))
    fig.update_layout(title_text=title, xaxis_title=x_col, yaxis_title=y_col)
    return fig

def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """
    Creates a bar chart using Plotly.

    Args:
        df: DataFrame containing the data.
        x_col: The name of the column to be used for the x-axis.
        y_col: The name of the column to be used for the y-axis.
        title: The title of the chart.

    Returns:
        A Plotly Figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[x_col], y=df[y_col]))
    fig.update_layout(title_text=title, xaxis_title=x_col, yaxis_title=y_col)
    return fig
