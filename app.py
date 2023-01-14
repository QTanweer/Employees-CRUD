from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    employees = Employee.query.all()
    return render_template('home.html', employees=employees)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        address = request.form['address']
        employee = Employee(name=name, salary=salary, address=address)
        db.session.add(employee)
        db.session.commit()
        return redirect('/')
    return render_template('create.html')

@app.route('/read/<int:id>')
def read(id):
    employee = Employee.query.get(id)
    return render_template('read.html', employee=employee)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.salary = request.form['salary']
        employee.address = request.form['address']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', employee=employee)

@app.route('/delete/<int:id>')
def delete(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
