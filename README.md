# life is tech translation script check

Script　の翻訳を少し楽にするコード

## 使い方
1. Python ファイル (check.py) をローカルにダウンロードする
2. プロジェクトフォルダの中の　lesson_snaps フォルダの中に check.py を移動する。  
e.g. b_zootopia_6/lesson_snaps
3. ファイルを実行  
**実行方法:**  
    - `python3 <check.pyのパス> ls`  
    step づつどのファイルが編集されているかをリストアウト。（それ以外のファイルは翻訳を前のステップからコピペすればいい。）　　
    - `python3 copy <check.pyのパス>  <source> <destination>`(例： python3 <path> step010 step080)  
  src のステップのファイルのコンテンツを src から dest ステップまで全てのステップのファイルにコピーする。ただし編集されているファイルはコピーされない。編集されているファイルが同じステップをまとめてコピペするといい。  　　
    - `python3 <check.pyのパス> japanese`  
    lesson_snaps の中の　editor フォルダにあるレッスンファイルの中に日本が残っているかチェックする。残っていればどのフィイルにあるか出力される。
  
  
 あくまで変わっていないところのコピペだけなので、コピペの元の翻訳をするのを忘れずに！  
 例えば、copy step010 step080　の場合は　step010の begin, input, result の中のファイルは全て訳す。また、コピペされていないファイル（編集が加わってるファイル）はステップづつ翻訳・コピペしていく。
