import sqlite3
from sqlite3 import Error
from utils.logger import setup_logger

class DatabaseManager:
    def __init__(self, db_path='savegames/game.db'):
        self.logger = setup_logger('db_manager_logger', 'logs/db_manager.log')
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.setup_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # To access columns by name
            self.logger.info(f"Connected to database at {self.db_path}")
        except Error as e:
            self.logger.error(f"Error connecting to database: {e}")

    def setup_tables(self):
        try:
            cursor = self.conn.cursor()
            
            # Check if necessary columns exist in teams table
            cursor.execute("PRAGMA table_info(teams)")
            columns = cursor.fetchall()
            columns_dict = {column[1]: column for column in columns}
            
            # Add missing 'country' column if it doesn't exist
            if 'country' not in columns_dict:
                cursor.execute("ALTER TABLE teams ADD COLUMN country TEXT DEFAULT 'England'")
            # Add missing 'division' column if it doesn't exist
            if 'division' not in columns_dict:
                cursor.execute("ALTER TABLE teams ADD COLUMN division INTEGER DEFAULT 1")
            
            # Create 'teams' table if it does not exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    formation TEXT,
                    tactics TEXT,
                    country TEXT DEFAULT 'England',
                    division INTEGER DEFAULT 1
                );
            """)
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
            # Settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    difficulty TEXT DEFAULT 'Easy',
                    audio TEXT DEFAULT 'On'
                );
            """)
            # Insert default settings if not exist
            cursor.execute("SELECT COUNT(*) FROM settings WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO settings (id, difficulty, audio)
                    VALUES (1, 'Easy', 'On')
                """)
            # Commit the changes
            self.conn.commit()
            self.logger.info("Database tables have been set up successfully.")
        except Error as e:
            self.logger.error(f"Error setting up tables: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed.")

    # Player methods
    def add_player(self, name, position, skills, morale, contract_end):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO players (name, position, skills, morale, contract_end)
                VALUES (?, ?, ?, ?, ?)
            """, (name, position, skills, morale, contract_end))
            self.conn.commit()
            self.logger.info(f"Player '{name}' added successfully.")
            return cursor.lastrowid
        except Error as e:
            self.logger.error(f"Error adding player: {e}")

    def get_all_players(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM players")
            players = cursor.fetchall()
            self.logger.info(f"Retrieved {len(players)} players.")
            return players
        except Error as e:
            self.logger.error(f"Error retrieving players: {e}")
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
                self.logger.info(f"Retrieved player: {player_dict}")
                return player_dict
            else:
                self.logger.warning(f"No player found with ID {player_id}.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving player: {e}")
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
            self.logger.info(f"Player ID {player_id} skills updated to {new_skills}.")
        except Error as e:
            self.logger.error(f"Error updating player skills: {e}")

    def update_player_morale(self, player_id, new_morale):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE players
                SET morale = ?
                WHERE id = ?
            """, (new_morale, player_id))
            self.conn.commit()
            self.logger.info(f"Player ID {player_id} morale updated to {new_morale}.")
        except Error as e:
            self.logger.error(f"Error updating player morale: {e}")

    def update_player_contract(self, player_id, new_contract_end):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE players
                SET contract_end = ?
                WHERE id = ?
            """, (new_contract_end, player_id))
            self.conn.commit()
            self.logger.info(f"Player ID {player_id} contract end updated to {new_contract_end}.")
        except Error as e:
            self.logger.error(f"Error updating player contract end: {e}")

    def delete_player(self, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM players
                WHERE id = ?
            """, (player_id,))
            self.conn.commit()
            self.logger.info(f"Player ID {player_id} deleted successfully.")
        except Error as e:
            self.logger.error(f"Error deleting player: {e}")

    # Team methods
    def add_team(self, name, formation, tactics, division=1):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO teams (name, formation, tactics, division)
                VALUES (?, ?, ?, ?)
            """, (name, formation, tactics, division))
            self.conn.commit()
            self.logger.info(f"Team '{name}' added successfully.")
            return cursor.lastrowid
        except Error as e:
            self.logger.error(f"Error adding team: {e}")

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
                    'tactics': team['tactics'],
                    'country': team['country'],
                    'division': team['division']
                }
                self.logger.info(f"Retrieved team: {team_dict}")
                return team_dict
            else:
                self.logger.warning(f"No team found with ID {team_id}.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving team: {e}")
            return None

    def add_player_to_team(self, team_id, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO team_players (team_id, player_id)
                VALUES (?, ?)
            """, (team_id, player_id))
            self.conn.commit()
            self.logger.info(f"Player ID {player_id} added to Team ID {team_id}.")
        except Error as e:
            self.logger.error(f"Error adding player to team: {e}")

    def remove_player_from_team(self, team_id, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM team_players
                WHERE team_id = ? AND player_id = ?
            """, (team_id, player_id))
            self.conn.commit()
            self.logger.info(f"Player ID {player_id} removed from Team ID {team_id}.")
        except Error as e:
            self.logger.error(f"Error removing player from team: {e}")

    def update_team_formation(self, team_id, new_formation):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE teams
                SET formation = ?
                WHERE id = ?
            """, (new_formation, team_id))
            self.conn.commit()
            self.logger.info(f"Team ID {team_id} formation updated to '{new_formation}'.")
        except Error as e:
            self.logger.error(f"Error updating team formation: {e}")

    def update_team_tactics(self, team_id, new_tactics):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE teams
                SET tactics = ?
                WHERE id = ?
            """, (new_tactics, team_id))
            self.conn.commit()
            self.logger.info(f"Team ID {team_id} tactics updated to '{new_tactics}'.")
        except Error as e:
            self.logger.error(f"Error updating team tactics: {e}")

    def get_english_teams(self):
        """Get all English teams from the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, name, formation, tactics, division
                FROM teams 
                WHERE country = 'England'
            ''')
            teams = cursor.fetchall()
            # Convert to list of dictionaries for easier handling
            teams_list = [
                {
                    'id': team[0],
                    'name': team[1],
                    'formation': team[2],
                    'tactics': team[3],
                    'division': team[4]
                }
                for team in teams
            ]
            self.logger.info(f"Retrieved {len(teams_list)} English teams")
            return teams_list
        except Exception as e:
            self.logger.error(f"Error retrieving English teams: {str(e)}")
            return []

    def initialize_english_teams(self):
        """Initialize all English teams for a new game"""
        try:
            # Delete existing teams first
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM teams")
            
            # Premier League teams
            premier_league = [
                "Arsenal", "Aston Villa", "Chelsea", "Everton", "Liverpool", 
                "Manchester City", "Manchester United", "Newcastle United", 
                "Nottingham Forest", "Tottenham Hotspur", "West Ham United",
                "Wolves", "Brighton", "Crystal Palace", "Fulham", "Burnley",
                "Sheffield United", "Bournemouth", "Brentford", "Luton Town"
            ]

            # Insert Premier League teams with division 1
            for team in premier_league:
                cursor.execute("""
                    INSERT INTO teams (name, formation, tactics, country, division)
                    VALUES (?, ?, ?, ?, ?)
                """, (team, "4-4-2", "Balanced", "England", 1))

            # Championship teams
            championship = [
                "Leeds United", "Leicester City", "Southampton", "West Bromwich",
                "Norwich City", "Watford", "Middlesbrough", "Sunderland",
                "Stoke City", "Hull City", "Swansea City", "Cardiff City",
                "Blackburn Rovers", "QPR", "Sheffield Wednesday", "Birmingham City",
                "Millwall", "Preston", "Rotherham", "Coventry City", "Ipswich Town",
                "Plymouth Argyle", "Huddersfield Town", "Bristol City"
            ]

            # Insert Championship teams with division 2
            for team in championship:
                cursor.execute("""
                    INSERT INTO teams (name, formation, tactics, country, division)
                    VALUES (?, ?, ?, ?, ?)
                """, (team, "4-4-2", "Balanced", "England", 2))

            # League One teams
            league_one = [
                "Derby County", "Portsmouth", "Barnsley", "Bolton Wanderers",
                "Oxford United", "Charlton Athletic", "Peterborough United",
                "Lincoln City", "Bristol Rovers", "Wycombe Wanderers",
                "Shrewsbury Town", "Cambridge United", "Port Vale", "Exeter City",
                "Cheltenham Town", "Carlisle United", "Stevenage", "Fleetwood Town",
                "Burton Albion", "Reading", "Northampton Town", "Leyton Orient",
                "Wigan Athletic", "Forest Green Rovers"
            ]

            # Insert League One teams with division 3
            for team in league_one:
                cursor.execute("""
                    INSERT INTO teams (name, formation, tactics, country, division)
                    VALUES (?, ?, ?, ?, ?)
                """, (team, "4-4-2", "Balanced", "England", 3))

            # League Two teams
            league_two = [
                "Bradford City", "Mansfield Town", "Stockport County", "Notts County",
                "Wrexham", "Swindon Town", "Crewe Alexandra", "Gillingham",
                "AFC Wimbledon", "Doncaster Rovers", "Morecambe", "Grimsby Town",
                "Harrogate Town", "Salford City", "Tranmere Rovers", "Crawley Town",
                "Newport County", "Barrow", "Accrington Stanley", "Sutton United",
                "Colchester United", "MK Dons", "Walsall", "Rochdale"
            ]

            # Insert League Two teams with division 4
            for team in league_two:
                cursor.execute("""
                    INSERT INTO teams (name, formation, tactics, country, division)
                    VALUES (?, ?, ?, ?, ?)
                """, (team, "4-4-2", "Balanced", "England", 4))

            self.conn.commit()
            self.logger.info("English teams initialized successfully.")
        except Error as e:
            self.logger.error(f"Error initializing English teams: {e}")

    def get_teams_by_division(self, division):
        """Get all teams from a specific division"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, name, formation, tactics 
                FROM teams 
                WHERE division = ? 
                ORDER BY name
            ''', (division,))
            teams = cursor.fetchall()
            teams_list = [
                {
                    'id': team[0],
                    'name': team[1],
                    'formation': team[2],
                    'tactics': team[3]
                }
                for team in teams
            ]
            self.logger.info(f"Retrieved {len(teams_list)} teams from division {division}")
            return teams_list
        except Error as e:
            self.logger.error(f"Error retrieving teams from division {division}: {e}")
            return []

    # Match methods
    def add_match(self, home_team_id, away_team_id, date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO matches (home_team_id, away_team_id, date)
                VALUES (?, ?, ?)
            """, (home_team_id, away_team_id, date))
            self.conn.commit()
            match_id = cursor.lastrowid
            self.logger.info(f"Match between Team ID {home_team_id} and Team ID {away_team_id} on {date} added successfully with ID {match_id}.")
            return match_id
        except Error as e:
            self.logger.error(f"Error adding match: {e}")

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
                self.logger.info(f"Retrieved match: {match_dict}")
                return match_dict
            else:
                self.logger.warning(f"No match found with ID {match_id}.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving match: {e}")
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
            self.logger.info(f"Match ID {match_id} score updated to {home_score}-{away_score}.")
        except Error as e:
            self.logger.error(f"Error updating match score: {e}")

    def get_all_matches(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM matches")
            matches = cursor.fetchall()
            self.logger.info(f"Retrieved {len(matches)} matches.")
            return matches
        except Error as e:
            self.logger.error(f"Error retrieving matches: {e}")
            return []

    def delete_match(self, match_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM matches
                WHERE id = ?
            """, (match_id,))
            self.conn.commit()
            self.logger.info(f"Match ID {match_id} deleted successfully.")
        except Error as e:
            self.logger.error(f"Error deleting match: {e}")

    # League methods
    def add_league(self, name, season):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO leagues (name, season)
                VALUES (?, ?)
            """, (name, season))
            self.conn.commit()
            league_id = cursor.lastrowid
            self.logger.info(f"League '{name}' for season '{season}' added successfully with ID {league_id}.")
            return league_id
        except Error as e:
            self.logger.error(f"Error adding league: {e}")

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
                self.logger.info(f"Retrieved league: {league_dict}")
                return league_dict
            else:
                self.logger.warning(f"No league found with ID {league_id}.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving league: {e}")
            return None

    def get_all_leagues(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM leagues")
            leagues = cursor.fetchall()
            self.logger.info(f"Retrieved {len(leagues)} leagues.")
            return leagues
        except Error as e:
            self.logger.error(f"Error retrieving leagues: {e}")
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
            self.logger.info(f"League ID {league_id} name updated to '{new_name}'.")
        except Error as e:
            self.logger.error(f"Error updating league name: {e}")

    def update_league_season(self, league_id, new_season):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE leagues
                SET season = ?
                WHERE id = ?
            """, (new_season, league_id))
            self.conn.commit()
            self.logger.info(f"League ID {league_id} season updated to '{new_season}'.")
        except Error as e:
            self.logger.error(f"Error updating league season: {e}")

    def delete_league(self, league_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM leagues
                WHERE id = ?
            """, (league_id,))
            self.conn.commit()
            self.logger.info(f"League ID {league_id} deleted successfully.")
        except Error as e:
            self.logger.error(f"Error deleting league: {e}")

    # Finance methods
    def add_finance(self, team_id, budget, revenue=0, expenses=0):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO finances (team_id, budget, revenue, expenses)
                VALUES (?, ?, ?, ?)
            """, (team_id, budget, revenue, expenses))
            self.conn.commit()
            finance_id = cursor.lastrowid
            self.logger.info(f"Finance record for Team ID {team_id} added successfully with ID {finance_id}.")
            return finance_id
        except Error as e:
            self.logger.error(f"Error adding finance record: {e}")

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
                self.logger.info(f"Retrieved finance record: {finance_dict}")
                return finance_dict
            else:
                self.logger.warning(f"No finance record found for Team ID {team_id}.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving finance record: {e}")
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
            self.logger.info(f"Finance budget for Team ID {team_id} updated to {new_budget}.")
        except Error as e:
            self.logger.error(f"Error updating finance budget: {e}")

    def update_finance_revenue(self, team_id, additional_revenue):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE finances
                SET revenue = revenue + ?, budget = budget + ?
                WHERE team_id = ?
            """, (additional_revenue, additional_revenue, team_id))
            self.conn.commit()
            self.logger.info(f"Finance revenue for Team ID {team_id} increased by {additional_revenue}.")
        except Error as e:
            self.logger.error(f"Error updating finance revenue: {e}")

    def update_finance_expenses(self, team_id, additional_expenses):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE finances
                SET expenses = expenses + ?, budget = budget - ?
                WHERE team_id = ?
            """, (additional_expenses, additional_expenses, team_id))
            self.conn.commit()
            self.logger.info(f"Finance expenses for Team ID {team_id} increased by {additional_expenses}.")
        except Error as e:
            self.logger.error(f"Error updating finance expenses: {e}")

    def delete_finance(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM finances
                WHERE team_id = ?
            """, (team_id,))
            self.conn.commit()
            self.logger.info(f"Finance record for Team ID {team_id} deleted successfully.")
        except Error as e:
            self.logger.error(f"Error deleting finance record: {e}")

    # Settings methods
    def get_settings(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM settings WHERE id = 1")
            settings = cursor.fetchone()
            if settings:
                settings_dict = {
                    'difficulty': settings['difficulty'],
                    'audio': settings['audio']
                }
                self.logger.info(f"Retrieved settings: {settings_dict}")
                return settings_dict
            else:
                self.logger.warning("No settings found.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving settings: {e}")
            return None

    def set_setting(self, key, value):
        if key not in ['difficulty', 'audio']:
            self.logger.error(f"Invalid setting key: {key}")
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"""
                UPDATE settings
                SET {key} = ?
                WHERE id = 1
            """, (value,))
            self.conn.commit()
            self.logger.info(f"Setting '{key}' updated to '{value}'.")
            return True
        except Error as e:
            self.logger.error(f"Error setting '{key}': {e}")
            return False

    # Additional methods for teams, finances, etc.
    def get_available_players(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.* FROM players p
                LEFT JOIN team_players tp ON p.id = tp.player_id
                WHERE tp.player_id IS NULL
            """)
            players = cursor.fetchall()
            self.logger.info(f"Retrieved {len(players)} available players.")
            return players
        except Error as e:
            self.logger.error(f"Error retrieving available players: {e}")
            return []

    def get_team_of_player(self, player_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT team_id FROM team_players WHERE player_id = ?
            """, (player_id,))
            result = cursor.fetchone()
            if result:
                team_id = result['team_id']
                self.logger.info(f"Player ID {player_id} belongs to Team ID {team_id}.")
                return team_id
            else:
                self.logger.warning(f"Player ID {player_id} does not belong to any team.")
                return None
        except Error as e:
            self.logger.error(f"Error retrieving team of player: {e}")
            return None

    def get_all_teams(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM teams")
            teams = cursor.fetchall()
            self.logger.info(f"Retrieved {len(teams)} teams.")
            return teams
        except Error as e:
            self.logger.error(f"Error retrieving teams: {e}")
            return []
    # Add other necessary methods as needed

    # Add other necessary methods as needed