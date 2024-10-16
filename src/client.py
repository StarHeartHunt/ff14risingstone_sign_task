import uuid
import logging

import httpx

from . import settings
from .models import SealType, SignRewardListResponse

client = httpx.Client(
    headers={
        "accept": "application/json, text/plain, */*",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": settings.input_user_agent,
        "Cookie": settings.input_cookie,
    },
    timeout=30,
    verify=False,
    proxies="http://127.0.0.1:8888",
)


def do_seal(type_: SealType):
    r = client.post(
        f"{settings.input_base_url}/api/home/active/online2312/doSeal",
        data={"type": type_},
    )

    logging.info(r.text)


def is_login_in():
    r = client.get(
        f"{settings.input_base_url}/api/home/sysMsg/getSysMsg",
        params={
            "page": 1,
            "limit": 10,
            "tempsuid": str(uuid.uuid4()),
        },
    )

    logging.info(r.text)


def sign_in():
    r = client.post(
        f"{settings.input_base_url}/api/home/sign/signIn",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
    )

    logging.info(r.text)


def like():
    r = client.post(
        f"{settings.input_base_url}/api/home/posts/like",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={"id": settings.input_like_post_id, "type": 1},
    )
    logging.info(r.text)

    return r


def comment():
    r = client.post(
        f"{settings.input_base_url}/api/home/posts/comment",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={
            "content": settings.input_comment_content,
            "posts_id": settings.input_comment_post_id,
            "parent_id": "0",
            "root_parent": "0",
            "comment_pic": "",
        },
    )

    logging.info(r.text)


def get_user_info():
    r = client.get(
        f"{settings.input_base_url}/api/home/userInfo/getUserInfo",
        params={"page": 1},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()

    return r


def get_sign_reward(id_, month):
    r = client.post(
        f"{settings.input_base_url}/api/home/sign/getSignReward",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={
            "id": id_,
            "month": month,
            "tempsuid": str(uuid.uuid4()),
        },
    )

    return r


def get_sign_reward_list(month):
    r = client.get(
        f"{settings.input_base_url}/api/home/sign/signRewardList",
        params={
            "month": month,
            "tempsuid": str(uuid.uuid4()),
        },
    )

    return SignRewardListResponse.model_validate_json(r.text).data
