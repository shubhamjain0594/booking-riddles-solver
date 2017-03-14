import json
from pprint import pprint
import os


FILENAME = '/home/users/shubham/projects/hack-man-engine/resultfile.json'
NUM_GAMES = 20

def main():
    scores = [0, 0]
    for i in range(NUM_GAMES):
        os.system('./play.sh')
        with open(FILENAME, encoding='utf-8') as data_file:
            result = json.load(data_file)
            last_round = json.loads(result['game'])['states'][-1]
            players = last_round['players']
            for i in range(len(players)):
                scores[i] += players[i]['score']

    print(scores)


if __name__ == '__main__':
    main()
