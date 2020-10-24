# 特記事項

## デプロイ

Heroku:
- https://team-stanza.herokuapp.com/

## データベース
- マイグレーションの作成: `python manage.py makemigrations`
- `django_on_docker/posts/migrations/0002_auto.py` をコピー
- `django_on_docker/posts/fixture` をコピー
- `django_on_docker/app/fixture` をコピー
- マイグレーションの実行: `python manage.py migrate`
- データベースの削除: `rm -d -r db.sqlite3` (*DBをPostgreSQLにした後変更する必要あり)

## ルーティング
|-- /admin : 管理者ページ \
| \
|-- /accounts  
|　　|-- /login : サインインページ  
|　　|-- /logout : サインアウトページ  
|  
|-- /create_account : サインアップページ  
|-- /posts : 投稿一覧 \
|　　|-- /{post_id} : 投稿詳細 \
|　　| \
|　　|-- /create : 投稿 \
|　　| \
|　　|-- /edit/{post_id} : 投稿編集 \
|　　| \
|　　|-- /delete/{post_id} : 投稿削除 \
|　　| \
|　　|-- /hoge/{post_id} : コメント作成
|　　| \
|　　|-- /ranking/[ahare|wokashi] : ランキング

## 旧stanzaからの変更点
- アカウント別投稿一覧ページの作成
- 書評投稿システムを構築
- 各種ファイルにおいてデザインを大幅に変更！

### 変更ファイル
- view.py
    - それぞれのページを表示するためのコードを追加
- models.py
    - 書評用のクラスを作成
- 各種htmlファイル
    - 書評投稿ページや投稿一覧ページのテンプレートを作成
    - review_edit.html
    - review.css
    - review.html
    - review_book_select.html
    - list.html
