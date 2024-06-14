from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "pokemon.db"


def create_connect(db_filename):
    try:
        connection = sqlite3.connect(db_filename)
        return connection
    except Error as e:
        print(e)
        return None


@app.route('/')
def render_home_page():  # put application's code here
    return render_template("index.html")


@app.route('/display/<table_type>')
def render_display_page(table_type):  # put application's code here
    query = "SELECT number, name, type1, type2, hp, attack, defence, sp_attack, sp_defence, speed, total, generation, legendary FROM pokemon_data WHERE type1 = ? OR type2 = ? OR legendary = ? OR all_mons = ?"
    connection = create_connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (table_type, table_type, table_type, table_type))

    data_list = cursor.fetchall()
    print(data_list)

    return render_template("display.html", data=data_list, table_type=table_type)


@app.route('/search', methods=['GET', 'POST'])
def render_search_page():  # put application's code here

    look_up = request.form['Search']
    title = "Search for: '" + look_up + "' "
    look_up = "%" + look_up + "%"

    query = "SELECT number, name, type1, type2, hp, attack, defence, sp_attack, sp_defence, speed, total, generation, legendary FROM pokemon_data WHERE name like ?"
    connection = create_connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (look_up, ))

    data_list = cursor.fetchall()
    print(data_list)

    return render_template("display.html", data=data_list, table_type=title)


if __name__ == '__main__':
    app.run()
