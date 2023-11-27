from flask import Flask, jsonify, request, abort, make_response, json, Response
import sqlite3

app = Flask(__name__)


@app.route('/items')
def get_items(id=0):

    sql = "SELECT * FROM item WHERE item_status != 'on'"

    if (id == 0):
        return sql
    else:
        return sql + f" AND item_id = '{id}'"


@app.route('/items/<id>')
def get_item(id):
    return get_items(id)


if __name__ == "__main__":
    app.run(debug=True)
