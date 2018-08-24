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
  todotext = db.Column(db.String(890))
  user_id = db.Column(db.Integer)
  phase = db.Column(db.Integer)  #0:未着手 1:テストUP 2:本番環境UP

  def __init__(self, todotext, user_id):
    self.todotext = todotext
    self.user_id = user_id
    self.phase = 0


# user 入り口
@app.route("/")
def top():
  user_list = User.query.all()
  todo_list = Todo.query.all()
  # return "Hello World"
  return render_template('top.html',title='ユーザー一覧', user_list=user_list, todo_list=todo_list)

# todo
# ユーザー登録 formでデータ取得する
@app.route("/add_todo", methods=['POST'])
def add_todo():
  todotext = request.form.get('todotext')
  user_id = request.form.get('user_id')
  if todotext:
    todo = Todo(todotext, user_id)
    db.session.add(todo)
    db.session.commit()

  # ユーザー登録簿は元ページにリダイレクト
  return redirect(url_for('top'))

# データ参照 aタグのリンクのパラメータでuser_idを取得する
@app.route("/todo/<int:todo_id>", methods=['GET'])
def show_todo(todo_id):
  target_todo = Todo.query.get(todo_id)

  return render_template('showtodo.html', title='Todo詳細', target_todo=target_todo)

# 数字を受け取る　修正する
@app.route("/todo/<int:todo_id>", methods=['POST'])
def mod_todo(todo_id):
  # primary keyを利用する getメソッドで対象todoIDを取得
  target_todo = Todo.query.get(todo_id)
  # todotextを取得
  todotext = request.form.get('todotext')
  phase = request.form.get('phase')

  # dataの存在を確認
  if target_todo and todotext:
    target_todo.todotext = todotext
    target_todo.phase = phase
    db.session.commit()

  return redirect(url_for('top'))


@app.route("/todo/<int:todo_id>", methods=['POST'])
def done_todo(todo_id):
  # primary keyを利用する getメソッドで対象todoIDを取得
  target_todo = Todo.query.get(todo_id)
  # todotextを取得
  phase = request.form.get('phase')
  phase += 1

  # dataの存在を確認
  if target_todo:
    target_todo.phase = phase
    db.session.commit()

  return redirect(url_for('top'))  

@app.route("/del_todo/<int:user_id>", methods=['POST'])
def del_todo(todo_id):
  # primary keyを利用する場合,getメソッドで対象ユーザーIDを取得
  target_todo = User.query.get(todo_id)

  if target_todo:
    db.session.delete(target_todo)
    db.session.commit()
  
  return redirect(url_for('top'))

# todo -->

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