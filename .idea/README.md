# Stock Alert App

A Python-based stock alert notifier for NSE (India) stocks using real-time data from Yahoo Finance.
Gives alerts if a stock crosses your customised range.

---

## Features

-  System notification alerts when stock price enters a defined range
-  Customizable stock list and range via CSV
-  Real-time stock data using `yfinance`
-  Lightweight and beginner-friendly

---

##  CSV Format (`alerts_ranges.csv`)

| Symbol      | MinPrice | MaxPrice |
|-------------|----------|----------|
| INFY.NS     | 1400     | 1600     |
| RELIANCE.NS | 2500     | 2700     |
| M&M.NS      | 1800     | 2000     |

> Use Yahoo Finance symbols for NSE stocks, ending with `.NS` (e.g., `TCS.NS`, `HDFCBANK.NS`, etc.)

---

## ⚙️ How to Use

### 1. Clone or Download the Project

```bash
  git clone https://github.com/yourusername/StockAlertApp.git
cd StockAlertApp
```

### 2. Install dependencies
```bash
  pip install -r requirements.txt
```