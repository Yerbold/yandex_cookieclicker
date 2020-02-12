import sqlite3


class CookieScanner:
    def get_cookies_amount(self):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            return cur.execute("""SELECT total_amount from cookies
                       WHERE ROWID IN ( SELECT max( ROWID ) FROM cookies );""").fetchone()[0]

    def set_new_record(self):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO cookies (total_amount, cookies_per_click) VALUES (0, 1)""")