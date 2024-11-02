import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_path='savegames/game.db'):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.setup_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # To access columns by name
            print(f"Connected to database at {self.db_path}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def setup_tables(self):
        try:
            cursor = self.conn.cursor()
            # Players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT,
                    skills INTEGER,
                    morale INTEGER,
                    contract_end INTEGER
                );
            """)
            # Teams table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    formation TEXT,
                    tactics TEXT
                );
            """)
            # Team_Players join table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS team_players (
                    team_id INTEGER,
                    player_id INTEGER,
                    PRIMARY KEY (team_id, player_id),
                    FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE,
                    FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE
                );
            """)
            # Matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    home_team_id INTEGER,
                    away_team_id INTEGER,
                    date TEXT,
                    home_score INTEGER,
                    away_score INTEGER,
                    FOREIGN KEY (home_team_id) REFERENCES teams (id),
                    FOREIGN KEY (away_team_id) REFERENCES teams (id)
                );
            """)
            # Leagues table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leagues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    season TEXT
                );
            """)
            # Finances table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS finances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER,
                    budget INTEGER,
                    revenue INTEGER,
                    expenses INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams (id)
                );
            """)
            self.conn.commit()
            print("Database tables have been set up successfully.")
        except Error as e:
            print(f"Error setting up tables: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    # Player methods
    def add_player(self, name, position, skills, morale, contract_end):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO players (name, position, skills, morale, contract_end)
                VALUES (?, ?, ?, ?, ?)
            """, (name, position, skills, morale, contract_end))
            self.conn.commit()
            print(f"Player '{name}' added successfully.")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding player: {e}")

    def get_all_players(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM players")
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving players: {e}")
            return []

    def get_player_by_id(self, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
            player = cursor.fetchone()
            if player:
                player_dict = {
                    'id': player['id'],
                    'name': player['name'],
                    'position': player['position'],
                    'skills': player['skills'],
                    'morale': player['morale'],
                    'contract_end': player['contract_end']
                }
                return player_dict
            else:
                return None
        except Error as e:
            print(f"Error retrieving player: {e}")
            return None

    def update_player_skills(self, player_id, new_skills):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE players
                SET skills = ?
                WHERE id = ?
            """, (new_skills, player_id))
            self.conn.commit()
            print(f"Player ID {player_id} skills updated to {new_skills}.")
        except Error as e:
            print(f"Error updating player skills: {e}")

    def update_player_morale(self, player_id, new_morale):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE players
                SET morale = ?
                WHERE id = ?
            """, (new_morale, player_id))
            self.conn.commit()
            print(f"Player ID {player_id} morale updated to {new_morale}.")
        except Error as e:
            print(f"Error updating player morale: {e}")

    def update_player_contract(self, player_id, new_contract_end):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE players
                SET contract_end = ?
                WHERE id = ?
            """, (new_contract_end, player_id))
            self.conn.commit()
            print(f"Player ID {player_id} contract end updated to {new_contract_end}.")
        except Error as e:
            print(f"Error updating player contract end: {e}")

    def delete_player(self, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM players
                WHERE id = ?
            """, (player_id,))
            self.conn.commit()
            print(f"Player ID {player_id} deleted successfully.")
        except Error as e:
            print(f"Error deleting player: {e}")

    # Team methods
    def add_team(self, name, formation, tactics):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO teams (name, formation, tactics)
                VALUES (?, ?, ?)
            """, (name, formation, tactics))
            self.conn.commit()
            print(f"Team '{name}' added successfully.")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding team: {e}")

    def get_team_by_id(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
            team = cursor.fetchone()
            if team:
                team_dict = {
                    'id': team['id'],
                    'name': team['name'],
                    'formation': team['formation'],
                    'tactics': team['tactics']
                }
                return team_dict
            else:
                return None
        except Error as e:
            print(f"Error retrieving team: {e}")
            return None

    def add_player_to_team(self, team_id, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO team_players (team_id, player_id)
                VALUES (?, ?)
            """, (team_id, player_id))
            self.conn.commit()
            print(f"Player ID {player_id} added to Team ID {team_id}.")
        except Error as e:
            print(f"Error adding player to team: {e}")

    def remove_player_from_team(self, team_id, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM team_players
                WHERE team_id = ? AND player_id = ?
            """, (team_id, player_id))
            self.conn.commit()
            print(f"Player ID {player_id} removed from Team ID {team_id}.")
        except Error as e:
            print(f"Error removing player from team: {e}")

    def update_team_formation(self, team_id, new_formation):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE teams
                SET formation = ?
                WHERE id = ?
            """, (new_formation, team_id))
            self.conn.commit()
            print(f"Team ID {team_id} formation updated to '{new_formation}'.")
        except Error as e:
            print(f"Error updating team formation: {e}")

    def update_team_tactics(self, team_id, new_tactics):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE teams
                SET tactics = ?
                WHERE id = ?
            """, (new_tactics, team_id))
            self.conn.commit()
            print(f"Team ID {team_id} tactics updated to '{new_tactics}'.")
        except Error as e:
            print(f"Error updating team tactics: {e}")

    # Match methods
    def add_match(self, home_team_id, away_team_id, date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO matches (home_team_id, away_team_id, date)
                VALUES (?, ?, ?)
            """, (home_team_id, away_team_id, date))
            self.conn.commit()
            print(f"Match between Team ID {home_team_id} and Team ID {away_team_id} on {date} added successfully.")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding match: {e}")

    def get_match_by_id(self, match_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
            match = cursor.fetchone()
            if match:
                match_dict = {
                    'id': match['id'],
                    'home_team_id': match['home_team_id'],
                    'away_team_id': match['away_team_id'],
                    'date': match['date'],
                    'home_score': match['home_score'],
                    'away_score': match['away_score']
                }
                return match_dict
            else:
                return None
        except Error as e:
            print(f"Error retrieving match: {e}")
            return None

    def update_match_score(self, match_id, home_score, away_score):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE matches
                SET home_score = ?, away_score = ?
                WHERE id = ?
            """, (home_score, away_score, match_id))
            self.conn.commit()
            print(f"Match ID {match_id} score updated to {home_score}-{away_score}.")
        except Error as e:
            print(f"Error updating match score: {e}")

    def get_all_matches(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM matches")
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving matches: {e}")
            return []

    def delete_match(self, match_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM matches
                WHERE id = ?
            """, (match_id,))
            self.conn.commit()
            print(f"Match ID {match_id} deleted successfully.")
        except Error as e:
            print(f"Error deleting match: {e}")

    # League methods
    def add_league(self, name, season):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO leagues (name, season)
                VALUES (?, ?)
            """, (name, season))
            self.conn.commit()
            print(f"League '{name}' for season '{season}' added successfully.")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding league: {e}")

    def get_league_by_id(self, league_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM leagues WHERE id = ?", (league_id,))
            league = cursor.fetchone()
            if league:
                league_dict = {
                    'id': league['id'],
                    'name': league['name'],
                    'season': league['season']
                }
                return league_dict
            else:
                return None
        except Error as e:
            print(f"Error retrieving league: {e}")
            return None

    def get_all_leagues(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM leagues")
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving leagues: {e}")
            return []

    def update_league_name(self, league_id, new_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE leagues
                SET name = ?
                WHERE id = ?
            """, (new_name, league_id))
            self.conn.commit()
            print(f"League ID {league_id} name updated to '{new_name}'.")
        except Error as e:
            print(f"Error updating league name: {e}")

    def update_league_season(self, league_id, new_season):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE leagues
                SET season = ?
                WHERE id = ?
            """, (new_season, league_id))
            self.conn.commit()
            print(f"League ID {league_id} season updated to '{new_season}'.")
        except Error as e:
            print(f"Error updating league season: {e}")

    def delete_league(self, league_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM leagues
                WHERE id = ?
            """, (league_id,))
            self.conn.commit()
            print(f"League ID {league_id} deleted successfully.")
        except Error as e:
            print(f"Error deleting league: {e}")

    # Finance methods
    def add_finance(self, team_id, budget, revenue=0, expenses=0):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO finances (team_id, budget, revenue, expenses)
                VALUES (?, ?, ?, ?)
            """, (team_id, budget, revenue, expenses))
            self.conn.commit()
            print(f"Finance record for Team ID {team_id} added successfully.")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding finance record: {e}")

    def get_finance_by_team_id(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM finances WHERE team_id = ?", (team_id,))
            finance = cursor.fetchone()
            if finance:
                finance_dict = {
                    'id': finance['id'],
                    'team_id': finance['team_id'],
                    'budget': finance['budget'],
                    'revenue': finance['revenue'],
                    'expenses': finance['expenses']
                }
                return finance_dict
            else:
                return None
        except Error as e:
            print(f"Error retrieving finance record: {e}")
            return None

    def update_finance_budget(self, team_id, new_budget):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE finances
                SET budget = ?
                WHERE team_id = ?
            """, (new_budget, team_id))
            self.conn.commit()
            print(f"Finance budget for Team ID {team_id} updated to {new_budget}.")
        except Error as e:
            print(f"Error updating finance budget: {e}")

    def update_finance_revenue(self, team_id, additional_revenue):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE finances
                SET revenue = revenue + ?, budget = budget + ?
                WHERE team_id = ?
            """, (additional_revenue, additional_revenue, team_id))
            self.conn.commit()
            print(f"Finance revenue for Team ID {team_id} increased by {additional_revenue}.")
        except Error as e:
            print(f"Error updating finance revenue: {e}")

    def update_finance_expenses(self, team_id, additional_expenses):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE finances
                SET expenses = expenses + ?, budget = budget - ?
                WHERE team_id = ?
            """, (additional_expenses, additional_expenses, team_id))
            self.conn.commit()
            print(f"Finance expenses for Team ID {team_id} increased by {additional_expenses}.")
        except Error as e:
            print(f"Error updating finance expenses: {e}")

    def delete_finance(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM finances
                WHERE team_id = ?
            """, (team_id,))
            self.conn.commit()
            print(f"Finance record for Team ID {team_id} deleted successfully.")
        except Error as e:
            print(f"Error deleting finance record: {e}")

    # Additional methods for leagues, finances can be added similarly.
