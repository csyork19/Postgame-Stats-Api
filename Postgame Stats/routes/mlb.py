conn = sqlite3.connect('/Users/stormyork/Documents/NFL Information.db')
query = """
       SELECT short_name
       FROM nfl_players
       WHERE LOWER(display_name) = LOWER(?)
         AND display_name IS NOT NULL
         AND display_name != ''
         AND display_name == player_name
    
   """
cur = conn.cursor()
cur.execute(query, (short_name,))
result = cur.fetchone()
conn.close()
short_name = result[0] if result else None