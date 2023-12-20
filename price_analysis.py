""" import libraries """
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def download_bitcoin_data(ticker_symbol, start_date, end_date):
    """
    Download historical Bitcoin price data.

    Parameters:
    - ticker_symbol (str): Ticker symbol for Bitcoin (e.g., "BTC-USD").
    - start_date (str): Start date for historical data retrieval (format: "YYYY-MM-DD").
    - end_date (str): End date for historical data retrieval (format: "YYYY-MM-DD").

    Returns:
    - pd.DataFrame: Historical Bitcoin price data.
    """
    btc_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return btc_data


def extract_monthly_prices(data):
    """
    Extract monthly beginning and end-of-the-month prices.

    Parameters:
    - data (pd.DataFrame): Historical Bitcoin price data.

    Returns:
    - pd.DataFrame: Monthly prices (start and end of each month).
    """
    data["YearMonth"] = data.index.to_period("M")
    monthly_prices = (
        data.groupby("YearMonth").agg({"Open": ["first", "last"]}).reset_index()
    )
    monthly_prices["YearMonth"] = pd.to_datetime(
        monthly_prices["YearMonth"].astype(str)
    )
    return monthly_prices


def visualize_bitcoin_prices(monthly_prices):
    """
    Visualize Bitcoin prices using Matplotlib.

    Parameters:
    - monthly_prices (pd.DataFrame): Monthly Bitcoin prices.

    Returns:
    - None
    """
    plt.figure(figsize=(12, 6))

    # Plotting start of the month prices
    plt.plot(
        monthly_prices["YearMonth"],
        monthly_prices["Open"]["first"],
        label="Start of Month",
        marker="o",
    )

    # Plotting end of the month prices
    plt.plot(
        monthly_prices["YearMonth"],
        monthly_prices["Open"]["last"],
        label="End of Month",
        marker="o",
    )

    # Annotating data points with prices
    for i, (start_price, end_price) in enumerate(
        zip(monthly_prices["Open"]["first"], monthly_prices["Open"]["last"])
    ):
        plt.text(
            monthly_prices["YearMonth"][i],
            start_price,
            f"${start_price:.2f}",
            ha="right",
            va="bottom",
            color="blue",
        )
        plt.text(
            monthly_prices["YearMonth"][i],
            end_price,
            f"${end_price:.2f}",
            ha="left",
            va="top",
            color="orange",
        )

    plt.title("Bitcoin Prices - Start and End of Each Month")
    plt.xlabel("Year-Month")
    plt.ylabel("Opening Price (USD)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_and_visualize_bitcoin_prices(ticker_symbol, start_date, end_date):
    """
    Retrieve and visualize historical Bitcoin prices.

    Parameters:
    - ticker_symbol (str): Ticker symbol for Bitcoin (e.g., "BTC-USD").
    - start_date (str): Start date for historical data retrieval (format: "YYYY-MM-DD").
    - end_date (str): End date for historical data retrieval (format: "YYYY-MM-DD").

    Returns:
    - None
    """
    # Download historical data
    btc_data = download_bitcoin_data(ticker_symbol, start_date, end_date)

    # Extract monthly prices
    monthly_prices = extract_monthly_prices(btc_data)

    # Visualize the data
    visualize_bitcoin_prices(monthly_prices)

    print("Monthly Bitcoin prices retrieved and visualized successfully.")


# Run the function to get and visualize data
get_and_visualize_bitcoin_prices("BTC-USD", "2016-01-01", "2023-12-20")
