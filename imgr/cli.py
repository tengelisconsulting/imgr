"""
Options:
  list: list images
    - If a subarg is given, a wildcard match against container names is performed.
      ex. ->        imgr list bunt
    - Possible flags before args are:
      eq: equal match
      ex. ->        imgr list eq ubuntu
"""
import argparse
from typing import List

from .dclient import search_images


parser = argparse.ArgumentParser()
parser.add_argument(
    "cmd",
    help="Command",
    nargs="?"
)


def list_images(args: List[str]):
    search_args = {"strict_match": False}
    if len(args) == 2:
        query_type, name = args
        search_args["name"] = name
        if query_type == "eq":
            search_args["strict_match"] = True
    elif len(args) == 1:
        search_args["name"] = args[0]
    imgs = search_images(**search_args)
    output = "\n".join([
        str(im) for im in imgs
    ])
    print(output)
    return


CMDS = {
    "list": list_images
}


def parse():
    def err_out():
        print(__doc__)
        import sys
        sys.exit(1)
    cmd: str
    subargs: List[str]
    try:
        args, subargs = parser.parse_known_args()
        if args.cmd not in CMDS:
            print("argument {} not found".format(args.cmd))
            return err_out()
    except argparse.ArgumentError as err:
        print("bad argument: {}".format(err))
        return err_out()
    CMDS[args.cmd](subargs)
    return
