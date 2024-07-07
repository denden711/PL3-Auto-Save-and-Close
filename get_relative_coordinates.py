import pyautogui
import time
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog, messagebox
import json

# 開いているすべてのウィンドウのタイトルを取得
try:
    windows = gw.getAllTitles()
    windows = [title for title in windows if title]  # 空のタイトルを除外
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウの取得中にエラーが発生しました: {e}")
    exit()

# GUIを作成してユーザーにウィンドウを選択させる
root = tk.Tk()
root.withdraw()  # メインウィンドウを表示しない

if not windows:
    messagebox.showinfo("ウィンドウなし", "開いているウィンドウがありません。")
    exit()

# ウィンドウのタイトルを選択
selected_window = simpledialog.askstring("ウィンドウ選択", "操作対象のウィンドウタイトルを選択してください:", initialvalue=windows[0])

if not selected_window:
    messagebox.showinfo("選択なし", "ウィンドウが選択されていません。プログラムを終了します。")
    exit()

# 選択されたウィンドウの情報を取得
try:
    window = gw.getWindowsWithTitle(selected_window)[0]
    window.activate()
except IndexError:
    messagebox.showerror("エラー", "指定されたウィンドウが見つかりません。")
    exit()
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウの操作中にエラーが発生しました: {e}")
    exit()

# 座標を取得する関数
def get_relative_coordinates(description):
    try:
        print(f"{description} の位置にマウスを移動させ、5秒後に座標を取得します。")
        time.sleep(5)
        mouse_x, mouse_y = pyautogui.position()
        relative_x = mouse_x - win_x
        relative_y = mouse_y - win_y
        print(f"取得した相対座標 ({description}): ({relative_x}, {relative_y})")
        messagebox.showinfo("取得した座標", f"取得した相対座標 ({description}): ({relative_x}, {relative_y})")
        return (relative_x, relative_y)
    except Exception as e:
        messagebox.showerror("エラー", f"座標取得中にエラーが発生しました: {e}")
        exit()

# ウィンドウの位置とサイズを取得
try:
    win_x, win_y, win_width, win_height = window.left, window.top, window.width, window.height
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウ情報の取得中にエラーが発生しました: {e}")
    exit()

# 各ボタンの座標を取得
save_button_coords = get_relative_coordinates("上書き保存ボタン")
confirm_button_coords = get_relative_coordinates("上書き保存の確認ボタン")
close_button_coords = get_relative_coordinates("閉じるボタン")

# 座標をファイルに保存
coords = {
    "save_button_coords": save_button_coords,
    "confirm_button_coords": confirm_button_coords,
    "close_button_coords": close_button_coords
}

try:
    with open("coords.json", "w") as f:
        json.dump(coords, f)
    print("座標を coords.json に保存しました。")
except Exception as e:
    messagebox.showerror("エラー", f"座標の保存中にエラーが発生しました: {e}")
    exit()
