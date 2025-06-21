import os
import stripe
from dash import Dash, html, dcc, page_container
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Make stripe available to pages
import __main__

__main__.stripe = stripe

# Initialize Dash app with pages
app = Dash(__name__, use_pages=True, pages_folder='pages')

# Store for checkout sessions
app.server.config['CHECKOUT_SESSIONS'] = {}

# Main layout with navigation
app.layout = html.Div([
    html.Div([
        # Header with navigation
        html.Div([
            html.H1('Dash Stripe Integration',
                    style={'display': 'inline-block', 'margin': '0'}),

            # Navigation links
            html.Div([
                dcc.Link('Products', href='/',
                         style={'marginRight': '20px', 'textDecoration': 'none',
                                'color': '#1a73e8', 'fontSize': '18px'}),
                dcc.Link('Analytics', href='/analytics',
                         style={'textDecoration': 'none', 'color': '#1a73e8',
                                'fontSize': '18px'})
            ], style={'display': 'inline-block', 'float': 'right', 'marginTop': '10px'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px',
                  'marginBottom': '20px', 'borderBottom': '2px solid #e0e0e0'}),

        # Page content
        page_container
    ])
])

if __name__ == '__main__':
    print("Starting Stripe Revenue Dashboard...")
    print("Open http://127.0.0.1:2245/ in your browser")
    app.run(debug=True, port=2245)