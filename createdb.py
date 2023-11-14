# -*- coding: utf-8 -*-

import sqlite3

import os


def check_db(database, create=True, force=False):  # Verifica a existência do banco de dados.

    # Se 'force = True', força a criação do banco.
    # Caso ele já exista, recria.
    if force:
        if create_db(database):
            return {"success": f"Banco de dados {database} criado."}
        else:
            return {"error": "Falha ao criar banco de dados."}

    if not os.path.exists(database):  # Se o banco de dados NÃO existe no sistema de arquivos...
        if create:  # Por padrão (create=True)...
            if create_db(database):  # Cria o banco de dados.
                return {
                    "message": "Banco de dados não existe.",
                    "success": f"Banco de dados {database} criado."
                }
            else:
                return {"error": "Falha ao criar banco de dados."}
    else:  # Se o banco existe, nada será feito.
        return {"message": f"Banco de dados {database} já existe."}

    return  # Encerra.


def create_db(database):  # (Re)Cria a base de dados do aplicativo.

    try:
        # Conecta ao banco de dados SQLite3 (se não existir, será criado).
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Define as instruções SQL.
        sql_statements = [
            """
            DROP TABLE IF EXISTS item;
            """,
            """
            DROP TABLE IF EXISTS owner;
            """,
            """
            CREATE TABLE owner (
                owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                owner_name TEXT,
                owner_email TEXT,
                owner_password TEXT,
                owner_status TEXT DEFAULT 'on'
            );
            """,
            """
            CREATE TABLE item (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                item_name TEXT,
                item_description TEXT,
                item_location TEXT,
                item_owner INTEGER,
                item_status TEXT DEFAULT 'on',
                FOREIGN KEY (item_owner) REFERENCES owner(owner_id)
            );
            """,
            """
            INSERT INTO owner VALUES
            (1, '2023-09-14 12:13:14', 'Joca da Silva', 'joca@silva.com', '123', 'on'),
            (2, '2023-10-22 21:31:41', 'Setembrino Trocatapas', 'set@brino.com', '123', 'on');
            """,
            """
            INSERT INTO item VALUES
            (1, '2023-09-14 12:31:22', 'Coisa', 'Apenas uma coisa', 'Sob a escada', 1, 'on'),
            (2, '2023-10-19 21:22:23', 'Treco', 'Apenas um treco', 'Na caixa azul', 1, 'on'),
            (3, '2023-10-23 17:18:19', 'Bagulho', 'Apenas um bagulho', 'Na mesa de jantar', 2, 'on');
            """
        ]

        # Executa as instruções SQL.
        for statement in sql_statements:
            cursor.executescript(statement)

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Retorna.
        return True

    except sqlite3.Error as error:
        return False


# Exemplos de uso:
# database = "./dbitem.db" # Banco de dados a ser testado/criado.
#
# check_db(database) # Se o banco de dados não existir, será criado.
# check_db(database, create=False) # Apenas informa se o banco de dados existe ou não.
# check_db(database, force=True) # (Re)cria o banco de dados, mesmo que ele já exista.
# check_db(database, =True) # Mostra mensagens no console. Pode usar com qualquer modo acima.
