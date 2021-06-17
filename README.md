# Balls
#### Requirments: [python3](https://www.python.org/downloads/), [pygame](https://www.pygame.org/wiki/GettingStarted)
## What is Balls?
Balls is a simple game created in Python module **pygame**. </br>
![In-game screen](https://github.com/SuperrMurlocc/Balls/blob/master/read/screen.png)
## How do you play Balls?
Basic **rules** and diffrent balls meanings are described in [this manual](https://github.com/SuperrMurlocc/Balls/blob/master/read/BallsManual.pdf), 
but you may as well discover the game all by yourself.
## Patches
If you're interested what has changed so far, make sure to visit [patch notes](https://github.com/SuperrMurlocc/Balls/blob/master/read/patch_notes.txt).
### Last Patch Notes:
White stripe added:
   - white stripe appears every 1.5 game tick (ball change directions every 0.025 game tick)
   - it has a short (0.0375 game tick) indication time when it blinks after which it explodes
   - explosion kills every ball except yours, but...
   - explosion takes 25 from your radius away

Game windows resized (800x600 -> 900x700)</br></br>
Manual updated, bugs fixed </br></br>
Minor GUI changes:
   - tinier letters while playing for more clarity
   - you can now quit(Q) or reset(R) game at any moment </br>

Added pink dot that heals you, but is hard to catch </br>
Added orange dot that changes steering for roughly 2 seconds </br>