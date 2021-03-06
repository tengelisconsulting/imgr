import re
from typing import List
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
) -> List[Image]:
    rows = []
    if strict_match:
        rows = client.images.list(name=name)
    else:
        rows = client.images.list()
    imgs = []
    for row in rows:
        for tag in row.tags:
            image_id = row.id.split("sha256:")[1]
            img_name, vsn = tag.split(":")
            imgs.append(Image(
                image_id=image_id,
                tag=vsn,
                name=img_name
            ))
    if not strict_match and name:
        name_match = f".*{name}.*"
        imgs = [
            im for im in imgs
            if re.search(name_match, im.name)
        ]
    return imgs


def rm_image(image_id: str) -> None:
    client.images.remove(image_id)
    return
