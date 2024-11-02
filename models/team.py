class Team:
    def __init__(self, name, formation, tactics):
        self.id = None  # Will be set by the database
        self.name = name
        self.formation = formation
        self.tactics = tactics
        self.players = []  # List of Player instances

    def add_player(self, player):
        if isinstance(player, Player):
            self.players.append(player)
            print(f"Player '{player.name}' added to team '{self.name}'.")
        else:
            print("Only Player instances can be added to the team.")

    def remove_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                self.players.remove(player)
                print(f"Player '{player.name}' removed from team '{self.name}'.")
                return
        print(f"No player with ID {player_id} found in team '{self.name}'.")

    def __repr__(self):
        return f"Team(id={self.id}, name='{self.name}', formation='{self.formation}', tactics='{self.tactics}', players={len(self.players)})"
