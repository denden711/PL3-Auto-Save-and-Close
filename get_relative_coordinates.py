import pyautogui
import time
import pygetwindow as gw
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Button
import json
import logging

# ログ設定
logging.basicConfig(filename='get_coordinates.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def select_window():
    def on_select(event=None):
        try:
            selected_index = listbox.curselection()[0]
            selected_window = windows[selected_index]
            root.quit()
            root.destroy()
            select_window.selected_window = selected_window
        except IndexError:
            messagebox.showerror("エラー", "ウィンドウが選択されていません。")
            logging.error("ウィンドウが選択されていません。")
            return

    def on_quit():
        messagebox.showinfo("選択なし", "ウィンドウが選択されていません。プログラムを終了します。")
        logging.info("ウィンドウが選択されていません。プログラムを終了します。")
        root.quit()
        root.destroy()
        exit()

    root = tk.Tk()
    root.title("ウィンドウ選択")

    listbox = Listbox(root, selectmode=tk.SINGLE)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    for window in windows:
        listbox.insert(tk.END, window)

    button = Button(root, text="選択", command=on_select)
    button.pack(side=tk.BOTTOM, fill=tk.X)

    root.protocol("WM_DELETE_WINDOW", on_quit)
    listbox.bind('<Double-1>', on_select)  # ダブルクリックでも選択を可能にする
    root.mainloop()

# 開いているすべてのウィンドウのタイトルを取得
try:
    windows = gw.getAllTitles()
    windows = [title for title in windows if title]  # 空のタイトルを除外
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウの取得中にエラーが発生しました: {e}")
    logging.error(f"ウィンドウの取得中にエラーが発生しました: {e}")
    exit()

if not windows:
    messagebox.showinfo("ウィンドウなし", "開いているウィンドウがありません。")
    logging.info("開いているウィンドウがありません。")
    exit()

# ウィンドウを選択する
select_window()

# 選択されたウィンドウの情報を取得
selected_window = select_window.selected_window
try:
    window = gw.getWindowsWithTitle(selected_window)[0]
    window.activate()
except IndexError:
    messagebox.showerror("エラー", "指定されたウィンドウが見つかりません。")
    logging.error("指定されたウィンドウが見つかりません。")
    exit()
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウの操作中にエラーが発生しました: {e}")
    logging.error(f"ウィンドウの操作中にエラーが発生しました: {e}")
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
        logging.error(f"座標取得中にエラーが発生しました: {e}")
        exit()

# ウィンドウの位置とサイズを取得
try:
    win_x, win_y, win_width, win_height = window.left, window.top, window.width, window.height
except Exception as e:
    messagebox.showerror("エラー", f"ウィンドウ情報の取得中にエラーが発生しました: {e}")
    logging.error(f"ウィンドウ情報の取得中にエラーが発生しました: {e}")
    exit()

# 各ボタンの座標を取得
try:
    save_button_coords = get_relative_coordinates("上書き保存ボタン")
    confirm_button_coords = get_relative_coordinates("上書き保存の確認ボタン")
    close_button_coords = get_relative_coordinates("閉じるボタン")
except Exception as e:
    messagebox.showerror("エラー", f"ボタン座標の取得中にエラーが発生しました: {e}")
    logging.error(f"ボタン座標の取得中にエラーが発生しました: {e}")
    exit()

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
    logging.info("座標を coords.json に保存しました。")
except Exception as e:
    messagebox.showerror("エラー", f"座標の保存中にエラーが発生しました: {e}")
    logging.error(f"座標の保存中にエラーが発生しました: {e}")
    exit()
