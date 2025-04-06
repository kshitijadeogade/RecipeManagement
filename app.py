from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from pymongo import MongoClient
from db import createUser, loginUser, getUserByEmail  # You'll need to implement getUserByEmail
from bson import ObjectId  # Required to convert string ID back to ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MongoDB Setup (optional if used in db.py)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['taste_trail']

# User Class
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # Flask-Login requires `id` attribute
        self.email = user_data['email']
        self.name = user_data.get('name', '')

@login_manager.user_loader
def load_user(user_id):
    user_data = getUserByEmail(user_id, by_id=True)  # Lookup by _id, not email
    if user_data:
        return User(user_data)
    return None

@app.route('/')
def index():
    return render_template('index.html', user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        code = createUser(email, password, name)
        if code['code'] == 'USER_CREATED':
            flash("User Created Successfully.")
        elif code['code'] == 'EXISTING_USER':
            flash("Existing User Found.")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        code = loginUser(email, password)
        if code['code'] == 'USER_LOGGED_IN':
            user_data = getUserByEmail(email)
            user = User(user_data)
            login_user(user)
            flash("Logged in Successfully.")
            return redirect(url_for('index'))
        elif code['code'] == 'INVALID_CREDENTIALS':
            flash("Invalid Credentials.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/add-recipe')
@login_required
def add_recipe():
    return render_template('add_recipe.html')

@app.route('/edit_recipe')
@login_required
def edit_recipe():
    return render_template('edit_recipe.html')

@app.route('/my_recipes')
@login_required
def my_recipes():
    return render_template('my_recipe.html')

if __name__ == '__main__':
    app.run()
