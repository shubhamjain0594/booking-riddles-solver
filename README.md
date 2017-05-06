# booking-riddles-solver

AI Bot for booking.riddles.io

A collaborative effort with help of [flow](makemeflow.org)

# Installation

This is *Python 3* project. You need to install [hack-man-engine](https://github.com/riddlesio/hack-man-engine) and set the wrapper-commands.json . A sample wrapper-commands.json compatible with this project is

```json
{
  "wrapper": {
    "timebankMax": 10000,
    "timePerMove": 100,
    "maxTimeouts": 2,
    "resultFile": "./resultfile.json"
  },
  "match": {
    "bots": [{
      "command": "python /home/users/shubham/projects/booking-riddle/main.py"
    }, {
      "command": "python /home/users/shubham/projects/booking-riddle/main.py"
    }],
    "engine": {
      "command": "java -jar /home/users/shubham/projects/hack-man-engine/build/libs/bookinggame-2.0.0.jar"
    }
  }
}
```

# Version

## V1

- Shortest Path to the code or weapon
- Treat bug as obstacle if I don't have a weapon
- Other play is an empty space if it does not have a weapon

## V2

- We will separate the map into different layers, so that each layer maybe has a bug (I have weapon)/ bug (I don't have weapon) / opposition with weapon / code / weapon / when I have a weapon.
- Now the position where the key object is located in Map 'i', has say strength S_i and it decreases by say D_i every step, until it reaches a threshold T_i, and after F_i steps it becomes 0
- For Bug when I don't have weapon, S_i = -15, D_i = 1, T_i = -1, F_i = 20
- For Bug when I have weapon, S_i = -5, D_i = 1, T_i = 0, F_i = 10
- Opposition with weapon, S_i = -15, D_i = 1, T_i = -1, F_i = 20
- Code, S_i = 20, D_i = 1, T_i = 2, F_i = 25
- Weapon, S_i = 15, D_i = 1, T_i = 1, F_i = 25

## Final bot

I started this competition after halite.io and wanted to create a bot which has some learning component. Though rule based approaches were great, my motivation was to have some learning component where the bot learns by self play and improves.

For all the possible moves I calculate a score.

- Firstly, I calculate the nearest snippet/weapon for my opponent. So the score is result of sum of 5 different components.
	- I calculate my distance from the bug and apply function F(k1, k2, k3, d) which is described further and d is distance to the bug. The function returns a number which is added to the total score.
	- Distance to snippet. If the snippet is the one, which is nearest to the opponent then I ignore it, else the score for that is added as F(k4, k5, None, d). To compare this I also take into account which player plays first. If distance of both is same and I play first then I approach the snippet. But while this is running it seems to have some bug at times, which I didn't had time to debug.
	- Distance to weapon. If the weapon is the one, which is nearest to the opponent then I ignore it, else the score for that is added as F(k6, k7, None, d).
	- Distance to opponent if he has weapon and I don't. I add F(k8, k9, k10, d)
	- Distance to opponent if he does not have weapon and I have. I add F(k11, k12, K13, d)
- I started with F(a, b, c, d) as linear function, so that when the distance is 1, we get 'a', and then value decreases by amount of 'b' for each step, until number of steps 'd' are greater than 'c'. But in linear cases, there were lot of times when bot used to just move between two adjacent points to and fro. This is somehow related to the linearity of function.
- At the same time, I wanted a function where higher score is given when you are near and the score must change rapidly as you go away. In linear functions the rate of change is constant, and that wasnt desirable. So instead I used

```bash
F(a, b, c, d) = a*e^(-d/b) if d < c else 0
```
- I used values of a, b, c as below:

```bash
POINTS = [

(-45, 1, 4), # bug

(15, 5, None), # snippet nearer to me than opponent

(10, 4, None), # weapon

(-45, 1, 4), # opponent with weapon but I don't

(8, 3, None) # opponent without weapon but I have ]
```

The further plans were to firstly debug the code, the bot seems to chase the snippets where opponent is near. Next is to learn these values using Genetic Evolutionary Algorithms and create a bot based on that. But I had constraints on time I can put into this so this wasn't possible. I have the code, will soon be pushing to github with a blog post, if anyone's interested in taking it up and trying some evolutionary stuff go ahead.

It was a good learning experience. Congrats to winners in advance.
