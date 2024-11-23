# Stock Analyzer :chart_with_upwards_trend:

Welcome to **Stock Analyzer**! This Python script provides an easy way to retrieve and analyze financial data for any stock ticker using Yahoo Finance. The tool calculates important metrics such as revenue, operating profit, net income, and more, while also estimating their trends using linear regression. Perfect for investors who want a quick way to analyze a company's financial health. :moneybag:

## Features

- Extract financial metrics for any stock ticker using Yahoo Finance.
- Calculates key metrics such as revenue, gross profit, operating profit, net income, and more.
- Shows annual metrics for the past four years, plus the most recent quarter.
- Uses linear regression to identify trends in each financial metric.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)

## Setup

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
$ git clone https://github.com/petercunha/stock-analyzer.git
$ cd stock-analyzer
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

Create a virtual environment to manage your dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the necessary dependencies using `pip`:

```bash
$ pip install -r requirements.txt
```

The `requirements.txt` file contains:

```txt
numpy
pandas
yfinance
scikit-learn
```

## Usage

To run the stock analyzer, simply execute the Python script, passing in a stock ticker symbol. For example, if you want to analyze Intel Corporation:

```bash
$ python index.py
```

### Example Usage

You can modify the ticker symbol directly in the script to any desired stock ticker. For instance:

```python
ticker = 'NVDA'  # Replace with any stock ticker
get_company_financials(ticker)
```

The output includes:

- Historical financial metrics for the past four years.
- The most recent quarterly data.
- The trend in each metric (positive or negative) based on linear regression.

## Example Output

```
NVDA

Metric                    2024      2023      2022      2021   MRQ/TTM               Slope
Revenue                  16.68     26.91     26.97     60.92    113.27   Positive (22.72x)
Gross Profit             10.40     17.48     15.36     44.30     85.93   Positive (17.79x)
Operating Profit          4.53     10.04      5.58     32.97     71.03   Positive (15.59x)
Net Income                4.33      9.75      4.37     29.76     63.07   Positive (13.75x)
Total Assets             28.79     44.19     41.18     65.73     96.01   Positive (15.60x)
Total Liabilities        11.90     17.57     19.08     22.75     30.11    Positive (4.16x)
Total Equity             16.89     26.61     22.10     42.98     65.90   Positive (11.44x)
Free Cash Flow            4.69      8.13      3.81     27.02     16.81    Positive (4.31x)
```

## Dependencies

To ensure the script runs correctly, you need the following Python packages:

- `numpy`: Efficient mathematical operations and array manipulation.
- `pandas`: Data analysis and manipulation.
- `yfinance`: Fetching financial data from Yahoo Finance.
- `scikit-learn`: Performing linear regression for trend analysis.

Make sure to install these packages using the provided `requirements.txt` file.

## Contributing

Contributions are welcome! If you'd like to improve the script, feel free to fork the repository and submit a pull request. Please make sure to add relevant test cases and documentation for any new features.

1. Fork the repo.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. Feel free to use and distribute it as per the terms of the license.
