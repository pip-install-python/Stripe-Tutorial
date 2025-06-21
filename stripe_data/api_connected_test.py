import os
import stripe
from dotenv import load_dotenv
load_dotenv()
# Test script to verify Stripe setup
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

print(f"Environment variable STRIPE_SECRET_KEY: {stripe.api_key}")

if not stripe.api_key:
    print("\n❌ STRIPE_SECRET_KEY not found!")
    print("\nTo set it:")
    print("1. In terminal before running:")
    print("   export STRIPE_SECRET_KEY='sk_test_your_key_here'")
    print("\n2. In PyCharm:")
    print("   Run → Edit Configurations → Environment variables")
    print("   Add: STRIPE_SECRET_KEY=sk_test_your_key_here")
    print("\n3. In VS Code:")
    print("   Create .env file with: STRIPE_SECRET_KEY=sk_test_your_key_here")
else:
    print("✅ Stripe API key found!")
    try:
        # Test the connection
        products = stripe.Product.list(limit=1)
        print(f"✅ Connection successful! Found {len(products.data)} product(s)")
    except Exception as e:
        print(f"❌ Connection failed: {e}")