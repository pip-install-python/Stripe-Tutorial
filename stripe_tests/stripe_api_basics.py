#!/usr/bin/env python3
"""
Test Stripe Connection
======================
Simple script to verify your Stripe API connection is working.
Run this before starting the tutorials!
"""

import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing Stripe API Connection...")
print("=" * 50)

# Check if API key exists
api_key = os.environ.get('STRIPE_SECRET_KEY')
if not api_key:
    print("❌ ERROR: No STRIPE_SECRET_KEY found in environment variables!")
    print("\nPlease create a .env file with:")
    print("STRIPE_SECRET_KEY=sk_test_your_key_here")
    exit(1)

# Check if it's a test key
if api_key.startswith('sk_test_'):
    print("✅ Using TEST mode API key (safe for development)")
elif api_key.startswith('sk_live_'):
    print("⚠️  WARNING: Using LIVE mode API key!")
    print("   Be careful - this will create real charges!")
else:
    print("❌ Invalid API key format")
    exit(1)

# Set the API key
stripe.api_key = api_key

# Test the connection
try:
    # Try to retrieve account information
    account = stripe.Account.retrieve()

    print("\n✅ Successfully connected to Stripe!")
    print(f"   Account Email: {account.email}")
    print(f"   Account ID: {account.id}")
    print(f"   Country: {account.country}")
    print(f"   Default Currency: {account.default_currency}")

    # Test listing products
    print("\n📦 Testing Product API...")
    products = stripe.Product.list(limit=3)
    print(f"   Found {len(products.data)} products")

    if products.data:
        print("   Products:")
        for product in products.data:
            print(f"   - {product.name} ({product.id})")
    else:
        print("   No products found. Create some in your Stripe Dashboard!")

    # Test listing customers
    print("\n👥 Testing Customer API...")
    customers = stripe.Customer.list(limit=3)
    print(f"   Found {len(customers.data)} customers")

    # Test listing recent payments
    print("\n💳 Testing Payment Intent API...")
    payments = stripe.PaymentIntent.list(limit=3)
    print(f"   Found {len(payments.data)} recent payment intents")

    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your Stripe connection is working.")
    print("You're ready to run the tutorials!")

except stripe.error.AuthenticationError as e:
    print(f"\n❌ Authentication Error: {e.user_message}")
    print("   Please check your API key is correct")
except stripe.error.APIConnectionError as e:
    print(f"\n❌ Network Error: {str(e)}")
    print("   Please check your internet connection")
except Exception as e:
    print(f"\n❌ Unexpected Error: {str(e)}")
    print("   Please check the Stripe documentation")

print("\n" + "=" * 50)