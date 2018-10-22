import sqlite3

with sqlite3.connect("sss.db") as db:
    cursor = db.cursor()

    cursor.execute('''
    Create table IF NOT EXISTS user(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR (30) NOT NULL,
    email VARCHAR (100) NOT NULL,
    password VARCHAR (100) NOT NULL,
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    ''')

    cursor.execute('''
    INSERT INTO user(name,username,email,password,register_date)
    VALUES("Mueller","Bob","Smith@baba.com","MrBob", "11-04-2018")
    ''')
    db.commit()

    cursor.execute("SELECT * FROM user")
    print(cursor.fetchall())