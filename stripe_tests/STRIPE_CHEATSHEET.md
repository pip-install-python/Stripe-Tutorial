# 🎯 Stripe API Cheat Sheet

## 🔑 Quick Setup
```python
import stripe
stripe.api_key = 'sk_test_...'

# Or use environment variables (recommended)
import os
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
```

## 📦 Products & Prices
```python
# Create Product
product = stripe.Product.create(
    name="Course Name",
    description="Description"
)

# One-time Price
price = stripe.Price.create(
    product=product.id,
    unit_amount=5000,  # $50.00
    currency="usd"
)

# Subscription Price
sub_price = stripe.Price.create(
    product=product.id,
    unit_amount=999,  # $9.99/month
    currency="usd",
    recurring={"interval": "month"}
)
```

## 👥 Customers
```python
# Create Customer
customer = stripe.Customer.create(
    email="user@example.com",
    name="John Doe",
    metadata={"user_id": "123"}
)

# Update Customer
stripe.Customer.modify(
    customer.id,
    metadata={"plan": "premium"}
)

# List Customers
customers = stripe.Customer.list(limit=10)
```

## 💳 Payments
```python
# Payment Intent (for custom flows)
payment_intent = stripe.PaymentIntent.create(
    amount=2000,  # $20.00
    currency="usd",
    customer=customer.id
)

# Checkout Session (hosted page)
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': price.id,
        'quantity': 1
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel'
)
```

## 🔄 Subscriptions
```python
# Create Subscription
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{'price': sub_price.id}]
)

# Cancel Subscription
stripe.Subscription.cancel(subscription.id)

# Update Subscription
stripe.Subscription.modify(
    subscription.id,
    items=[{'price': new_price.id}]
)
```

## 📊 Fetching Data
```python
# List with Pagination
payments = []
has_more = True
starting_after = None

while has_more:
    batch = stripe.PaymentIntent.list(
        limit=100,
        starting_after=starting_after
    )
    payments.extend(batch.data)
    has_more = batch.has_more
    if batch.data:
        starting_after = batch.data[-1].id

# Filter by Date
from datetime import datetime, timedelta
start = int((datetime.now() - timedelta(days=30)).timestamp())

recent_payments = stripe.PaymentIntent.list(
    created={'gte': start}
)
```

## 🪝 Webhooks
```python
# Verify Webhook
import stripe

def handle_webhook(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return 400  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return 400  # Invalid signature
    
    # Handle event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Process successful payment
    
    return 200
```

## ❌ Error Handling
```python
try:
    # Stripe API call
    payment = client.payment_intents.create(...)
except stripe.error.CardError as e:
    # Card was declined
    print(f"Card error: {e.user_message}")
except stripe.error.RateLimitError as e:
    # Too many requests
    print("Rate limit exceeded")
except stripe.error.InvalidRequestError as e:
    # Invalid parameters
    print(f"Invalid request: {str(e)}")
except stripe.error.AuthenticationError as e:
    # Authentication failed
    print("Invalid API key")
except stripe.error.APIConnectionError as e:
    # Network error
    print("Network error")
except stripe.error.StripeError as e:
    # Generic error
    print(f"Stripe error: {str(e)}")
```

## 🧪 Test Cards
```
Success:         4242 4242 4242 4242
Decline:         4000 0000 0000 0002
Insufficient:    4000 0000 0000 9995
Expired:         4000 0000 0000 0069
3D Secure:       4000 0025 0000 3155
```

## 📈 Plotly Quick Charts
```python
import plotly.graph_objs as go
import pandas as pd

# Convert payments to DataFrame
df = pd.DataFrame([{
    'date': payment.created,
    'amount': payment.amount / 100
} for payment in payments])

# Daily Revenue Chart
daily = df.groupby('date')['amount'].sum()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=daily.index,
    y=daily.values,
    name='Daily Revenue'
))
fig.update_layout(title='Revenue Overview')
fig.show()
```

## 🎯 Dash App Skeleton
```python
from dash import Dash, html, dcc, callback
import dash

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Stripe Dashboard'),
    dcc.Graph(id='revenue-chart'),
    dcc.Interval(
        id='interval',
        interval=60000  # Update every minute
    )
])

@callback(
    Output('revenue-chart', 'figure'),
    Input('interval', 'n_intervals')
)
def update_chart(n):
    # Fetch latest data
    # Create figure
    return fig

if __name__ == '__main__':
    app.run(debug=True)
```

## 🔍 Common Patterns
```python
# Amount Conversion
cents_to_dollars = lambda cents: cents / 100
dollars_to_cents = lambda dollars: int(dollars * 100)

# Safe Metadata Access
metadata_value = payment.get('metadata', {}).get('key', 'default')

# Check Payment Status
if payment_intent.status == 'succeeded':
    # Payment successful

# Format Currency
amount_display = f"${amount/100:.2f} {currency.upper()}"
```

## 📝 Remember
- Always use test mode for development
- Never expose secret keys
- Amounts are in cents (multiply by 100)
- Use idempotency keys for critical operations
- Implement webhook signature verification
- Handle all possible error types
- Use metadata to link Stripe to your database