from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from db import createUser, loginUser

app = Flask(__name__)

@app.route('/dashboard')
def hello_world():
    #return 'Hello World'
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        code = createUser(email, password, name)
        if(code['code'] == 'USER_CREATED'):
            return render_template('signup.html', message="User Created Successfully.")
        elif(code['code'] == 'EXISTING_USER'):
            return render_template('signup.html', message="Existing User Found.")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        code = loginUser(email, password)
        if(code['code'] == 'USER_LOGGED_IN'):
            return render_template('login.html', message="Logged IN Successfully.")
        elif(code['code'] == 'INVALID_CREDENTIALS'):
            return render_template('login.html', message="Invalid Credentials.")
    return render_template('login.html')

@app.route('/add-recipe')
def add_recipe():
    return render_template('add-recipe.html')

@app.route('/edit-recipe')
def edit_recipe():
    return render_template('edit-recipe.html')

@app.route('/my-recipes')
def my_recipes():
    return render_template('my-recipe.html')

if __name__ == '__main__':
    app.run()