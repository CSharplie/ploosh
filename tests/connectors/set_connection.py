import json
import sys

args = {}
for i in range(1, len(sys.argv), 2):
    args[sys.argv[i][2:]] = sys.argv[i + 1]

with open(f"./tests/connectors/connections/{args['type']}.json", "w") as outfile: 
    json.dump(args, outfile)