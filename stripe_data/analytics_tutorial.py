#!/usr/bin/env python3
"""
Stripe Payment Analytics Tutorial
=================================
This tutorial demonstrates how to fetch and analyze payment data from Stripe.
We'll explore how to:
1. Connect to Stripe API
2. Fetch payment intents
3. Process and analyze transaction data
4. Calculate key metrics
"""

import os
import stripe
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# ===== STEP 1: Initialize Stripe =====
# Set your Stripe secret key from environment variables
# You can find this in your Stripe Dashboard under Developers > API Keys
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

print("🔑 Stripe API initialized")
print(f"   Using API key: {stripe.api_key[:8]}..." if stripe.api_key else "   ⚠️  No API key found!")
print("\n" + "=" * 50 + "\n")


def fetch_payment_data():
    """
    Fetch payment data from Stripe for the last 30 days.

    Stripe's PaymentIntent represents a payment from a customer.
    Each PaymentIntent has various states, but we're interested in 'succeeded' ones.
    """
    print("📊 FETCHING PAYMENT DATA FROM STRIPE")
    print("-" * 35)

    # Calculate timestamp for 30 days ago
    # Stripe uses Unix timestamps (seconds since epoch)
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

    print(f"📅 Date range: {datetime.fromtimestamp(thirty_days_ago).date()} to {datetime.now().date()}")
    print(f"   Unix timestamp 30 days ago: {thirty_days_ago}")

    # Initialize list to store payment data
    revenue_data = []

    try:
        # Fetch payment intents from Stripe
        # limit=100 is the maximum per request
        # created={'gte': thirty_days_ago} filters for payments after this timestamp
        print("\n🔄 Calling Stripe API: stripe.PaymentIntent.list()")
        payments = stripe.PaymentIntent.list(
            limit=100,
            created={'gte': thirty_days_ago}
        )

        print(f"✅ Found {len(payments.data)} payment intents")

        # Process each payment
        succeeded_count = 0
        for i, payment in enumerate(payments.data):
            # Show first 3 payments as examples
            if i < 3:
                print(f"\n   Payment {i + 1}:")
                print(f"   - ID: {payment.id}")
                print(f"   - Status: {payment.status}")
                print(f"   - Amount: ${payment.amount / 100:.2f} {payment.currency.upper()}")
                print(f"   - Created: {datetime.fromtimestamp(payment.created)}")

            # Only process successful payments
            if payment.status == 'succeeded':
                succeeded_count += 1
                revenue_data.append({
                    'payment_id': payment.id,
                    'date': datetime.fromtimestamp(payment.created).date(),
                    'datetime': datetime.fromtimestamp(payment.created),
                    'amount': payment.amount / 100,  # Convert cents to dollars
                    'currency': payment.currency.upper(),
                    'description': payment.description or 'Payment',
                    'customer': payment.customer,  # Customer ID if available
                    'metadata': dict(payment.metadata) if payment.metadata else {}
                })

        if len(payments.data) > 3:
            print(f"\n   ... and {len(payments.data) - 3} more payments")

        print(f"\n📈 Summary: {succeeded_count} successful payments out of {len(payments.data)} total")

    except stripe.error.StripeError as e:
        print(f"\n❌ Stripe API Error: {e}")
        return pd.DataFrame()

    # Convert to pandas DataFrame for easier analysis
    df = pd.DataFrame(revenue_data) if revenue_data else pd.DataFrame()

    return df


def analyze_revenue_data(df):
    """
    Analyze the revenue data and calculate key metrics.
    This demonstrates various ways to process Stripe payment data.
    """
    print("\n\n💰 ANALYZING REVENUE DATA")
    print("-" * 25)

    if df.empty:
        print("⚠️  No payment data to analyze")
        return

    # Basic metrics
    total_revenue = df['amount'].sum()
    total_transactions = len(df)
    avg_transaction = df['amount'].mean()

    print(f"\n📊 Basic Metrics (Last 30 Days):")
    print(f"   💵 Total Revenue: ${total_revenue:,.2f}")
    print(f"   📦 Total Transactions: {total_transactions}")
    print(f"   💳 Average Transaction: ${avg_transaction:.2f}")

    # Currency breakdown
    print(f"\n💱 Currency Breakdown:")
    currency_totals = df.groupby('currency')['amount'].agg(['sum', 'count'])
    for currency, row in currency_totals.iterrows():
        print(f"   {currency}: ${row['sum']:,.2f} ({int(row['count'])} transactions)")

    # Daily revenue analysis
    print(f"\n📅 Daily Revenue Analysis:")
    daily_revenue = df.groupby('date').agg({
        'amount': ['sum', 'count', 'mean']
    })
    daily_revenue.columns = ['revenue', 'transactions', 'avg_transaction']

    # Find best and worst days
    best_day = daily_revenue['revenue'].idxmax()
    worst_day = daily_revenue['revenue'].idxmin()

    print(f"   📈 Best day: {best_day} - ${daily_revenue.loc[best_day, 'revenue']:,.2f}")
    print(f"   📉 Worst day: {worst_day} - ${daily_revenue.loc[worst_day, 'revenue']:,.2f}")
    print(f"   📊 Average daily revenue: ${daily_revenue['revenue'].mean():,.2f}")

    # Show daily breakdown for last 7 days
    print(f"\n📋 Last 7 Days Detail:")
    last_7_days = daily_revenue.sort_index(ascending=False).head(7)
    for date, row in last_7_days.iterrows():
        print(f"   {date}: ${row['revenue']:,.2f} ({int(row['transactions'])} transactions)")

    # Hour of day analysis
    print(f"\n⏰ Transaction Timing Analysis:")
    df['hour'] = pd.to_datetime(df['datetime']).dt.hour
    hourly_transactions = df.groupby('hour').size()
    peak_hour = hourly_transactions.idxmax()
    print(f"   🕐 Peak transaction hour: {peak_hour}:00 ({hourly_transactions[peak_hour]} transactions)")

    # Customer analysis (if customer IDs are available)
    if 'customer' in df.columns and df['customer'].notna().any():
        print(f"\n👥 Customer Analysis:")
        unique_customers = df['customer'].nunique()
        repeat_customers = df[df['customer'].notna()]['customer'].value_counts()
        repeat_count = (repeat_customers > 1).sum()

        print(f"   👤 Unique customers: {unique_customers}")
        print(f"   🔄 Repeat customers: {repeat_count}")
        if len(repeat_customers) > 0:
            print(f"   🌟 Top customer: {repeat_customers.index[0]} ({repeat_customers.iloc[0]} transactions)")


