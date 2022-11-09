from flask import Flask, render_template, request, redirect
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)


#Database model
class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return '<Task %r>' % self.id

#Routing
@app.route('/', methods= ['POST', 'GET']) #Base route
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task =Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return"There is an issue in adding task"
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There is an issue while deleting the task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue while updating the task!!"
    else:
        return render_template('update.html', task= task)

    

#app.run(host="0.0.0.0", port=80) #localhost with 0.0.0.0

if __name__ == "__main__":
    app.run(debug=True)

