import stripe
import pandas as pd
from dash import html, Input, Output, callback, register_page, callback_context, dependencies
from dash.exceptions import PreventUpdate
import webbrowser

# Register this page
register_page(__name__, path='/', name='Products')

# Import stripe from main
import __main__

stripe = __main__.stripe

def fetch_products_data():
    """Fetch products data from Stripe"""
    products_data = []
    products = stripe.Product.list(limit=100)

    for product in products.data:
        # Get prices for each product
        prices = stripe.Price.list(product=product.id, limit=10)

        for price in prices.data:
            products_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'description': product.description or 'No description',
                'price_id': price.id,
                'unit_amount': price.unit_amount / 100 if price.unit_amount else 0,
                'currency': price.currency.upper(),
                'recurring': 'Yes' if price.recurring else 'No',
                'image': product.images[0] if product.images else None
            })

    return pd.DataFrame(products_data) if products_data else pd.DataFrame()


def create_product_cards(products_df):
    """Create product cards with images and buy buttons"""
    if products_df.empty:
        return html.P("No products found in your Stripe account.",
                      style={'textAlign': 'center', 'color': 'gray', 'marginTop': '50px'})

    cards = []
    for idx, product in products_df.iterrows():
        card = html.Div([
            # Product image
            html.Div([
                html.Img(
                    src=product['image'] if product['image'] else 'https://via.placeholder.com/300x200?text=No+Image',
                    style={'width': '100%', 'height': '200px', 'objectFit': 'cover',
                           'borderRadius': '5px 5px 0 0'}
                )
            ]),

            # Product details
            html.Div([
                html.H3(product['product_name'], style={'margin': '10px 0'}),
                html.P(product['description'],
                       style={'color': 'gray', 'minHeight': '60px', 'fontSize': '14px'}),

                # Price and currency
                html.Div([
                    html.H4(f"${product['unit_amount']:.2f} {product['currency']}",
                            style={'color': '#1a73e8', 'margin': '15px 0'}),
                    html.P(f"{'Subscription' if product['recurring'] == 'Yes' else 'One-time payment'}",
                           style={'fontSize': '12px', 'color': 'gray'})
                ]),

                # Buy button
                html.Button(
                    'Buy Now',
                    id={'type': 'buy-button', 'index': idx},
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'backgroundColor': '#1a73e8',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '16px',
                        'marginTop': '10px',
                        'transition': 'background-color 0.3s'
                    },
                    **{'data-price-id': product['price_id']}
                )
            ], style={'padding': '20px'})
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '5px',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
            'margin': '10px',
            'width': '300px',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'transition': 'transform 0.2s, box-shadow 0.2s'
        })

        cards.append(card)

    return html.Div(cards, style={'textAlign': 'center'})


# Fetch products data
try:
    products_df = fetch_products_data()
    error_message = None
except Exception as e:
    products_df = pd.DataFrame()
    error_message = f"Error fetching Stripe products: {str(e)}"

# Page layout
layout = html.Div([
    html.Div([
        # Page title
        html.H2('Available Products', style={'textAlign': 'center', 'marginBottom': '30px'}),

        # Error message if any
        html.Div(id='error-message', children=[
            html.Div(error_message, style={'color': 'red', 'textAlign': 'center', 'marginBottom': '20px'})
        ] if error_message else []),

        # Hidden div to store checkout URL
        html.Div(id='checkout-url', style={'display': 'none'}),

        # Product cards
        html.Div(id='products-container', children=[
            create_product_cards(products_df)
        ])
    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})
])


# Callback to handle buy button clicks
@callback(
    Output('checkout-url', 'children'),
    [Input({'type': 'buy-button', 'index': dependencies.ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def handle_buy_button(n_clicks):
    """Handle buy button clicks and create Stripe checkout session"""

    # Check which button was clicked
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Check if any button was actually clicked
    if all(click == 0 for click in n_clicks):
        raise PreventUpdate

    # Find which button was clicked by comparing n_clicks
    clicked_index = None
    for i, clicks in enumerate(n_clicks):
        if clicks > 0:
            clicked_index = i
            break

    if clicked_index is None:
        raise PreventUpdate

    # Get the price_id from the products dataframe
    try:
        price_id = products_df.iloc[clicked_index]['price_id']

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription' if products_df.iloc[clicked_index]['recurring'] == 'Yes' else 'payment',
            success_url='http://127.0.0.1:2245/?success=true',
            cancel_url='http://127.0.0.1:2245/?canceled=true',
        )

        # Open the checkout URL in a new browser tab
        webbrowser.open_new_tab(session.url)

        return session.url

    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        raise PreventUpdate