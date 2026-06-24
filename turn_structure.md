
Minor action: move
Major action: Attack, "replaces attacks", ability

EVENTS:
turn_start
turn_end
move
attack
damage
death
spot_enemy


---
#suggested to use Godot for UI
#suggested to test engine via commandline

Unit
 ├── Stats
 ├── Attacks
 ├── Abilities
 └── Position

Attack
 └── Execute()

Ability
 └── Event Hooks

Board
 └── Grid State

Game Engine
 └── Turn Resolution