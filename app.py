from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# Correct the database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable modification tracking

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Todo model (database table)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(200), nullable=False)  # Task title
    desc = db.Column(db.String(500), nullable=False)  # Task description
    # Timezone-aware UTC timestamp
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create the database tables inside the application context
with app.app_context():
    db.create_all()  # This ensures the tables are created before the app starts

@app.route("/",methods=['GET','POST' ])  # Home page
def home():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/about')  # Products page
def about():
    return render_template('about.html')

@app.route('/show')  # Products page
def products():
    allTodo=Todo.query.all()
    #print(allTodo)
    return 'This is the products page'

@app.route('/update/<int:sno>',methods=['GET','POST' ])  # Products page
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')  # Products page
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=7000)
