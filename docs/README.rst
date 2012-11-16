Qurawl
======

Proof of concept for a roguelike game. There is no real gameplay at the moment.
It's all about the 4 basic actions of a grid/turn based game:

* Movement
* Picking up Items
* Dropping down Items
* Fight


Installation
------------

Dependencies: Python2.6+ (tested with Python2.6, should work with Python 2.7 too)

Download and unpack this Repository. Enter ::
 
    python start.py

at the top level directory.


Instructions
------------

Implemented are 3 Players: Otto, Xenia and Yip, 
represented by uppercase letters ``O``, ``X`` and ``Y`` respectively,
to whom you can give commands. 
Yes, you have to type commands, no conventional key control here.

New: You can make typos, the input scanner tries to match your words. 


Movement
~~~~~~~~
The 4 directions are named ``up``, ``left``, ``right`` and ``down``.
Valid commands are for example (upper- or lowercase doesn't matter): 
::
     
    -> xenia up

::

    -> otto down

::
 
    -> yip right

::
     
   etc. 


You get it.



Items
~~~~~

Items are shown as non-alphabetical characters.
Players and Monsters can pick up Health ``+`` , Armor ``]``, Strength ``!``,
a silver key ``%`` and a gold key ``$`` by moving over these locations.
Items that hurt are Acid ``~``, Traps ``^`` and mines ``*`` (Ouch!).
 


Dropping
~~~~~~~~

Pickable items can also dropped down with command syntax 

    <player name> drop <item name> <direction>

The item names are obviously (notice the underscore for double word items) :

* health
* armor
* strength
* silver_key
* gold_key


Examples:
::

    -> xenia drop armor down

::

    -> otto drop gold_key left

A drop is successful if there is enough amount available.


Fight
~~~~~

Monsters are represented by lowercase letters. 
Attack them with

   <player name> attack <direction>

Example:
::
     
    -> yip attack right



At Last
~~~~~~~

Hit RETURN and observe the monsters!
To quit type ``q``.


Todo
-----

* Doors
* Button-items for changing the level state
* Maze-like levels 
* Pathfinding
* Monster AI
* Pygame port
* and more...


License
-------

See LICENSE.txt




