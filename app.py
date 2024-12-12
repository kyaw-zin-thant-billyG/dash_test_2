import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# Load the CSV file
data_file = "tranaction_count_amount(2024OCT).csv"
df = pd.read_csv(data_file)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout of the dashboard
app.layout = dbc.Container([

    html.H1("Transaction Dashboard", className="text-center my-4"),

    # Row for filters and chart type selection
    dbc.Row([
        dbc.Col([
            html.Label("Select Visualization Type:"),
            dcc.Dropdown(
                id="chart-type",
                options=[
                    {"label": "Transaction Count", "value": "txn"},
                    {"label": "Transaction Amount", "value": "amount"}
                ],
                value="txn",
                clearable=False
            )
        ], width=4),

        dbc.Col([
            html.Label("Select Transaction Types:"),
            dcc.Dropdown(
                id="transaction-filter",
                options=[
                    {"label": "Select All", "value": "all"}
                ] + [{"label": txn, "value": txn} for txn in df["transactiontypename"].unique()],
                value="all",
                multi=True
            )
        ], width=4),

        dbc.Col([
            html.Label("Select Chart Type:"),
            dcc.RadioItems(
                id="chart-choice",
                options=[
                    {"label": "Bar Chart", "value": 0},
                    {"label": "Pie Chart", "value": 1}
                ],
                value=0 
            )
        ], width=4)
    ], className="mb-4"),

    # Row for displaying the total transaction count, total amount, and chart
    dbc.Row([
        dbc.Col([
            # Card for displaying the total transaction count
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Transaction Count", className="card-title"),
                    html.H3(id="total-count", className="card-text")
                ])
            ], className="card-hover shadow-lg bg-light text-center rounded border-primary")  # Custom card class
        ], width=6),

        dbc.Col([
            # Card for displaying the total amount
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Transaction Amount", className="card-title"),
                    html.H3(id="total-amount", className="card-text")
                ])
            ], className="card-hover shadow-lg bg-light text-center rounded border-primary")  # Custom card class
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="visualization")
                ])
            ], className="mt-4 card-hover shadow-lg bg-light text-center rounded border-primary")  # Custom card class
        ], width=12)
    ])
], fluid=True)

# Callback for updating the chart, total transaction count, and total transaction amount
@app.callback(
    [Output("visualization", "figure"),
     Output("total-count", "children"),
     Output("total-amount", "children")],
    [Input("chart-type", "value"),
     Input("transaction-filter", "value"),
     Input("chart-choice", "value")]
)
def update_chart(chart_type, transaction_filter, chart_choice):
    # Filter data based on selection
    filtered_df = df if transaction_filter == "all" or "all" in transaction_filter else df[df["transactiontypename"].isin(transaction_filter)]

    # Calculate total transaction count (count of transactions, not dependent on chart type)
    total_transactions = filtered_df["txn"].sum()  # Use "txn" for transaction count

    # Calculate total transaction amount (sum of the "amount" column)
    total_amount = filtered_df["amount"].sum()

    if chart_choice == 0:
        # Bar chart
        fig = go.Figure(data=[
            go.Bar(x=filtered_df["transactiontypename"], y=filtered_df[chart_type], marker_color="blue")
        ])
        fig.update_layout(
            title="Transaction Types - Bar Chart",
            xaxis_title="Transaction Type",
            yaxis_title="Value",
            xaxis_tickangle=-45,
            xaxis_tickfont_size=10
        )
    else:
        # Pie chart
        fig = go.Figure(data=[
            go.Pie(labels=filtered_df["transactiontypename"], values=filtered_df[chart_type], hole=0)
        ])
        fig.update_layout(title="Transaction Types - Pie Chart")

    # Return the figure, total transaction count, and total amount
    return fig, f"{total_transactions:,.0f}", f"MMK - {total_amount:,.2f}"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
