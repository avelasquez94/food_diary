from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Food:
    db_name = 'food_diary'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.food_name = db_data['food_name']
        self.calories = db_data['calories']
        self.food_date = db_data['food_date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO foods (food_name, calories, food_date, user_id) VALUES (%(food_name)s,%(calories)s,%(food_date)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query =  "SELECT * FROM foods JOIN users ON foods.user_id=users.id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        foods = []
        for row in results:
            food = cls(row)
            user_data = {
                "id":row['users.id'],
                "first_name":row['first_name'], 
                "last_name":row['last_name'], 
                "email":row['email'], 
                "password":row['password'], 
                "created_at":row['users.created_at'],
                "updated_at":row['users.updated_at']
            }
            foods.append(food)
        return foods
    
    @classmethod
    def  get_one(cls,data):
        query = 'SELECT * from foods JOIN users ON foods.user_id=users.id WHERE foods.id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        food = cls(row)
        user_data = {
                "id":row['users.id'],
                "first_name":row['first_name'], 
                "last_name":row['last_name'], 
                "email":row['email'], 
                "password":row['password'], 
                "created_at":row['users.created_at'],
                "updated_at":row['users.updated_at']
            }
        return food

    @classmethod
    def get_all_for_users(cls,data):
        query ='SELECT * from foods JOIN users ON foods.user_id=users.id WHERE foods.user_id= %(id)s;'
        print(query)
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if not results and len(results) < 1:
            return False
        return results

    @classmethod
    def update(cls, data):
        food_id = int(data['id'])
        query = "UPDATE foods SET food_name=%(food_name)s, calories=%(calories)s, food_date=%(food_date)s WHERE id={food_id};".format(food_id=food_id)
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM foods WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_food(food):
        print(food)
        is_valid = True
        if len(food['food_name']) < 3:
            is_valid = False
            flash("food name must be at least 2 characters","food")
        if len(food['calories']) < 3:
            is_valid = False
            flash("Calories must be at least 2 characters","food")
        if len(food['food_date']) < 3:
            is_valid = False
            flash("Food date must be at least 2 characters","food")
        return is_valid
