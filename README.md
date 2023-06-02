# roselia_chord

[楽器.me](https://gakufu.gakki.me/)からRoseliaの曲をスクレイピングし、コード進行から作曲者を推論する。

## 環境
- MacOS Ventura ver13.3.1
- Python 3.8.13

## ファイル
- scraping.py : スクレイピング用のスクリプト
- chord.py :　コード進行からword2vecでベクトル表現を獲得し、推論を行う。
- roselia_songs.py : スクレイピング対象の曲リスト