def advanced_stripe_features():
    """
    Demonstrate additional Stripe features for payment analytics.
    """
    print("\n\n🚀 ADVANCED STRIPE FEATURES")
    print("-" * 27)

    # Demonstrate pagination for large datasets
    print("\n📄 Pagination Example:")
    print("   When you have more than 100 payments, use pagination:")
    print("   ```python")
    print("   all_payments = []")
    print("   has_more = True")
    print("   starting_after = None")
    print("   ")
    print("   while has_more:")
    print("       payments = stripe.PaymentIntent.list(")
    print("           limit=100,")
    print("           starting_after=starting_after")
    print("       )")
    print("       all_payments.extend(payments.data)")
    print("       has_more = payments.has_more")
    print("       if payments.data:")
    print("           starting_after = payments.data[-1].id")
    print("   ```")

    # Show how to fetch additional payment details
    print("\n🔍 Fetching Detailed Payment Information:")
    print("   You can retrieve additional details for specific payments:")
    print("   ```python")
    print("   payment = stripe.PaymentIntent.retrieve('pi_xxxxx')")
    print("   charges = payment.charges.data  # Get charge details")
    print("   if charges:")
    print("       charge = charges[0]")
    print("       print(f'Card brand: {charge.payment_method_details.card.brand}')")
    print("       print(f'Last 4: {charge.payment_method_details.card.last4}')")
    print("   ```")

    # Demonstrate balance transactions for fees
    print("\n💸 Calculating Net Revenue (after Stripe fees):")
    print("   Use BalanceTransaction to get fee information:")
    print("   ```python")
    print("   balance_txn = stripe.BalanceTransaction.retrieve(charge.balance_transaction)")
    print("   fee = balance_txn.fee / 100  # Convert to dollars")
    print("   net = balance_txn.net / 100  # Net amount after fees")
    print("   ```")


def export_analytics_data(df):
    """
    Show how to export data for further analysis.
    """
    print("\n\n💾 EXPORTING DATA")
    print("-" * 17)

    if not df.empty:
        # Create a summary report
        summary = {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'total_revenue': f"${df['amount'].sum():,.2f}",
            'total_transactions': len(df),
            'average_transaction': f"${df['amount'].mean():.2f}",
            'currencies': df['currency'].unique().tolist()
        }

        print("\n📊 Summary Report:")
        for key, value in summary.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

        print("\n💡 Export Options:")
        print("   1. CSV: df.to_csv('stripe_payments.csv', index=False)")
        print("   2. Excel: df.to_excel('stripe_payments.xlsx', index=False)")
        print("   3. JSON: df.to_json('stripe_payments.json', orient='records')")


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("\n🎯 STRIPE PAYMENT ANALYTICS TUTORIAL")
    print("=" * 36)
    print("This tutorial demonstrates how to fetch and analyze")
    print("payment data using the Stripe API.\n")

    # Fetch payment data
    payment_df = fetch_payment_data()

    # Analyze the data
    analyze_revenue_data(payment_df)

    # Show advanced features
    advanced_stripe_features()

    # Export options
    export_analytics_data(payment_df)

    print("\n\n✅ Tutorial Complete!")
    print("=" * 20)
    print("Next steps:")
    print("1. Explore Stripe's reporting API for pre-built reports")
    print("2. Set up webhooks to track payments in real-time")
    print("3. Use Stripe Sigma for SQL-based analytics")
    print("4. Implement customer lifetime value calculations")
    print("\nFor more info: https://stripe.com/docs/api/payment_intents")