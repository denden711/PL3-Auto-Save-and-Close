import os
import pyautogui
import time
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def log_message(log_file_path, message):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def execute_pl3_and_save(file_path, log_file_path, wait_time=5, retry_limit=3):
    log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 起動開始")
    try:
        # .pl3 ファイルを実行
        process = subprocess.Popen(file_path, shell=True)
        time.sleep(wait_time)  # ファイル実行後に待機

        # 上書き保存操作
        for attempt in range(1, retry_limit + 1):
            try:
                pyautogui.hotkey('alt', 'f')
                time.sleep(0.5)
                pyautogui.press('s')
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(2)
                if os.path.exists(file_path + '~'):
                    log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 上書き保存: 成功")
                    break
                else:
                    raise Exception("上書き保存ファイルが存在しません")
            except Exception as e:
                if attempt == retry_limit:
                    log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 上書き保存: 失敗 - エラー: {str(e)} - リトライ回数: {attempt}")
                else:
                    time.sleep(1)  # リトライ前に少し待機

        # ウィンドウを閉じる操作
        for attempt in range(1, retry_limit + 1):
            try:
                pyautogui.hotkey('alt', 'f')
                time.sleep(0.5)
                pyautogui.press('x')
                log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 閉じる: 成功")
                break
            except Exception as e:
                if attempt == retry_limit:
                    log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 閉じる: 失敗 - エラー: {str(e)} - リトライ回数: {attempt}")
                else:
                    time.sleep(1)  # リトライ前に少し待機

    except Exception as e:
        log_message(log_file_path, f"{datetime.now()} - パス: {file_path} - 起動: 失敗 - エラー: {str(e)}")

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()
    return directory_path

if __name__ == "__main__":
    directory_path = select_directory()
    if not directory_path:
        print("ディレクトリが選択されていません。")
        exit()

    log_file_path = os.path.join(os.path.dirname(__file__), "pl3_save_log.txt")

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pl3"):
                file_path = os.path.join(root, file)
                execute_pl3_and_save(file_path, log_file_path)
