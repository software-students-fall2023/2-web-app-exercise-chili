from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import db
from bson.objectid import ObjectId


@app.route('/')
def flask_mongodb_atlas():
    recipes = db.db.collection.find({})
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['POST'])
def add_recipe():
    "Route to add recipe, POSTs a recipe, accepts form for submission and saves to database"
    name = request.form['fname']
    ingredients = request.form['fingredients']
    instructions = request.form['finstructions']
    time = request.form['ftime']

    recipe = {
        "name": name, 
        "ingredients": ingredients,
        "instructions": instructions,
        "time": time
    }
    db.db.collection.insert_one(recipe)
    return redirect(url_for('flask_mongodb_atlas'))

@app.route('/add')
def add():
    return render_template('add_recipe_form.html')

@app.route('/confirm_delete/<recipe_id>', methods=['POST'])
def confirm_delete(recipe_id):
    "Route to delete a recipe"
    db.db.collection.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('flask_mongodb_atlas'))

@app.route('/delete/<recipe_id>')
def delete_recipe(recipe_id):
    return render_template('delete_confirmation.html', recipe_id=recipe_id)

@app.route('/search')
def search():
    return "add search functionality here"

@app.route('/edit')
def edit():
    return "add edit functionality here"

@app.route('/cook/<recipe_id>')
def cook(recipe_id):
  recipe = db.db.collection.find_one({"_id": ObjectId(recipe_id)})
  if not recipe:
    return "Recipe not found"
  return render_template('recipe_info.html', recipe=recipe)



if __name__ == '__main__':
    app.run(port=8000)
