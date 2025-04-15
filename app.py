from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from pymongo import MongoClient
from db import createUser, loginUser, getUserByEmail, addRecipe, getMyRecipes, getAllRecipes  # You'll need to implement getUserByEmail
from bson import ObjectId  # Required to convert string ID back to ObjectId
from PIL import Image
import base64
from db import db

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
    res = getAllRecipes()
    if(res["code"] == "RECIPES_FOUND"):
        recipes = res["recipes"]
    else:
        recipes = []
    return render_template('index.html', user=current_user, recipes=recipes)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        code = createUser(email, password, name)
        if code['code'] == 'USER_CREATED':
            flash("User Created Successfully.")
            return redirect(url_for('login'))
        elif code['code'] == 'EXISTING_USER':
            flash("Existing User Found.")
            return render_template('signup.html', msg="User Already existed.")
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
            return render_template('login.html', msg="Invalid Credentials.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        note = request.form['note']
        userId = current_user.id
        image_file = request.files['image']
        if image_file and image_file.filename != '':
            image_data = image_file.read()
            mime_type = image_file.mimetype
            base64_data = base64.b64encode(image_data).decode('utf-8')
            encoded_image = f"data:{mime_type};base64,{base64_data}"
        else:
            encoded_image = None
        addRecipe(name, encoded_image, ingredients, steps, note, userId)
        return redirect(url_for('my_recipes'))
    return render_template('add_recipe.html', user=current_user)

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = db['recipes'].find_one({'_id': ObjectId(recipe_id)})
    if recipe is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        updated_recipe = {
            'name': request.form['name'],
            'ingredients': request.form['ingredients'],
            'image': request.form['image'],
            'steps': request.form['steps'],
            'note': request.form['note']
        }
        db['recipes'].update_one({'_id': ObjectId(recipe_id)}, {'$set': updated_recipe})
        return redirect(url_for('my_recipes'))

    return render_template('edit_recipe.html', user=current_user, recipe=recipe)

@app.route('/my_recipes')
@login_required
def my_recipes():
    res = getMyRecipes(current_user.id)
    if(res["code"] == "RECIPES_FOUND"):
        recipes = res["recipes"]
    else:
        recipes = []
    return render_template('my_recipes.html', user=current_user, recipes=recipes)

@app.route('/view_recipe/<recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    recipe = db['recipes'].find_one({'_id': ObjectId(recipe_id)})
    if recipe is None:
        return redirect(url_for('index'))
    return render_template('view_recipe.html', recipe=recipe)


@app.route('/delete/<id>')
def delete_recipe(id):
    recipes_collection = db['recipes']
    recipes_collection.delete_one({'_id': ObjectId(id)})
    return '', 204



if __name__ == '__main__':
    app.run()
