class Player:
    def __init__(self, name, position, skills, morale, contract_end):
        self.id = None  # Will be set by the database
        self.name = name
        self.position = position
        self.skills = skills
        self.morale = morale
        self.contract_end = contract_end

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}', position='{self.position}', skills={self.skills}, morale={self.morale}, contract_end={self.contract_end})"
