# WebGakuseiSystemBackup
web学生システムの受信メッセージのバックアップのためのスクリプト（ベータ版）
# 注意点
- 埼玉大学の公式配布物ではありません．
- あくまで学生個人がChat-GPTの力を借りながら作った不完全な制作物です．
- 実行に際して発生した不利益に関する責任は制作者は負いません．自己責任で実行してください．
- スクレイピングは本来人力で行う事を機械で短時間で行う性質上，サーバに瞬間的な負荷をかけます．無駄に回数実行しないでください．また，混雑の予想される時刻，時期での実行は控えてください．
## お願いと予防線
- 環境によっては実行できない場合がありますが，あまり詳しくないので対応できるか解りません．
- このコードには多分，かなりガバがあります．認証情報をコード内に平文で書くとか最悪だろうし．そのあたり解る人は気が向いたらもっとマシなプログラム作ってください．オナシャス！
- 上記の場合，イチから書くのが面倒ならこのコードを一部切り貼りしてもOK．その場合は，コメントでもreadmeでも適当なところにこれを使ったとは書いておいてください
## 使った物
- selenium
- beautiful soup
## ライブラリのインポート
pip install selenium beautifulsoup4 webdriver-manager
## 使い方
- anaconda,venv,docker,wslなどの使い捨ての環境を用意することを推奨します．
- 31行目，32行目のaa bb の箇所を然るべき変更します．
- 実行すると実行したディレクトリ（フォルダー）にメッセージの受信箱のクリックしたときのサイトの画面（.html）とメッセージの内容（.txt）を保存します．
- 12行目のheadlessに関する記述を消すか，コメントアウトすると実行されている様子が見られますが，下手に触って何がおきるかは解らないので非推奨．
