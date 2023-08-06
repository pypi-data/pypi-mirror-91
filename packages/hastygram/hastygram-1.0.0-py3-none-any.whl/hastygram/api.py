import datetime
import json
from dataclasses import dataclass
from typing import Union, Sequence, Optional, Any

from aiohttp import ClientSession


@dataclass(frozen=True)
class Paginated:
    data: Sequence[Any]
    total: int
    after: Optional[str]


@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int


@dataclass(frozen=True)
class Content:
    id: str
    caption: Optional[str]
    date: datetime.datetime
    comment_count: int
    like_count: int


@dataclass(frozen=True)
class Media:
    src: str
    thumb: str
    dimensions: Dimensions


@dataclass(frozen=True)
class Image(Media, Content):
    type: str = "image"


@dataclass(frozen=True)
class Video(Media, Content):
    type: str = "video"


@dataclass(frozen=True)
class EmbeddedImage(Media):
    id: str
    type: str = "image"


@dataclass(frozen=True)
class EmbeddedVideo(Media):
    id: str
    type: str = "video"


@dataclass(frozen=True)
class Group(Content):
    medias: Sequence[Union[EmbeddedImage, EmbeddedVideo]]
    type: str = "group"


def headers() -> dict:
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFqSx",
        "x-instagram-ajax": "d3d3aea32e75",
        "x-requested-with": "XMLHttpRequest",
    }

_no_edges = {"edges": []}
_by_width = lambda r: r["config_width"]


def parse_embedded(node: dict) -> Union[EmbeddedImage, EmbeddedVideo]:
    kwargs = {
        "id": node["id"],
        "thumb": min(node["display_resources"], key=_by_width)["src"],
        "dimensions": Dimensions(**node["dimensions"]),
    }
    if node["__typename"] == "GraphImage":
        return EmbeddedImage(
            **kwargs,
            src=node["display_url"],
        )
    elif node["__typename"] == "GraphVideo":
        return EmbeddedVideo(
            **kwargs,
            src=node["video_url"],
        )
    else:
        raise TypeError("unknown", node["__typename"])


def parse(node: dict) -> Union[Image, Video, Group]:
    kwargs = {"id": node["id"],
              "date": datetime.datetime.fromtimestamp(node["taken_at_timestamp"]),
              "comment_count": node["edge_media_to_comment"]["count"],
              "like_count": node["edge_media_preview_like"]["count"],
              "caption": "\n\n".join(
                  e["node"]["text"]
                  for e in node.get("edge_media_to_caption", _no_edges)["edges"])}

    if node["__typename"] == "GraphSidecar":
        return Group(
            **kwargs,
            medias=[
                parse_embedded(e["node"])
                for e in node["edge_sidecar_to_children"]["edges"]
            ])
    elif node["__typename"] == "GraphImage":
        return Image(
            **kwargs,
            src=node["display_url"],
            thumb=node["thumbnail_src"],
            dimensions=Dimensions(**node["dimensions"]),
        )
    elif node["__typename"] == "GraphVideo":
        return Video(
            **kwargs,
            src=node["video_url"],
            thumb=node["thumbnail_src"],
            dimensions=Dimensions(**node["dimensions"]),
        )
    else:
        raise TypeError("unknown", node["__typename"])


async def user_data(s: ClientSession, username: str) -> dict:
    async with s.get(f"https://www.instagram.com/{username}/?__a=1") as r:
        data = await r.json()
        return data["graphql"]["user"]


async def _request(s: ClientSession, query_hash: str, variables: dict = None):
    async with s.get(
        "https://www.instagram.com/graphql/query/",
        params={
            "query_hash": query_hash,
            **({} if variables is None else {"variables": json.dumps(variables)}),
        }) as r:
        return await r.json()


async def user_feed(s: ClientSession, uid: str, limit: int = 12, after=None):
    data = await _request(s, "003056d32c2554def87228bc3fd9668a", {
        "id": uid,
        "first": limit,
        **({"after": after} if after else {}),
    })
    data = data["data"]["user"]["edge_owner_to_timeline_media"]
    return Paginated([parse(e["node"]) for e in data["edges"]],
                     total=data["count"],
                     after=data["page_info"].get("end_cursor"))


async def self_info(s: ClientSession):
    data = await _request(s, "d4d88dc1500312af6f937f7b804c68c3", {
        "include_chaining": False, "include_reel": True, "include_suggested_users": False,
        "include_logged_out_extras": True, "include_highlight_reels": False, "include_live_status": True,
    })
    return data["data"]["user"]["reel"]["user"]


async def self_feed(s: ClientSession):
    data = await _request(s, "c699b185975935ae2a457f24075de8c7")
    return data['data']['user']
