import tkinter as tk
from tkinter import messagebox
from binance.client import Client
import configparser
import os

# 已建立關閉按鈕

def is_valid_price(price):
    try:
        price = float(price)
        return True
    except ValueError:
        return False


def set_api():
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    client = Client(api_key, api_secret)
    try:
        account_info = client.get_account()
        print("成功連接到 Binance API!")
        api_window.destroy()
        show_trade_window()
    except Exception as error:
        messagebox.showerror("ERROR", f"{error}")
        api_window.destroy()

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

        if not is_valid_price(price):
            price_label.config(fg="red")
            messagebox.showerror("錯誤", "投入金額輸入錯誤")
            return
        else:
            price_label.config(fg="black")

        if not grid_num.isdigit():
            grid_label.config(fg="red")
            messagebox.showerror("錯誤", "網格數輸入錯誤")
            return
        else:
            grid_label.config(fg="black")

        high_price = float(high_price)
        low_price = float(low_price)
        price = float(price)
        grid_num = int(grid_num)

        if low_price >= high_price:
            messagebox.showerror("錯誤", "投入金額填寫錯誤")
            return

        print(f"最高價: {high_price}, 最低價: {low_price}, 網格數: {grid_num}, 投入金額: {price}")

    def close_main():
        root.destroy()

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

    # 建立確認按鈕
    confirm_button = tk.Button(root, text="確認", command=confirm, font=("Arial", 14))
    confirm_button.place(x=150, y=300, width=100, height=40)

    # 建立關閉按鈕
    exit_button = tk.Button(root, text="關閉", command=close_main, font=("Arial", 14))
    exit_button.place(x=400, y=300, width=100, height=40)

    root.mainloop()


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