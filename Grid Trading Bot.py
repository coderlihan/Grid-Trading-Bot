import tkinter as tk
from tkinter import messagebox
from binance.client import Client
from binance.spot import Spot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import configparser
import sys
import os


def is_valid_price(price):
    try:
        price = float(price)
        return True
    except ValueError:
        return False


def set_api():
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    client = Client(api_key, api_secret)  # 連接到網路
    try:
        account_info = client.get_account()
        print("成功連接到 Binance API!")
        api_window.withdraw()  # 隱藏窗口
        api_window.quit()  # 結束事件循環
        return account_info
    except Exception as error:
        messagebox.showerror("ERROR", f"{error}")
        sys.exit()


def show_trade_window():
    def confirm():
        high_price = high_entry.get()
        low_price = low_entry.get()
        grid_num = grid_entry.get()
        price = price_entry.get()

        if not is_valid_price(high_price):
            high_label.config(fg="red")
            messagebox.showerror("錯誤", "最高價輸入錯誤")
            return
        else:
            high_label.config(fg="black")

        if not is_valid_price(low_price):
            low_label.config(fg="red")
            messagebox.showerror("錯誤", "最低價輸入錯誤")
            return
        else:
            low_label.config(fg="black")

        if low_price >= high_price:
            messagebox.showerror("錯誤", "價格填寫錯誤")
            return

        if not grid_num.isdigit():
            grid_label.config(fg="red")
            messagebox.showerror("錯誤", "網格數輸入錯誤")
            return
        else:
            grid_label.config(fg="black")

        if not is_valid_price(price):
            price_label.config(fg="red")
            messagebox.showerror("錯誤", "投入金額輸入錯誤")
            return
        else:
            price_label.config(fg="black")

        high_price = float(high_price)
        low_price = float(low_price)
        price = float(price)
        grid_num = int(grid_num)

        print(f"最高價: {high_price}, 最低價: {low_price}, 網格數: {grid_num}, 投入金額: {price}")

    root = tk.Tk()
    root.title("交易參數設置")
    root.geometry("640x480")

    # 建立標籤和輸入欄位
    high_label = tk.Label(root, text="最高價:", font=("Arial", 14))
    high_label.place(x=50, y=50)
    high_entry = tk.Entry(root, font=("Arial", 14))
    high_entry.place(x=150, y=50, width=200)

    low_label = tk.Label(root, text="最低價:", font=("Arial", 14))
    low_label.place(x=50, y=100)
    low_entry = tk.Entry(root, font=("Arial", 14))
    low_entry.place(x=150, y=100, width=200)

    grid_label = tk.Label(root, text="網格數:", font=("Arial", 14))
    grid_label.place(x=50, y=150)
    grid_entry = tk.Entry(root, font=("Arial", 14))
    grid_entry.place(x=150, y=150, width=200)

    price_label = tk.Label(root, text="投入金額:", font=("Arial", 14))
    price_label.place(x=50, y=200)
    price_entry = tk.Entry(root, font=("Arial", 14))
    price_entry.place(x=150, y=200, width=200)

    # 建立顯示價格按鈕
    price_button = tk.Button(root, text="查詢幣價", command=show_currencyprice_window, font=("Arial", 14))
    price_button.place(x=300, y=370, width=100, height=40)

    # 建立顯示價格按鈕
    assets_button = tk.Button(root, text="查詢資產", command=show_assets_window, font=("Arial", 14))
    assets_button.place(x=300, y=300, width=100, height=40)

    # 建立確認按鈕
    confirm_button = tk.Button(root, text="確認", command=confirm, font=("Arial", 14))
    confirm_button.place(x=150, y=300, width=100, height=40)

    # 建立關閉按鈕
    exit_button = tk.Button(root, text="關閉", command=sys.exit, font=("Arial", 14))
    exit_button.place(x=450, y=300, width=100, height=40)

    root.mainloop()


