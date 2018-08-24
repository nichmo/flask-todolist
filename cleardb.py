# DBを毎回手打ちすると辛いので、作り直すためのデフォルトソース
from todo import db, User, Todo

# 一旦データベースを作り直す
db.drop_all()
db.create_all()

# admin ユーザを再作成
user = User('admin')
db.session.add(user)
db.session.commit()

# admin Todoの投稿を2件作成
todo1 = Todo('todotext1', user.id)
todo2 = Post('todotext2', user.id)
db.session.add(todo1)
db.session.add(todo2)
db.session.commit()