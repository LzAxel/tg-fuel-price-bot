import logging
import sqlite3


class Database():
    def __init__(self, src) -> None:
        self.connection = sqlite3.Connection(src)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS users  (
                                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id  INTEGER UNIQUE NOT NULL,
                                    username TEXT    NOT NULL
                                );
                                """)
                                
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS fuel  (
                                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name     TEXT UNIQUE NOT NULL,
                                    price    REAL    NOT NULL,
                                    compare  INTEGER NOT NULL DEFAULT 0
                                );
                                """)

    def add_user(self, user_id, username):
        try:
            with self.connection:
                self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)",
                                    (user_id, username))
        except sqlite3.IntegrityError as ex:
            pass


    def remove_user(self, user_id):
        with self.connection:
            self.cursor.execute(r"DELETE FROM users WHERE user_id = ?",
                                (user_id,))
    
    def get_users(self) -> list:
        with self.connection:
            self.cursor.execute(r"SELECT user_id, username FROM users")
            
            return self.cursor.fetchall()
    
    def save_price(self, name, price, compare):
        with self.connection:
            self.cursor.execute(r"INSERT OR REPLACE INTO fuel (name, price, compare) VALUES (?, ?, ?)",
                                (name, price, compare))
    
    def get_prices(self) -> dict:
        prices = dict()
        with self.connection:
            self.cursor.execute(r"SELECT name, price, compare FROM fuel")
            raw = self.cursor.fetchall()
        
        for i in raw:
            prices[i[0]] = {"price": i[1], "compare": i[2]}
        
        return prices