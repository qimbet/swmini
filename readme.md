To run mapbuilder: 

call python from PROJECT_ROOT via: 
    python -m src.map.mapBuilder

This calls the relevant main() function, etc

Calling from PROJECT_ROOT ensures that src folder is visible to downstream functions via imports


-----------------------

Test games can be run through src.game.startup.py

