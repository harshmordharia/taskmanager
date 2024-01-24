from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://task_manager_user:TM123@localhost/task_manager_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.String(50))
    description = db.Column(db.String(500))

# Explicitly create tables before the first request
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

# Define the custom filter
@app.template_filter('format_deadline')
def format_deadline(deadline):
    if isinstance(deadline, str):
        return deadline
    return deadline.strftime('%d-%m-%Y')

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form.get('name')
    deadline = request.form.get('deadline')
    description = request.form.get('description')

    new_task = Task(name=name, deadline=deadline, description=description)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
