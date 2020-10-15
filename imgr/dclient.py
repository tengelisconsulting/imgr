import re
from typing import NamedTuple

import docker


class Image(NamedTuple):
    name: str
    tag: str
    image_id: str


client = docker.from_env()


def search_images(
        name: str = "",
        strict_match: bool = True
):
    rows = []
    if strict_match:
        rows = client.images.list(name=name)
    else:
        rows = client.images.list()
    imgs = []
    for row in rows:
        for tag in row.tags:
            image_id = row.id.split("sha256:")[1]
            name, vsn = tag.split(":")
            imgs.append(Image(
                image_id=image_id,
                tag=vsn,
                name=name
            ))
    if not strict_match:
        name_match = f".*{name}.*"
        imgs = [
            im for im in imgs
            if re.search(name_match, im.name)
        ]
    return imgs
