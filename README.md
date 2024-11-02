# Retro Football Manager

## Project Overview

Retro Football Manager is a text-based football (soccer) management simulation game with a retro aesthetic. Manage your team, make tactical decisions, and lead your club to glory!

## Features

- Team Management: Select and manage teams, set formations and tactics.
- Player Management: View player stats, manage contracts and morale.
- Match Simulation: Simulate matches with text-based commentary.
- League System: Participate in league competitions with standings and statistics.
- Transfer System: Buy and sell players, negotiate contracts.
- Financial Management: Manage club finances, budget, and sponsorships.

## Project Structure

```
retro_football_manager/
├── main.py
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   ├── player.py
│   ├── team.py
│   ├── match.py
│   ├── league.py
│   └── finance.py
├── views/
│   ├── __init__.py
│   └── menu_view.py
├── controllers/
│   ├── __init__.py
│   ├── game_controller.py
│   ├── team_controller.py
│   ├── player_controller.py
│   ├── match_controller.py
│   ├── league_controller.py
│   └── finance_controller.py
├── database/
│   ├── __init__.py
│   └── db_manager.py
├── assets/
│   ├── fonts/
│   │   └── c64_font.ttf
│   ├── sounds/
│   └── images/
└── savegames/
```

## Requirements

- Python 3.7+
- Pygame

## How to Run

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/retro_football_manager.git
   cd retro_football_manager
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python main.py
   ```

## Contributing

Contributions to Retro Football Manager are welcome! Please feel free to submit a Pull Request.
