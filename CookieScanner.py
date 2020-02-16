import sqlite3


class CookieScanner:
    def get_cookies_per_second(self):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            return cur.execute("""SELECT cookies_per_second from cookies
                       WHERE ROWID IN ( SELECT max( ROWID ) FROM cookies );""").fetchone()[0]

    def get_last_id(self):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            return cur.execute("""SELECT ROWID from cookies 
                            WHERE ROWID IN (SELECT max(ROWID) FROM cookies);""").fetchone()[0]

    def get_cookies_per_click(self):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            return cur.execute("""SELECT cookies_per_click from cookies 
                            WHERE ROWID=?;""", (self.get_last_id(),)).fetchone()[0]

    def set_new_record(self, amount, cookies_per_click, cookies_per_second):
        with sqlite3.connect('cookies.db') as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO cookies (total_amount, cookies_per_click, cookies_per_second)
                            VALUES (?, ?, ?)""", (amount, cookies_per_click, cookies_per_second))
