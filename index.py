import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression

def get_company_financials(ticker):
    try:
        # Fetch financial data
        stock = yf.Ticker(ticker)
        financials = stock.financials.T  # Transpose to get the correct format for accessing years
        quarterly_financials = stock.quarterly_financials.T
        quarterly_balance_sheet = stock.quarterly_balance_sheet.T
        quarterly_cash_flow = stock.quarterly_cashflow.T
        balance_sheet = stock.balance_sheet.T
        cash_flow = stock.cashflow.T

        # Get the years for the financial data
        years = [date.year for date in financials.index[:4]]

        # Get revenue, gross profit, operating profit, and net income for the past 4 years
        revenues = financials.get('Total Revenue', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()
        gross_profits = financials.get('Gross Profit', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()
        operating_profits = financials.get('Operating Income', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()
        net_incomes = financials.get('Net Income', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()

        # Fetch TTM (Trailing Twelve Months) values
        ttm_revenue = quarterly_financials.get('Total Revenue', pd.Series([0]*4)).iloc[:4].sum() / 1e9
        ttm_gross_profit = quarterly_financials.get('Gross Profit', pd.Series([0]*4)).iloc[:4].sum() / 1e9
        ttm_operating_profit = quarterly_financials.get('Operating Income', pd.Series([0]*4)).iloc[:4].sum() / 1e9
        ttm_net_income = quarterly_financials.get('Net Income', pd.Series([0]*4)).iloc[:4].sum() / 1e9

        # Get MRQ (Most Recent Quarter) values for balance sheet metrics
        mrq_assets = quarterly_balance_sheet.get('Total Assets', pd.Series([0])).iloc[0] / 1e9
        mrq_liabilities = quarterly_balance_sheet.get('Total Liabilities Net Minority Interest', pd.Series([0])).iloc[0] / 1e9
        mrq_equity = quarterly_balance_sheet.get('Total Equity Gross Minority Interest', pd.Series([0])).iloc[0] / 1e9

        # Get MRQ (Most Recent Quarter) value for free cash flow
        mrq_free_cash_flow = quarterly_cash_flow.get('Free Cash Flow', pd.Series([0])).iloc[0] / 1e9

        # Get balance sheet metrics for the past 4 years
        assets = balance_sheet.get('Total Assets', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()
        liabilities = balance_sheet.get('Total Liabilities Net Minority Interest', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()
        equity = balance_sheet.get('Total Equity Gross Minority Interest', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()

        # Get free cash flow for the past 4 years
        free_cash_flows = cash_flow.get('Free Cash Flow', pd.Series([0]*4)).iloc[:4].div(1e9).round(2).tolist()

        # Reverse the lists to ensure the order is from oldest to newest
        revenues.reverse()
        gross_profits.reverse()
        operating_profits.reverse()
        net_incomes.reverse()
        assets.reverse()
        liabilities.reverse()
        equity.reverse()
        free_cash_flows.reverse()

        # Add MRQ/TTM values to the lists (which should be the most recent data point)
        revenues.append(ttm_revenue)
        gross_profits.append(ttm_gross_profit)
        operating_profits.append(ttm_operating_profit)
        net_incomes.append(ttm_net_income)
        assets.append(mrq_assets)
        liabilities.append(mrq_liabilities)
        equity.append(mrq_equity)
        free_cash_flows.append(mrq_free_cash_flow)

        # Prepare linear regression model
        model = LinearRegression()

        # Create time points for the metrics (0, 1, 2, 3, 4)
        X = np.array(range(5)).reshape(-1, 1)

        # Calculate slopes for each metric using linear regression
        def calculate_slope(values):
            y = np.array(values).reshape(-1, 1)
            model.fit(X, y)
            return model.coef_[0][0]

        revenue_slope = calculate_slope(revenues)
        gross_profit_slope = calculate_slope(gross_profits)
        operating_profit_slope = calculate_slope(operating_profits)
        net_income_slope = calculate_slope(net_incomes)
        assets_slope = calculate_slope(assets)
        liabilities_slope = calculate_slope(liabilities)
        equity_slope = calculate_slope(equity)
        free_cash_flow_slope = calculate_slope(free_cash_flows)

        # Format slopes
        def format_slope(slope):
            direction = "Positive" if slope > 0 else "Negative"
            return f"{direction} ({slope:.2f}x)"

        # Prepare formatted output for proper alignment
        print(f"{ticker}\n")
        print(f"{'Metric':<20}{years[0]:>10}{years[1]:>10}{years[2]:>10}{years[3]:>10}{'MRQ/TTM':>10}{'Slope':>20}")
        print(f"{'Revenue':<20}{revenues[0]:>10.2f}{revenues[1]:>10.2f}{revenues[2]:>10.2f}{revenues[3]:>10.2f}{revenues[4]:>10.2f}{format_slope(revenue_slope):>20}")
        print(f"{'Gross Profit':<20}{gross_profits[0]:>10.2f}{gross_profits[1]:>10.2f}{gross_profits[2]:>10.2f}{gross_profits[3]:>10.2f}{gross_profits[4]:>10.2f}{format_slope(gross_profit_slope):>20}")
        print(f"{'Operating Profit':<20}{operating_profits[0]:>10.2f}{operating_profits[1]:>10.2f}{operating_profits[2]:>10.2f}{operating_profits[3]:>10.2f}{operating_profits[4]:>10.2f}{format_slope(operating_profit_slope):>20}")
        print(f"{'Net Income':<20}{net_incomes[0]:>10.2f}{net_incomes[1]:>10.2f}{net_incomes[2]:>10.2f}{net_incomes[3]:>10.2f}{net_incomes[4]:>10.2f}{format_slope(net_income_slope):>20}")
        print(f"{'Total Assets':<20}{assets[0]:>10.2f}{assets[1]:>10.2f}{assets[2]:>10.2f}{assets[3]:>10.2f}{assets[4]:>10.2f}{format_slope(assets_slope):>20}")
        print(f"{'Total Liabilities':<20}{liabilities[0]:>10.2f}{liabilities[1]:>10.2f}{liabilities[2]:>10.2f}{liabilities[3]:>10.2f}{liabilities[4]:>10.2f}{format_slope(liabilities_slope):>20}")
        print(f"{'Total Equity':<20}{equity[0]:>10.2f}{equity[1]:>10.2f}{equity[2]:>10.2f}{equity[3]:>10.2f}{equity[4]:>10.2f}{format_slope(equity_slope):>20}")
        print(f"{'Free Cash Flow':<20}{free_cash_flows[0]:>10.2f}{free_cash_flows[1]:>10.2f}{free_cash_flows[2]:>10.2f}{free_cash_flows[3]:>10.2f}{free_cash_flows[4]:>10.2f}{format_slope(free_cash_flow_slope):>20}")

    except Exception as e:
        print(f"Error fetching financial data: {e}")

# Example usage
ticker = 'NVDA'  # Replace with any stock ticker
get_company_financials(ticker)