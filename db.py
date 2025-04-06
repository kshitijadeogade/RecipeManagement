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
    
def addRecipe(name, image, ingredients, steps, note, userId="1"):
    recipes_collection = db['recipes']
    recipes_collection.insert_one({'name': name, 'image': image, 'ingredients':ingredients, 'steps':steps, 'note':note, 'userId': userId})
    return {'code': "RECIPE_ADDED"}

def getMyRecipes(userId):
    recipes_collection = db['recipes']
    recipes = list(recipes_collection.find({'userId': userId}))
    if recipes:
        return {'code': "RECIPE_FOUND", 'recipes': recipes}
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
    delete = recipes_collection.delete_one({'_id': ObjectId(id)})
    return {'code': "RECIPE_DELETED"}

#print(deleteRecipe("67dabeb83948e9820e62dd75"))
#print(editRecipe("67dae766c4d788f599650d70", "Palak Paneer Lahsuni",'pic2',["Palak", "Paneer"], ["Boil the palak","Fry the paneer", "Grind the palak","Give the final tadka","Put paneer pieces in tadka"],["Dont deep fry paneer"]))
#print(editRecipe('67dabeb83948e9820e62dd75','pic2',"Palak Paneer","Palak", ["Boil the palak","Fry the paneer", "Grind the palak","Give the final tadka","Put paneer pieces in tadka"],["Dont deep fry paneer"]))

#print(createUser('deogadekshitija@gmail.com', 'password', 'name'))