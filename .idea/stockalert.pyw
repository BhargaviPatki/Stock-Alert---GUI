import pandas as pd
import yfinance as yf
import threading
import time
from tkinter import *
from tkinter import messagebox
from plyer import notification
import os
import sys

# ✅ Get the folder where the .exe or .pyw is located
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(base_dir, "alert_ranges.csv")

# ✅ Flags and data
monitoring = False
alerted_stocks = []

# ✅ Notification Function
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# ✅ Fetch Live Price
def fetch_yfinance_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info['regularMarketPrice']
    except Exception:
        return None

# ✅ Monitor Function
def monitor_stocks():
    global monitoring, alerted_stocks
    alerted_stocks.clear()
    seen_alerts = set()

    while monitoring:
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read CSV:\n{e}")
            break

        for index, row in df.iterrows():
            symbol = row['Symbol']
            low = row['MinPrice']
            high = row['MaxPrice']

            price = fetch_yfinance_price(symbol)
            if price is None:
                continue

            if price <= low:
                alert_key = (symbol, "Low")
                if alert_key not in seen_alerts:
                    seen_alerts.add(alert_key)
                    alerted_stocks.append({"Symbol": symbol, "Price": price, "Alert": f"Below Min ({low})"})
                    send_notification("📉 Stock Alert", f"{symbol}: ₹{price} is below ₹{low}")

            elif price >= high:
                alert_key = (symbol, "High")
                if alert_key not in seen_alerts:
                    seen_alerts.add(alert_key)
                    alerted_stocks.append({"Symbol": symbol, "Price": price, "Alert": f"Above Max ({high})"})
                    send_notification("📈 Stock Alert", f"{symbol}: ₹{price} is above ₹{high}")

        time.sleep(30)

# ✅ Start Button Action
def start_monitoring():
    global monitoring
    if not monitoring:
        monitoring = True
        download_button.pack_forget()
        threading.Thread(target=monitor_stocks, daemon=True).start()
        status_label.config(text="Monitoring Started ✅")

# ✅ Stop Button Action
def stop_monitoring():
    global monitoring
    monitoring = False
    status_label.config(text="Monitoring Stopped ⛔")
    if alerted_stocks:
        download_button.pack(pady=5)

# ✅ Download to Excel
def download_excel():
    try:
        df = pd.DataFrame(alerted_stocks)
        save_path = os.path.join(base_dir, "notified_stocks.xlsx")
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Download Complete", f"✅ Excel saved as:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save Excel:\n{e}")

# ✅ GUI Setup
root = Tk()
root.title("📊 Stock Alert App")
root.geometry("320x250")
root.resizable(False, False)

Label(root, text="Live NSE Stock Monitor", font=("Arial", 14)).pack(pady=10)

Button(root, text="▶ Start Monitoring", command=start_monitoring, bg="green", fg="white", width=25).pack(pady=5)
Button(root, text="⏹ Stop Monitoring", command=stop_monitoring, bg="red", fg="white", width=25).pack(pady=5)

download_button = Button(root, text="📥 Download Alerted Stocks", command=download_excel, bg="blue", fg="white", width=25)

status_label = Label(root, text="Monitoring Not Started", fg="gray")
status_label.pack(pady=10)

root.mainloop()
