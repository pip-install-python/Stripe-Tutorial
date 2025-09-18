# Dash Stripe Integration

A Python web application built with Dash that integrates with Stripe to display products, handle payments, and visualize revenue analytics.

## 🚀 Features

- **Product Catalog**: Display Stripe products with images, descriptions, and pricing
- **Stripe Checkout Integration**: Seamless payment processing with Stripe Checkout
- **Revenue Analytics Dashboard**: Real-time visualization of payment data
- **Multi-page Application**: Clean navigation between products and analytics
- **Responsive Design**: Works on desktop and mobile devices

## 📋 Prerequisites

- Python 3.7+
- A Stripe account (free to create at [stripe.com](https://stripe.com))
- Stripe API keys (found in your Stripe Dashboard under Developers > API Keys)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install dash plotly stripe python-dotenv pandas
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Stripe secret key
   # STRIPE_SECRET_KEY=sk_test_your_actual_key_here
   ```

## 🔑 Stripe Configuration

1. **Get your API keys**
   - Log in to your [Stripe Dashboard](https://dashboard.stripe.com)
   - Navigate to Developers → API Keys
   - Copy your **Secret key** (starts with `sk_test_` for test mode)

2. **Add test products** (optional)
   - Go to Products in your Stripe Dashboard
   - Create some test products with prices
   - The app will automatically fetch and display them

3. **Test the connection**
   ```bash
   python stripe_data/api_connected_test.py
   ```
   You should see "✅ Connection successful!" if everything is set up correctly.

## 🚀 Running the Application

1. **Start the Dash server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Navigate to http://127.0.0.1:2245/
   - You'll see the products page with your Stripe products

## 📁 Project Structure

```
├── app.py                          # Main Dash application
├── pages/
│   ├── home.py                     # Products catalog page
│   ├── create_product.py           # Create new stipe products within application
│   └── analytics.py                # Revenue analytics dashboard
├── stripe_data/
│   └── stripe_analytics_tutorial.py    # Tutorial/demo script for Stripe analytics
├── stripe_data/
│   ├── api_connected_test.py      # Tutorial basic api connection
│   ├── stripe_api_basics.py       # Tutorial more indepth api connection understanding
│   └── STRIPE_CHEATSHEET.md       # Stripe API Cheat Sheet & Tips / Tricks
├── .env.example                   # Example environment variables
├── .env                           # Your actual environment variables (not in git)
├── requirements.txt               # Packages needed for the project
└── README.md                      # This file
```
## 📊 Features in Detail

### Products Page (`/`)
- Displays all active products from your Stripe account
- Shows product images, names, descriptions, and prices
- Supports both one-time and subscription products
- "Buy Now" buttons create Stripe Checkout sessions
- Automatically opens checkout in a new browser tab

### Analytics Page (`/analytics`)
- **Summary Cards**: Total revenue, transaction count, and average transaction value
- **Revenue Chart**: Daily revenue and transaction volume over the last 30 days
- **Key Insights**: Business metrics like busiest days and best revenue days
- **Real-time Data**: Fetches live data from your Stripe account

### Tutorial Script
The `stripe_data/stripe_analytics_tutorial.py` file provides:
- Step-by-step guide to using Stripe's API
- Examples of fetching payment data
- Advanced features like pagination and fee calculations
- Export options for further analysis

## 🧪 Testing

### Test Mode
The application uses Stripe's test mode by default (keys starting with `sk_test_`). This allows you to:
- Create test transactions without real money
- Use [test card numbers](https://stripe.com/docs/testing#cards) like `4242 4242 4242 4242`
- Develop and test without affecting production data

### Creating Test Data
1. Use the products page to make test purchases
2. Use Stripe's test card numbers during checkout
3. View the results immediately in the analytics dashboard

## 🔧 Troubleshooting

### "No API key found" error
- Ensure your `.env` file exists and contains `STRIPE_SECRET_KEY=sk_test_...`
- Check that you're in the correct directory
- Try running `python stripe_api_connected_test.py` to debug

### No products showing
- Verify you have products created in your Stripe Dashboard
- Ensure products have associated prices
- Check that products are active (not archived)

### Analytics showing no data
- The dashboard shows data from the last 30 days only
- Make some test transactions first
- Ensure payments have "succeeded" status

## 📚 Additional Resources

- [Stripe API Documentation](https://stripe.com/docs/api)
- [Dash Documentation](https://dash.plotly.com/)
- [Stripe Checkout Guide](https://stripe.com/docs/checkout)
- [Stripe Testing Guide](https://stripe.com/docs/testing)

## 📝 License

This project is provided as-is for educational and development purposes.

## ⚠️ Security Notes

- **Never commit your actual Stripe secret keys** to version control
- Always use environment variables for sensitive data
- Use test mode keys (`sk_test_`) during development
- Switch to live mode keys (`sk_live_`) only in production with proper security measures

---

Built with ❤️ using [Dash](https://dash.plotly.com/) and [Stripe](https://stripe.com/)