"""
Options:
  --format: Specify output format.  Options:
     id: just print image id

  list: list images
    - If a subarg is given, a wildcard match against container names is performed.
      ex.         imgr list bunt
    - Possible flags before args are:
      eq: equal match
      ex.         imgr list eq ubuntu

  keep-only: delete all images of a repository except a given tag
    ex.           imgr keep-nnly ubuntu buster
"""
import argparse
from typing import Dict
from typing import List

from .dclient import rm_image
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


def keep_only(
        args: List[str],
        format_args: Dict[str, bool]
) -> str:
    name, tag = args
    imgs = search_images(name=name)
    keep = [im.image_id for im in imgs
            if im.name == name and im.tag == tag]
    if not keep:
        return ""
    keep_id = keep[0]
    to_delete = [im.image_id for im in imgs
                 if im.image_id != keep_id]
    [rm_image(img_id) for img_id in to_delete]
    return "\n".join(to_delete)


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
