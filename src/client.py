from json import JSONDecodeError
import logging
import uuid

from curl_cffi import requests

from . import settings
from .models import SealType, SignRewardListResponse

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://ff14risingstones.web.sdo.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "User-Agent": settings.input_user_agent,
    "Cookie": settings.input_cookie,
}


def do_seal(type_: SealType):
    r = requests.post(
        f"{settings.input_base_url}/api/home/active/online2312/doSeal",
        data={"type": type_},  # type: ignore
        headers=HEADERS,
        impersonate="chrome124",
    )

    logging.info(r.text)


def is_login_in():
    r = requests.get(
        f"{settings.input_base_url}/api/home/sysMsg/getSysMsg",
        params={
            "page": 1,
            "limit": 10,
            "tempsuid": str(uuid.uuid4()),
        },
        headers=HEADERS,
        impersonate="chrome124",
    )

    logging.info(r.text)


def sign_in():
    r = requests.post(
        f"{settings.input_base_url}/api/home/sign/signIn",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={"tempsuid": str(uuid.uuid4())},
        headers=HEADERS,
        impersonate="chrome124",
    )
    try:
        data = r.json()
        code = data.get("code", None)
        if code is None or (code > 10000 and code != 10001):
            raise RuntimeError(f"登录时出现错误: {data!r}")
    except JSONDecodeError as e:
        raise RuntimeError(f"解析响应时出现错误: {e!r}, {r.text}")

    logging.info(r.text)


def like():
    r = requests.post(
        f"{settings.input_base_url}/api/home/posts/like",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={"id": settings.input_like_post_id, "type": 1},  # type: ignore
        headers=HEADERS,
        impersonate="chrome124",
    )
    logging.info(r.text)

    return r


def comment():
    r = requests.post(
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
        },  # type: ignore
        headers=HEADERS,
        impersonate="chrome124",
    )

    logging.info(r.text)


def get_user_info():
    r = requests.get(
        f"{settings.input_base_url}/api/home/userInfo/getUserInfo",
        params={"page": 1},
        headers={**HEADERS, "Content-Type": "application/x-www-form-urlencoded"},
        impersonate="chrome124",
    ).json()

    return r


def get_sign_reward(id_, month):
    r = requests.post(
        f"{settings.input_base_url}/api/home/sign/getSignReward",
        params={
            "tempsuid": str(uuid.uuid4()),
        },
        data={
            "id": id_,
            "month": month,
            "tempsuid": str(uuid.uuid4()),
        },
        headers=HEADERS,
        impersonate="chrome124",
    )

    return r


def get_sign_reward_list(month):
    r = requests.get(
        f"{settings.input_base_url}/api/home/sign/signRewardList",
        params={
            "month": month,
            "tempsuid": str(uuid.uuid4()),
        },
        headers=HEADERS,
        impersonate="chrome124",
    )

    return SignRewardListResponse.model_validate_json(r.text).data
