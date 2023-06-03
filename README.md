# roselia_chord

[楽器.me](https://gakufu.gakki.me/)からRoseliaの曲をスクレイピングし、コード進行から作曲者を推論する。
[元記事:自然言語処理の手法を用いてコード進行から作曲者を推論した](https://qiita.com/bokuranosenjou/items/973a39c0ac708ecc71a0)

## 実行環境
- MacOS Ventura ver13.3.1
- Python 3.8.13

## ファイル
- scraping.py : スクレイピング用のスクリプト
- chord.py　:　コード進行からword2vecでベクトル表現を獲得し、推論を行う。
- roselia_songs.py : スクレイピング対象の曲リスト

## 使い方
```
pip3 install -r requirements.txt
python3 scraping.py
python3 chord.py
```
