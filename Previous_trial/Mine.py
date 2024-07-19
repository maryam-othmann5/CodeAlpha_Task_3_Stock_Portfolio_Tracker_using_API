import requests
import json

portfolio = {}

def add_stock(symbol, quantity):
    if symbol in portfolio:
        portfolio[symbol] += quantity
    else:
        portfolio[symbol] = quantity

def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
    else:
        print("Stock not found in portfolio.")

def display_portfolio():
    for symbol, quantity in portfolio.items():
        print(f"{symbol}: {quantity} shares")
        try:
            response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=demo')
            data = response.json()
            # Extract the latest closing price
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            latest_close = data['Time Series (Daily)'][last_refreshed]['4. close']
            print(f"Latest close price for {symbol} on {last_refreshed}: ${latest_close}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

def calculate_portfolio_value():
    total_value = 0
    for symbol, quantity in portfolio.items():
        try:
            response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=demo')
            data = response.json()
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            latest_close = float(data['Time Series (Daily)'][last_refreshed]['4. close'])
            stock_value = latest_close * quantity
            total_value += stock_value
        except Exception as e:
            print(f"Error calculating value for {symbol}: {e}")
    print(f"Total portfolio value: ${total_value:.2f}")

while True:
    action = input("Choose an action: [add, remove, display, value, quit]: ")
    if action == 'add':
        symbol = input("Enter the stock symbol: ")
        quantity = int(input(f"Enter the quantity for {symbol}: "))
        add_stock(symbol, quantity)
    elif action == 'remove':
        symbol = input("Enter the stock symbol: ")
        remove_stock(symbol)
    elif action == 'display':
        display_portfolio()
    elif action == 'value':
        calculate_portfolio_value()
    elif action == 'quit':
        break
    else:
        print("Invalid action. Please choose from [add, remove, display, value, quit].")
