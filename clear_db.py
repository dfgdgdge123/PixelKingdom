import sqlite3

con = sqlite3.connect("results.db")
cur = con.cursor()
result = cur.execute("""SELECT * FROM results""").fetchall()
res = cur.execute('''UPDATE results SET games = 0, kills = 0, wins = 0, defeats = 0, time_in_game = 0, deaths = 0,
castle_destructions = 0, levels_passed = 0''')
con.commit()


con.close()
