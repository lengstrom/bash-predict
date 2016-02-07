import pdb, requests, sys

args = sys.argv[1:]
if len(args) <= 1:
    print ''
else:
    payload = {
        "words":" ".join(args[:-1]),
        "position":int(args[-1])
    }

    r = requests.get('http://0.0.0.0:5000/', params=payload)
    print r.text
