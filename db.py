from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://deogadekshitija:2CS9UMdZEnbP10jk@recipe.ttcgf.mongodb.net/?appName=Recipe"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['RecipesManagement']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def getUserByEmail(email, by_id=False):
    users = db['users']
    if by_id:
        try:
            return users.find_one({'_id': ObjectId(email)})
        except Exception as e:
            print("Error converting to ObjectId:", e)
            return None
    return users.find_one({'email': email})

def createUser(email, password, name):
    users_collection = db['users']
    if users_collection.find_one({'email': email}):
        return {'code': "EXISTING_USER"}
    else:
        users_collection.insert_one({'email': email, 'password': password, 'name': name})
        return {'code': "USER_CREATED"}
    
def loginUser(email, password):
    users_collection = db['users']
    user = users_collection.find_one({'email': email, 'password': password})
    if user:
        return {'code': "USER_LOGGED_IN"}
    else:
        return {'code': "INVALID_CREDENTIALS"}
    
def addRecipe(name, image, ingredients, steps, note, userId):
    recipes_collection = db['recipes']
    recipes_collection.insert_one({'name': name, 'image': image, 'ingredients':ingredients, 'steps':steps, 'note':note, 'userId': ObjectId(userId)})
    return {'code': "RECIPE_ADDED"}

def getMyRecipes(userId):
    recipes_collection = db['recipes']
    recipes = list(recipes_collection.find({'userId': ObjectId(userId)}))
    if recipes:
        return {'code': "RECIPES_FOUND", 'recipes': recipes}
    else:
        return {'code': "NO_RECIPE_FOUND"}
    
def getAllRecipes():
    recipes_collection = db['recipes']
    recipes = list(recipes_collection.find())
    if recipes:
        return {'code': "RECIPES_FOUND", 'recipes': recipes}
    else:
        return {'code': "NO_RECIPE_FOUND"}

def editRecipe(id, name, image, ingredients, steps, note, userId="1"):
    recipes_collection = db['recipes']
    query = { "_id": ObjectId(id) }
    values = { "$set": {'name': name, 'image': image, 'ingredients':ingredients, 'steps':steps, 'note':note, 'userId': userId} }
    recipes_collection.update_one(query, values)
    return {'code': "RECIPE_UPDATED"}

def deleteRecipe(id):
    recipes_collection = db['recipes']
    result = recipes_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return {'code': 'RECIPE_DELETED'}
    return {'code': 'RECIPE_NOT_FOUND'}