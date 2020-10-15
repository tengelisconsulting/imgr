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
from typing import Dict
from typing import List

from .dclient import search_images


parser = argparse.ArgumentParser()
parser.add_argument(
    "--format",
    type=str,
    required=False
)
parser.add_argument(
    "cmd",
    help="Command",
    nargs="?"
)


def list_images(
        args: List[str],
        format_args: Dict[str, bool]
) -> str:
    search_args = {"strict_match": False}
    if len(args) == 2:
        query_type, name = args
        search_args["name"] = name
        if query_type == "eq":
            search_args["strict_match"] = True
    elif len(args) == 1:
        search_args["name"] = args[0]
    imgs = search_images(**search_args)
    if "id" in format_args:
        return "\n".join([im.image_id for im in imgs])
    return "\n".join([str(im) for im in imgs])


def keep_only():
    return


CMDS = {
    "list": list_images,
    "keep-only": keep_only,
}


def run(cmd: str,
        args: List[str],
        format_args: Dict[str, bool] = {}):
    output = CMDS[cmd](args, format_args)
    print(output)
    return


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

    format_args = {}
    if args.format:
        format_args[args.format] = True
    run(args.cmd, subargs, format_args)
    return
