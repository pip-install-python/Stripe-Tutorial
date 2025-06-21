import stripe
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
from dash import html, dcc, register_page

# Register this page
register_page(__name__, path='/analytics', name='Analytics')

# Import stripe from main
import __main__

stripe = __main__.stripe


def fetch_revenue_data():
    """Fetch payment data from Stripe for the last 30 days"""
    # Get data from the last 30 days
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

    revenue_data = []
    payments = stripe.PaymentIntent.list(
        limit=100,
        created={'gte': thirty_days_ago}
    )

    for payment in payments.data:
        if payment.status == 'succeeded':
            revenue_data.append({
                'date': datetime.fromtimestamp(payment.created).date(),
                'amount': payment.amount / 100,  # Convert to dollars
                'currency': payment.currency.upper(),
                'description': payment.description or 'Payment'
            })

    return pd.DataFrame(revenue_data) if revenue_data else pd.DataFrame()


def create_revenue_chart(revenue_df):
    """Create revenue visualization"""
    if revenue_df.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No payment data found in the last 30 days",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(
            title="Revenue Overview (Last 30 Days)",
            height=400
        )
        return fig

    # Group by date and calculate daily revenue
    daily_revenue = revenue_df.groupby('date').agg({
        'amount': ['sum', 'count']
    }).reset_index()
    daily_revenue.columns = ['date', 'revenue', 'volume']

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add revenue bar chart
    fig.add_trace(
        go.Bar(
            x=daily_revenue['date'],
            y=daily_revenue['revenue'],
            name='Daily Revenue ($)',
            marker_color='lightblue',
            yaxis='y'
        )
    )

    # Add volume line chart
    fig.add_trace(
        go.Scatter(
            x=daily_revenue['date'],
            y=daily_revenue['volume'],
            name='Transaction Volume',
            line=dict(color='red', width=3),
            yaxis='y2'
        )
    )

    # Update layout with dual y-axes
    fig.update_layout(
        title='Revenue and Transaction Volume (Last 30 Days)',
        xaxis_title='Date',
        yaxis=dict(
            title='Revenue ($)',
            side='left'
        ),
        yaxis2=dict(
            title='Number of Transactions',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_summary_cards(total_revenue, total_transactions, avg_transaction):
    """Create summary statistics cards"""
    return html.Div([
        html.Div([
            html.Div([
                html.H3(f"${total_revenue:,.2f}", style={'margin': '0', 'color': '#1a73e8'}),
                html.P("Total Revenue (30 days)", style={'margin': '0', 'color': 'gray'})
            ], className='card',
                style={'padding': '30px', 'backgroundColor': '#f8f9fa',
                       'borderRadius': '8px', 'textAlign': 'center',
                       'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '1%'}),

        html.Div([
            html.Div([
                html.H3(f"{total_transactions}", style={'margin': '0', 'color': '#1a73e8'}),
                html.P("Total Transactions", style={'margin': '0', 'color': 'gray'})
            ], className='card',
                style={'padding': '30px', 'backgroundColor': '#f8f9fa',
                       'borderRadius': '8px', 'textAlign': 'center',
                       'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '1%'}),

        html.Div([
            html.Div([
                html.H3(f"${avg_transaction:.2f}", style={'margin': '0', 'color': '#1a73e8'}),
                html.P("Average Transaction", style={'margin': '0', 'color': 'gray'})
            ], className='card',
                style={'padding': '30px', 'backgroundColor': '#f8f9fa',
                       'borderRadius': '8px', 'textAlign': 'center',
                       'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '1%'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'})


# Fetch revenue data
try:
    revenue_df = fetch_revenue_data()
    error_message = None
except Exception as e:
    revenue_df = pd.DataFrame()
    error_message = f"Error fetching Stripe revenue data: {str(e)}"

# Calculate metrics for use in layout
if revenue_df.empty:
    total_revenue = 0
    total_transactions = 0
    avg_transaction = 0
else:
    total_revenue = revenue_df['amount'].sum()
    total_transactions = len(revenue_df)
    avg_transaction = revenue_df['amount'].mean()

# Page layout
layout = html.Div([
    html.Div([
        # Page title
        html.H2('Revenue Analytics', style={'textAlign': 'center', 'marginBottom': '30px'}),

        # Error message if any
        html.Div(id='analytics-error', children=[
            html.Div(error_message, style={'color': 'red', 'textAlign': 'center', 'marginBottom': '20px'})
        ] if error_message else []),

        # Summary cards
        create_summary_cards(total_revenue, total_transactions, avg_transaction),

        # Revenue chart
        dcc.Graph(
            id='revenue-chart',
            figure=create_revenue_chart(revenue_df)
        ),

        # Additional insights section
        html.Div([
            html.H3('Key Insights', style={'marginTop': '40px', 'marginBottom': '20px'}),
            html.Div([
                html.P(
                    f"📊 Your busiest day had {revenue_df.groupby('date')['amount'].count().max() if not revenue_df.empty else 0} transactions"),
                html.P(
                    f"💰 Your best revenue day was ${revenue_df.groupby('date')['amount'].sum().max():.2f}" if not revenue_df.empty else "💰 No revenue data yet"),
                html.P(
                    f"📈 You're averaging {total_transactions / 30:.1f} transactions per day" if not revenue_df.empty else "📈 Start accepting payments to see insights")
            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px'})
        ])
    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})
])