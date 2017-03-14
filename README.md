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

The power of weapon or code will decrease if opponent is near

## What we want

- Avoid going near bug, go away from bug
- Go away from (opponent with weapon, when you don't have weapon)
- Try to reach the code which you are nearer to than the opponent
- When with weapon, attack the opponent if you can.
