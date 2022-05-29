
#---メモ---
#$env:FLASK_APP = "app"
#$env:FLASK_ENV = "development"
#python -m flask run


#---ライブラリのインポート---
from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz


#---いろいろと初期設定---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordls_db.db'
db = SQLAlchemy(app)


#---データベース設定---
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)#idの定義（必須）
    word = db.Column(db.String(100), nullable=True)
    word_type = db.Column(db.String(100), nullable=True)
    word_mean = db.Column(db.String(100), nullable=True)
    word_ex = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(pytz.timezone("Asia/Tokyo")))


#---以下ルーティング---

#---メインページ---
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        posts  = Post.query.all()#DBの「内容」を取得するお！！
        return render_template("index.html",posts=posts)#htmlを返す、DBの全内容を返す！！



#---記録追加ページ---
@app.route("/create",methods=["GET","POST"])
def create():
    if request.method == "POST":
        word = request.form.get("word")
        word_type = request.form.get("word_type")
        word_mean = request.form.get("word_mean")
        word_ex = request.form.get("word_ex")

        post = Post(
                    word = word,
                    word_type = word_type,
                    word_mean = word_mean,
                    word_ex = word_ex
                    )

        db.session.add(post)#DBについかする！
        db.session.commit()#「追加した」という変更を保存する（絶対必須！）
        return redirect("/")

    else:
        li=["動詞","名詞","形容詞","代名詞","助動詞","副詞","前置詞","接続詞","冠詞","間投詞","??"]
        return render_template("create.html",li=li)


#---編集ページ---
@app.route("/<int:id>/update",methods=["GET","POST"])
def update(id):
    post = Post.query.get(id)#編集用のやつだけ

    if request.method == "GET":
        return render_template("update.html",post=post)

    else:
        post.word = request.form.get("word")
        post.word_type = request.form.get("word_type")
        post.word_mean = request.form.get("word_mean")
        post.word_ex = request.form.get("word_ex")
        db.session.commit()#「編集した」という変更を保存する（絶対必須！）
        return redirect("/")


#---削除ページ---
@app.route("/<int:id>/delete",methods=["GET"])
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)#とってきたidの情報を削除
    db.session.commit()
    return redirect("/")

#---詳細を見る---
@app.route("/<int:id>/info",methods=["GET"])
def info(id):
    post = Post.query.get(id)
    return render_template("info.html",post=post)

if __name__ == '__main__':
    app.run()