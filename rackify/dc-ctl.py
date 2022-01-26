import argparse

import rackify

parser = argparse.ArgumentParser(description='Generate container based "racks" for data centre simulation')
parser.add_argument('--action', type=str, choices=["create", "delete"],
                    help='an action to use, e.g. create or delete')
parser.add_argument('--config', type=str,
                    help='filename of config file')
parser.add_argument('--filter', type=str,
                    help='container prefix for which to filter', default="rack-")

args = vars(parser.parse_args())

if args['action'] == "create":
    rackify.create(args['config'])
elif args['action'] == "delete":
    rackify.delete(args['filter'])
else:
    print("invalid usage")