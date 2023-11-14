import json

import sqlite3

import os

# Define o banco de dados.
database = './temp_db.db'


def get_all_items():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "SELECT * FROM item"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()

    res = []

    for res_temp in data:
        res.append(dict(res_temp))

    os.system('cls')
    print(res)


get_all_items()
