# PL3 File Auto-Save Script

## 概要

このPythonスクリプトは、指定したディレクトリ内にあるすべての`.pl3`ファイルを自動的に実行し、一連の操作を行った後に上書き保存します。スクリプトは、各操作の成功や失敗をログファイルに記録します。

## 機能

- 指定されたディレクトリ内の`.pl3`ファイルを再帰的に検索。
- 各`.pl3`ファイルを開いて一連のキー操作を実行。
- ファイルの上書き保存とウィンドウの閉じる操作を自動的に行う。
- 操作結果やエラーをログファイルに記録。

## 使用方法

1. **Pythonのインストール**: このスクリプトはPython 3.xで動作します。Pythonがインストールされていない場合は、[公式サイト](https://www.python.org/downloads/)からインストールしてください。

2. **必要なパッケージのインストール**:
   - スクリプトを実行するためには、以下のPythonパッケージが必要です。以下のコマンドを実行してインストールしてください。
     ```sh
     pip install pyautogui
     ```

3. **スクリプトの実行**:
   - `pl3_save_log.txt`という名前のログファイルがスクリプトと同じディレクトリに作成されます。
   - スクリプトを実行すると、ディレクトリ選択ダイアログが表示されます。処理したい`.pl3`ファイルが含まれるディレクトリを選択してください。
   - スクリプトは、選択されたディレクトリ内のすべての`.pl3`ファイルを処理し、結果をログに記録します。

4. **注意事項**:
   - スクリプト実行中は、キーボードとマウスの操作が干渉する可能性がありますので、他の操作を避けてください。

## ログファイル

- `pl3_save_log.txt`: 各`.pl3`ファイルに対して行われた操作の成功や失敗が記録されます。ログには、処理の開始時刻、操作内容、結果が含まれます。

## トラブルシューティング

- **エラーが発生した場合**:
  - ログファイルを確認し、エラーの詳細とリトライ回数を確認してください。スクリプトは最大3回までリトライを行いますが、すべてのリトライで失敗した場合、エラーがログに記録されます。