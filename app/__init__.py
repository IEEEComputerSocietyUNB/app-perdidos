import os
from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from .model import Object, get_objects, add_object, delete_object, update_object, q_select, q_filter
from datetime import date


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import database
    database.init_app(app)


    @app.route('/')
    def hello():
        # database.init_db()
        return redirect(url_for('view_objects'))
    

    @app.route('/objects/create', methods=['GET', 'POST'])
    def create_object():
        if request.method == 'GET':
            return render_template('registerObject/index.html')

        else:
            db = database.get_db()
            cursor = db.cursor()

            name = request.form['name']
            description = request.form['description']
            create_date = date.today().strftime('%Y-%m-%d')
            query = add_object.format(name=name, description=description, create_date=create_date)

            cursor.execute(query)
            db.commit()

            database.close_db()

            return redirect(url_for('objects'))


    @app.route('/objects/view', methods=['GET'])
    def view_objects():
        db = database.get_db()
        cursor = db.cursor()

        query = get_objects.format()
        cursor.execute(query)

        registers = cursor.fetchall()

        objs = []
        for register in registers:
            objs.append(Object._make(register))

        database.close_db()
        
        return render_template('showCase/index.html', objs=objs)


    @app.route('/login', methods=['GET', 'POST'])
    def login():

        return render_template('login/index.html')


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():

        return render_template('signUp/index.html')
        

    @app.route('/objects', methods=['GET', 'POST'])
    def objects():
        return redirect(url_for('view_objects'))
        # db = database.get_db()
        # cursor = db.cursor()

        # if request.method == 'GET':
        #     query = get_objects.format()
        #     cursor.execute(query)

        #     registers = cursor.fetchall()

        #     objs = []
        #     for register in registers:
        #         objs.append(Object._make(register))

        #     database.close_db()
            
        #     return render_template('objects.html', objs=objs)

        # else:
        #     name = request.form['name']
        #     description = request.form['description']
        #     create_date = date.today().strftime('%Y-%m-%d')
        #     query = add_object.format(name=name, description=description, create_date=create_date)

        #     cursor.execute(query)
        #     db.commit()

        #     database.close_db()

        #     return redirect(url_for('objects'))



    # @app.route('/objects/<int:id>', methods=['PUT', 'DELETE'])
    # def object_update_or_delete(id):
    #     db = database.get_db()
    #     cursor = db.cursor()

    #     if request.method == 'DELETE':
    #         query = delete_object.format(id=id)
    #         cursor.execute(query)
    #         db.commit()

    #         database.close_db()

    #         return redirect(url_for('objects'), code=303)
    #     else:
    #         name = request.form['name']
    #         description = request.form['description']

    #         create_date = date.today().strftime('%Y-%m-%d')

    #         query = update_object.format(id=id, name=name, description=description, create_date=create_date)
    #         cursor.execute(query)
    #         db.commit()

    #         database.close_db()

    #         return redirect(url_for('objects'), code=303)
    

    @app.route('/db_test')
    def db_test():
        database.init_db()

        return 'Banco de dados inicializado com sucesso!' 


    return app