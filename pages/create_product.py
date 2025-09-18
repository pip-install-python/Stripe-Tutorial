import stripe
from dash import html, dcc, Input, Output, State, callback, register_page
from dash.exceptions import PreventUpdate
import dash

# Register this page
register_page(__name__, path='/create-products', name='Create Products')

# Import stripe from main
import __main__

stripe = __main__.stripe

# Page layout
layout = html.Div([
    html.Div([
        # Page title
        html.H2('Create New Product', style={'textAlign': 'center', 'marginBottom': '30px'}),

        # Success/Error messages
        html.Div(id='create-message', style={'marginBottom': '20px'}),

        # Product creation form
        html.Div([
            # Product Information Section
            html.Div([
                html.H3('Product Information', style={'marginBottom': '20px', 'color': '#1a73e8'}),

                # Product Name
                html.Div([
                    html.Label('Product Name *', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Input(
                        id='product-name',
                        type='text',
                        placeholder='e.g., Premium Subscription',
                        style={'width': '100%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd'},
                        required=True
                    ),
                ], style={'marginBottom': '20px'}),

                # Product Description
                html.Div([
                    html.Label('Description', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Textarea(
                        id='product-description',
                        placeholder='Describe your product...',
                        style={'width': '100%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd', 'minHeight': '100px'},
                    ),
                ], style={'marginBottom': '20px'}),

                # Product Image URL
                html.Div([
                    html.Label('Image URL (optional)', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Input(
                        id='product-image',
                        type='url',
                        placeholder='https://example.com/image.jpg',
                        style={'width': '100%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd'},
                    ),
                ], style={'marginBottom': '20px'}),

            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '30px'}),

            # Pricing Information Section
            html.Div([
                html.H3('Pricing Information', style={'marginBottom': '20px', 'color': '#1a73e8'}),

                # Price Type
                html.Div([
                    html.Label('Price Type *', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.RadioItems(
                        id='price-type',
                        options=[
                            {'label': ' One-time Payment', 'value': 'one_time'},
                            {'label': ' Recurring Subscription', 'value': 'recurring'}
                        ],
                        value='one_time',
                        style={'marginBottom': '10px'},
                        labelStyle={'display': 'block', 'marginBottom': '10px', 'cursor': 'pointer'}
                    ),
                ], style={'marginBottom': '20px'}),

                # Recurring Interval (shown only for subscriptions)
                html.Div([
                    html.Label('Billing Interval', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Dropdown(
                        id='recurring-interval',
                        options=[
                            {'label': 'Daily', 'value': 'day'},
                            {'label': 'Weekly', 'value': 'week'},
                            {'label': 'Monthly', 'value': 'month'},
                            {'label': 'Yearly', 'value': 'year'}
                        ],
                        value='month',
                        style={'width': '100%'}
                    ),
                ], id='interval-div', style={'marginBottom': '20px', 'display': 'none'}),

                # Price Amount
                html.Div([
                    html.Label('Price Amount *', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    html.Div([
                        html.Span('$', style={'fontSize': '20px', 'marginRight': '5px', 'color': '#666'}),
                        dcc.Input(
                            id='price-amount',
                            type='number',
                            placeholder='0.00',
                            min=0.50,
                            step=0.01,
                            style={'width': '150px', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                                   'border': '1px solid #ddd'},
                            required=True
                        ),
                        dcc.Dropdown(
                            id='currency',
                            options=[
                                {'label': 'USD', 'value': 'usd'},
                                {'label': 'EUR', 'value': 'eur'},
                                {'label': 'GBP', 'value': 'gbp'},
                                {'label': 'CAD', 'value': 'cad'},
                                {'label': 'AUD', 'value': 'aud'}
                            ],
                            value='usd',
                            style={'width': '100px', 'display': 'inline-block', 'marginLeft': '10px'}
                        ),
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    html.Small('Minimum: $0.50 or equivalent',
                               style={'color': '#666', 'marginTop': '5px', 'display': 'block'}),
                ], style={'marginBottom': '20px'}),

                # Price Nickname (optional)
                html.Div([
                    html.Label('Price Nickname (optional)', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Input(
                        id='price-nickname',
                        type='text',
                        placeholder='e.g., Standard Plan',
                        style={'width': '100%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd'},
                    ),
                ], style={'marginBottom': '20px'}),

            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '30px'}),

            # Metadata Section (optional)
            html.Div([
                html.H3('Additional Information (Optional)', style={'marginBottom': '20px', 'color': '#1a73e8'}),

                html.Div([
                    html.Label('Metadata Key', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Input(
                        id='metadata-key',
                        type='text',
                        placeholder='e.g., category',
                        style={'width': '45%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd', 'marginRight': '10px'},
                    ),
                    html.Label('Metadata Value',
                               style={'fontWeight': 'bold', 'marginBottom': '5px', 'marginLeft': '10px'}),
                    dcc.Input(
                        id='metadata-value',
                        type='text',
                        placeholder='e.g., software',
                        style={'width': '45%', 'padding': '10px', 'fontSize': '16px', 'borderRadius': '5px',
                               'border': '1px solid #ddd'},
                    ),
                ], style={'marginBottom': '20px'}),

            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '30px'}),

            # Submit Button
            html.Div([
                html.Button(
                    'Create Product',
                    id='create-product-button',
                    n_clicks=0,
                    style={
                        'backgroundColor': '#1a73e8',
                        'color': 'white',
                        'padding': '12px 40px',
                        'fontSize': '18px',
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'width': '100%',
                        'fontWeight': 'bold',
                        'transition': 'background-color 0.3s'
                    }
                ),
            ], style={'textAlign': 'center'}),

        ], style={'maxWidth': '600px', 'margin': '0 auto'}),

        # Recently Created Products Section
        html.Hr(style={'margin': '50px 0'}),

        html.Div([
            html.H3('Recently Created Products', style={'marginBottom': '20px', 'textAlign': 'center'}),
            html.Div(id='recent-products', style={'marginTop': '20px'}),
        ]),

    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})
])


# Callback to show/hide recurring interval based on price type
@callback(
    Output('interval-div', 'style'),
    Input('price-type', 'value')
)
def toggle_interval_display(price_type):
    if price_type == 'recurring':
        return {'marginBottom': '20px', 'display': 'block'}
    return {'marginBottom': '20px', 'display': 'none'}


# Callback to handle product creation
@callback(
    [Output('create-message', 'children'),
     Output('recent-products', 'children'),
     Output('product-name', 'value'),
     Output('product-description', 'value'),
     Output('product-image', 'value'),
     Output('price-amount', 'value'),
     Output('price-nickname', 'value'),
     Output('metadata-key', 'value'),
     Output('metadata-value', 'value')],
    [Input('create-product-button', 'n_clicks')],
    [State('product-name', 'value'),
     State('product-description', 'value'),
     State('product-image', 'value'),
     State('price-type', 'value'),
     State('recurring-interval', 'value'),
     State('price-amount', 'value'),
     State('currency', 'value'),
     State('price-nickname', 'value'),
     State('metadata-key', 'value'),
     State('metadata-value', 'value')],
    prevent_initial_call=True
)
def create_product(n_clicks, name, description, image, price_type, interval, amount, currency, nickname, meta_key,
                   meta_value):
    if n_clicks == 0:
        raise PreventUpdate

    # Validate required fields
    if not name or not amount:
        error_msg = html.Div([
            html.Div('❌ Error: Product name and price amount are required.',
                     style={'color': 'red', 'padding': '10px', 'backgroundColor': '#fee', 'borderRadius': '5px'})
        ])
        return error_msg, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        # Convert amount to cents
        amount_cents = int(float(amount) * 100)

        # Prepare product data
        product_data = {
            'name': name
        }

        if description:
            product_data['description'] = description

        if image:
            product_data['images'] = [image]

        # Add metadata if provided
        if meta_key and meta_value:
            product_data['metadata'] = {meta_key: meta_value}

        # Create product in Stripe
        product = stripe.Product.create(**product_data)

        # Prepare price data
        price_data = {
            'product': product.id,
            'unit_amount': amount_cents,
            'currency': currency
        }

        if nickname:
            price_data['nickname'] = nickname

        # Add recurring information if subscription
        if price_type == 'recurring':
            price_data['recurring'] = {'interval': interval}

        # Create price in Stripe
        price = stripe.Price.create(**price_data)

        # Success message
        success_msg = html.Div([
            html.Div([
                html.H4('✅ Product Created Successfully!', style={'margin': '0 0 10px 0'}),
                html.P(f'Product ID: {product.id}', style={'margin': '5px 0'}),
                html.P(f'Product Name: {product.name}', style={'margin': '5px 0'}),
                html.P(f'Price ID: {price.id}', style={'margin': '5px 0'}),
                html.P(
                    f'Price: ${amount} {currency.upper()}' + (f' per {interval}' if price_type == 'recurring' else ''),
                    style={'margin': '5px 0', 'fontWeight': 'bold'}),
            ], style={'color': 'green', 'padding': '15px', 'backgroundColor': '#efe', 'borderRadius': '5px'})
        ])

        # Fetch and display recent products
        recent_products = fetch_recent_products()

        # Clear form fields
        return success_msg, recent_products, '', '', '', '', '', '', ''

    except stripe.error.StripeError as e:
        error_msg = html.Div([
            html.Div(f'❌ Stripe Error: {str(e)}',
                     style={'color': 'red', 'padding': '10px', 'backgroundColor': '#fee', 'borderRadius': '5px'})
        ])
        return error_msg, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    except Exception as e:
        error_msg = html.Div([
            html.Div(f'❌ Error: {str(e)}',
                     style={'color': 'red', 'padding': '10px', 'backgroundColor': '#fee', 'borderRadius': '5px'})
        ])
        return error_msg, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


def fetch_recent_products():
    """Fetch and display recently created products"""
    try:
        # Fetch recent products
        products = stripe.Product.list(limit=5)

        if not products.data:
            return html.P("No products found.", style={'textAlign': 'center', 'color': '#666'})

        # Create product cards
        cards = []
        for product in products.data:
            # Get the first price for this product
            prices = stripe.Price.list(product=product.id, limit=1)
            price_info = "No price set"

            if prices.data:
                price = prices.data[0]
                amount = price.unit_amount / 100 if price.unit_amount else 0
                currency = price.currency.upper()

                if price.recurring:
                    interval = price.recurring.interval
                    price_info = f"${amount:.2f} {currency} per {interval}"
                else:
                    price_info = f"${amount:.2f} {currency}"

            card = html.Div([
                html.Div([
                    html.H4(product.name, style={'margin': '0 0 10px 0'}),
                    html.P(product.description or "No description",
                           style={'color': '#666', 'margin': '0 0 10px 0', 'fontSize': '14px'}),
                    html.P(price_info, style={'fontWeight': 'bold', 'color': '#1a73e8', 'margin': '0'}),
                    html.Small(f'ID: {product.id}', style={'color': '#999'}),
                ], style={'padding': '15px'})
            ], style={
                'backgroundColor': 'white',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'marginBottom': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            })

            cards.append(card)

        return html.Div(cards)

    except Exception as e:
        return html.P(f"Error fetching products: {str(e)}", style={'color': 'red'})


# Initial load of recent products
@callback(
    Output('recent-products', 'children', allow_duplicate=True),
    Input('create-product-button', 'n_clicks'),
    prevent_initial_call=True
)
def load_recent_products(n_clicks):
    if n_clicks == 0:
        return fetch_recent_products()
    raise PreventUpdate