import unittest
import os
import sqlite3 as sql

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
db_dir = os.path.dirname(parent_dir)

DB_PATH = os.path.join(db_dir, 'db', 'owl_league.db')

class TestDBTables(unittest.TestCase):

    def setUp(self):
        self.conn = sql.connect(DB_PATH)
        self.cur = self.conn.cursor()

    def test_player_table_unique(self):
        count_query = """
        SELECT COUNT(id) FROM Player;
        """
        self.cur.execute(count_query)
        player_count = self.cur.fetchall()

        distinct_query = """
        SELECT COUNT(DISTINCT id) FROM Player;
        """
        self.cur.execute(distinct_query)
        player_unique = self.cur.fetchall()

        self.assertEqual(player_count, player_unique)

    def test_player_overview_table_unique(self):
        count_query = """
        SELECT COUNT(id) FROM Player;
        """
        self.cur.execute(count_query)
        player_count = self.cur.fetchall()

        distinct_query = """
        SELECT COUNT(DISTINCT id) FROM Player;
        """
        self.cur.execute(distinct_query)
        player_unique = self.cur.fetchall()

        self.assertEqual(player_count, player_unique)

if __name__ == "__main__":
    unittest.main()