def show_currencyprice_window():
    def get_currency():
        currency = currency_entry.get().upper() + "USDT"
        client = Spot()  # 創建客戶端對
        try:  # 嘗試獲取該貨幣的 k 線數據，如果成功則跳出迴圈，否則提示用戶重新輸入
            klines = client.klines(currency, "1h", limit=10)

            # 建立一個新的 figure 顯示目前價格
            plt.figure(currency)
            plt.title(f'Currency: {currency}')
            plt.ylabel('USDT')

            # 提取時間和收盤價
            times = [kline[0] for kline in klines]
            prices = [float(kline[4]) for kline in klines]  # 收盤價在第5個位置，索引為4
            # 將時間戳轉換為日期
            dates = [datetime.fromtimestamp(time / 1000) for time in times]
            # 繪製線圖
            plt.plot_date(dates, prices, linestyle='solid')
            # 美化日期標籤
            plt.gcf().autofmt_xdate()
            date_format = mdates.DateFormatter('%H:%M')
            plt.gca().xaxis.set_major_formatter(date_format)
            plt.show()  # 顯示圖表

        except Exception:
            messagebox.showerror("錯誤", "無效的貨幣名稱。請再試一次。")

    # 創建新的窗口
    price_window = tk.Tk()
    price_window.title("Choose Currency")
    price_window.geometry("400x200")

    # 建立標籤和輸入欄位
    currency_label = tk.Label(price_window, text="Choose Currency:", font=("Arial", 14))
    currency_label.place(x=50, y=50)
    currency_entry = tk.Entry(price_window, font=("Arial", 14))
    currency_entry.place(x=220, y=50, width=100)
    currency_entry.insert(0, "BTC")

    # 建立確認按鈕
    confirm_button = tk.Button(price_window, text="確認", command=get_currency, font=("Arial", 14))
    confirm_button.place(x=150, y=150, width=100, height=40)

    price_window.mainloop()


def show_assets_window():
    account_info = set_api()

    print("帳戶信息:", account_info)
    count = 0  # 計數幣種順序
    assets = []
    balances = []
    for balance in account_info['balances']:
        asset = balance['asset']
        free = float(balance['free'])  # 轉換為浮點數
        locked = float(balance['locked'])  # 轉換為浮點數
        total = free + locked
        if total > 0:
            count += 1
            asset = str(count) + "." + asset  # 用於標識幣種
            # 將資產名稱和總餘額添加到相應的列表中
            assets.append(asset)
            balances.append(total)
            print(count, ".", f"幣種: {asset}, 可用餘額: {free}, 鎖定餘額: {locked}")

    # 建立一個新的 figure
    plt.figure(num="Asset Balances")
    # 繪製鎖所持資產長條圖
    plt.pie(balances, labels=assets, autopct='%1.1f%%')
    plt.title('Asset Balances')
    plt.show()  # 顯示圖表


def show_api_window():
    global api_window, api_key_entry, api_secret_entry

    api_window = tk.Tk()
    api_window.title("API設置")
    api_window.geometry("400x200")

    # 讀取config.ini文件
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")
    config.read(config_file)

    # 獲取api_key和api_secret
    api_key = config.get("API", "api_key", fallback="Config ERROR")
    api_secret = config.get("API", "api_secret", fallback="Config ERROR")

    # 建立標籤和輸入欄位
    api_key_label = tk.Label(api_window, text="API Key:", font=("Arial", 14))
    api_key_label.place(x=50, y=50)
    api_key_entry = tk.Entry(api_window, font=("Arial", 14))
    api_key_entry.place(x=150, y=50, width=200)
    api_key_entry.insert(0, api_key)

    api_secret_label = tk.Label(api_window, text="API Secret:", font=("Arial", 14))
    api_secret_label.place(x=50, y=100)
    api_secret_entry = tk.Entry(api_window, font=("Arial", 14), show="*")
    api_secret_entry.place(x=150, y=100, width=200)
    api_secret_entry.insert(0, api_secret)

    # 建立確認按鈕
    confirm_button = tk.Button(api_window, text="確認", command=set_api, font=("Arial", 14))
    confirm_button.place(x=150, y=150, width=100, height=40)

    api_window.mainloop()


if __name__ == "__main__":
    # 首先顯示API設置視窗
    show_api_window()
    show_trade_window()
