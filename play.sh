#!/bin/bash

cd /home/users/shubham/projects/hack-man-engine;
java -jar game-wrapper.jar "$(cat wrapper-commands.json)"
