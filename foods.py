from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.food import Food

@app.route('/new/food')
def new_foods():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_food.html',user=User.get_by_id(data))


@app.route('/create/food',methods=['POST'])
def new_food():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Food.validate_food(request.form):
        return redirect('/new/food')
    data = {
        "food_name": request.form["food_name"],
        "calories": request.form["calories"],
        "food_date": request.form["food_date"],
        "user_id": session["user_id"]
    }
    Food.save(data)
    return redirect('/dashboard')

@app.route('/edit/food/<int:id>', methods=[ 'GET'])
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_food.html",edit=Food.get_one(data),user=User.get_by_id(user_data))

@app.route('/edit/food/<int:id>', methods=[ 'POST'])
def edit_food(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    print(request.form)
    if not Food.validate_food(request.form):
        return redirect(f'/edit/food/{id}')
    Food.update(request.form)
    return redirect('/dashboard')

@app.route('/update/food',methods=['POST'])
def update_food():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Food.validate_food(request.form):
        return redirect(f'/edit/food/{request.form["id"]}')
    data = {
        "food_name":request.form["food_name"],
        "calories": request.form["calories"],
        "food_date": request.form["food_date"],
    }
    Food.update(data)
    return redirect('/dashboard')

@app.route('/show/food/<int:id>')
def show_food (id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("show_food.html",foods=Food.get_all_for_users(data), user=User.get_by_id(data))

@app.route('/destroy/food/<int:id>')
def destroy_food(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Food.destroy(data)
    return redirect('/dashboard')
