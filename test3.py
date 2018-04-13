import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-a', action="store", dest="ip")
parser.add_argument('-c', action="store", dest="count", default=2, type=int)

args = parser.parse_args()
print( args.ip , args.count)
