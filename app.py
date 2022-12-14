from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 用此檔案名稱創一個Flask的instance
app = Flask(__name__)
# 將app連接到我們database: sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize我們的database ORM
with app.app_context():
    db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # 把欲新增的task push to database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        # 如果fail的話，跳error
        except:
            return 'There was as issue adding your task'

    else:
        # 顯示我們新增的task到主頁
        tasks = Todo.query.order_by(Todo.date_created).all()
        # 重新render我們的主頁
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    # 如果fail的話，跳error
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        
        # 把欲更新的task update to database
        try:
            db.session.commit()
            return redirect('/')

        # 如果fail的話，跳error
        except:
            return 'There was an issue updating your task'
        
    else:
        # 重新render我們的主頁
        return render_template('update.html', task=task_to_update)

# flask app 的 driver code
if __name__ == '__main__':
    app.run(debug=True)