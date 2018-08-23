from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB周りの設定を追加
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# db.Modelを継承してUserクラスを定義、id,usernameのみ
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)

  def __init__(self, username):
    self.username = username

# db.Modelを継承してTodoクラスを定義、id,todoname,type(0=未完了,1=テストUp,2＝本番Up)
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  todoname = db.Column(db.String(890))

  def __init__(self, username):
    self.todoname = todoname

# 入り口
@app.route("/")
def top():
  user_list = User.query.all()
  # return "Hello World"
  return render_template('top.html',title='ユーザー一覧', user_list=user_list)

# ユーザー登録
@app.route("/add_user", methods=['POST'])
def add_user():
  username = request.form.get('username')
  if username:
    user = User(username)
    db.session.add(user)
    db.session.commit()

  # ユーザー登録簿は元ページにリダイレクト
  return redirect(url_for('top'))

# データ参照
@app.route("/user/<int:user_id>", methods=['GET'])
def show_user(user_id):
  target_user = User.query.get(user_id)

  return render_template('show.html', title='ユーザー詳細', target_user=target_user)

# 数字を受け取る　修正する
@app.route("/user/<int:user_id>", methods=['POST'])
def mod_user(user_id):
  # primary keyを利用する getメソッドで対象ユーザーIDを取得
  target_user = User.query.get(user_id)
  # Usernameを取得
  username = request.form.get('username')

  # dataの存在を確認
  if target_user and username:
    target_user.username = username
    db.session.commit()

  return redirect(url_for('top'))

@app.route("/del_user/<int:user_id>", methods=['POST'])
def del_user(user_id):
  # primary keyを利用する場合,getメソッドで対象ユーザーIDを取得
  target_user = User.query.get(user_id)

  if target_user:
    db.session.delete(target_user)
    db.session.commit()
  
  return redirect(url_for('top'))
  

if __name__ == '__main__':
  app.run(debug=True)
# app.config['SQLALCHEMY_DATABASE_URI'] = 