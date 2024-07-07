import pyautogui
import time
import subprocess
import os
import pygetwindow as gw
from tkinter import filedialog, Tk, messagebox
import json
import logging

# ログ設定
logging.basicConfig(filename='pl3_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 座標をファイルから読み込む
try:
    with open("coords.json", "r") as f:
        coords = json.load(f)
    save_button_coords = coords["save_button_coords"]
    confirm_button_coords = coords["confirm_button_coords"]
    close_button_coords = coords["close_button_coords"]
except FileNotFoundError:
    error_message = "coords.json ファイルが見つかりません。先に座標取得スクリプトを実行してください。"
    messagebox.showerror("エラー", error_message)
    logging.error(error_message)
    exit()
except json.JSONDecodeError as e:
    error_message = f"coords.json の読み込み中にエラーが発生しました: {e}"
    messagebox.showerror("エラー", error_message)
    logging.error(error_message)
    exit()
except Exception as e:
    error_message = f"coords.json の読み込み中に予期しないエラーが発生しました: {e}"
    messagebox.showerror("エラー", error_message)
    logging.error(error_message)
    exit()

# GUIでディレクトリを選択するための関数
def select_directory():
    try:
        root = Tk()
        root.withdraw()  # メインウィンドウを表示しない
        directory_path = filedialog.askdirectory()
        if not directory_path:
            raise ValueError("ディレクトリが選択されていません。")
        return directory_path
    except Exception as e:
        error_message = f"ディレクトリ選択中にエラーが発生しました: {e}"
        messagebox.showerror("エラー", error_message)
        logging.error(error_message)
        exit()

# ディレクトリを選択
directory_path = select_directory()
logging.info(f"選択されたディレクトリ: {directory_path}")
print(f"選択されたディレクトリ: {directory_path}")

# 上書き保存が成功したか確認する関数
def is_save_successful(file_path):
    backup_file_path = file_path + "~"
    return os.path.exists(backup_file_path)

# 指定したディレクトリ以下のすべての .pl3 ファイルを処理
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        if filename.endswith(".pl3"):
            file_path = os.path.join(root, filename)
            logging.info(f"処理中のファイル: {file_path}")
            print(f"処理中のファイル: {file_path}")
            
            # .pl3ファイルを開く
            try:
                subprocess.Popen([file_path], shell=True)
                logging.info(f"{file_path} ファイルを開きました。")
                print("ファイルを開きました。")
            except Exception as e:
                error_message = f"{file_path} のオープン中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

            # ファイルが開くまで待つ（必要に応じて時間を調整）
            time.sleep(10)

            # ウィンドウの情報を取得
            try:
                window = gw.getActiveWindow()
                if window is None:
                    raise Exception("アクティブウィンドウが見つかりませんでした。")
                logging.info("ウィンドウを取得しました。")
                print("ウィンドウを取得しました。")
            except Exception as e:
                error_message = f"ウィンドウの操作中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

            # ウィンドウの位置を取得
            try:
                win_x, win_y = window.left, window.top
                logging.info(f"ウィンドウ位置: ({win_x}, {win_y})")
                print(f"ウィンドウ位置: ({win_x}, {win_y})")
            except Exception as e:
                error_message = f"ウィンドウ情報の取得中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

            # 上書き保存ボタンをクリック
            try:
                pyautogui.click(win_x + save_button_coords[0], win_y + save_button_coords[1])
                logging.info("上書き保存ボタンをクリックしました。")
                print("上書き保存ボタンをクリックしました。")
                time.sleep(2)  # 確認ボタンが表示されるまでの待ち時間
            except Exception as e:
                error_message = f"上書き保存ボタンのクリック中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

            # 上書き保存の確認ボタンをクリック
            try:
                pyautogui.click(win_x + confirm_button_coords[0], win_y + confirm_button_coords[1])
                logging.info("上書き保存の確認ボタンをクリックしました。")
                print("上書き保存の確認ボタンをクリックしました。")
                time.sleep(2)  # 保存が完了するまでの待ち時間
            except Exception as e:
                error_message = f"上書き保存の確認ボタンのクリック中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

            # 保存が成功したか確認し、成功していない場合は再試行
            attempt = 1
            max_attempts = 3
            while attempt <= max_attempts:
                if is_save_successful(file_path):
                    logging.info(f"上書き保存が成功しました: {file_path}")
                    print(f"上書き保存が成功しました: {file_path}")
                    break
                else:
                    logging.warning(f"上書き保存が失敗しました。再試行します ({attempt}/{max_attempts}): {file_path}")
                    print(f"上書き保存が失敗しました。再試行します ({attempt}/{max_attempts}): {file_path}")
                    # 上書き保存ボタンをクリック
                    try:
                        pyautogui.click(win_x + save_button_coords[0], win_y + save_button_coords[1])
                        logging.info("上書き保存ボタンを再度クリックしました。")
                        print("上書き保存ボタンを再度クリックしました。")
                        time.sleep(2)  # 確認ボタンが表示されるまでの待ち時間
                    except Exception as e:
                        error_message = f"上書き保存ボタンのクリック中にエラーが発生しました: {e}"
                        logging.error(error_message)
                        print(error_message)
                        continue

                    # 上書き保存の確認ボタンをクリック
                    try:
                        pyautogui.click(win_x + confirm_button_coords[0], win_y + confirm_button_coords[1])
                        logging.info("上書き保存の確認ボタンを再度クリックしました。")
                        print("上書き保存の確認ボタンを再度クリックしました。")
                        time.sleep(2)  # 保存が完了するまでの待ち時間
                    except Exception as e:
                        error_message = f"上書き保存の確認ボタンのクリック中にエラーが発生しました: {e}"
                        logging.error(error_message)
                        print(error_message)
                        continue

                    attempt += 1

            if attempt > max_attempts:
                logging.error(f"上書き保存が失敗しました: {file_path}")
                print(f"上書き保存が失敗しました: {file_path}")
                continue

            # 閉じるボタンをクリック
            try:
                pyautogui.click(win_x + close_button_coords[0], win_y + close_button_coords[1])
                logging.info("閉じるボタンをクリックしました。")
                print("閉じるボタンをクリックしました。")
                time.sleep(2)  # ファイルが閉じるまでの待ち時間
            except Exception as e:
                error_message = f"閉じるボタンのクリック中にエラーが発生しました: {e}"
                logging.error(error_message)
                print(error_message)
                continue

print("すべてのファイルを処理しました。")
logging.info("すべてのファイルを処理しました。")
messagebox.showinfo("完了", "すべてのファイルの処理が完了しました。")
