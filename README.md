# booking-riddles-solver

AI Bot for booking.riddles.io

A collaborative effort with help of [flow][makemeflow.org]

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
