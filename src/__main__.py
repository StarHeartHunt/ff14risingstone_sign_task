import uuid
import logging
from enum import IntEnum
from typing import Any, Annotated

import httpx
from pydantic import Field, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)


InputCookie = Annotated[
    str,
    BeforeValidator(lambda x: str.strip(str(x))),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    input_base_url: str = "https://apiff14risingstones.web.sdo.com"
    input_cookie: InputCookie = Field(default=...)
    input_user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    input_comment_content: str = '<p><span class="at-emo">[emo6]</span>&nbsp;</p>'
    input_like_post_id: int = 8
    input_comment_post_id: int = 8
    input_check_house_remain: bool = False
    input_corpid: str = ""
    input_secret: str = ""
    input_agentid: str = ""
    input_touser: str = ""


class SealType(IntEnum):
    SIGN = 1
    LIKE = 2
    COMMENT = 3


settings = Settings()
logging.debug(f"Settings: {settings.model_dump_json()}")

client = httpx.Client(
    headers={
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
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
)
client_wx = httpx.Client()


def get_wecom_token():
    r = client_wx.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={settings.input_corpid}&corpsecret={settings.input_secret}"
    )
    logging.info(r.json())
    return r.json().get("access_token")


def send_wecom(msg):
    if access_token := get_wecom_token():
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        headers = {"Content-Type": "application/json"}
        data = {
            "touser": settings.input_touser,
            "agentid": settings.input_agentid,
            "msgtype": "text",
            "text": {"content": msg},
        }
        r = client_wx.post(url=url, headers=headers, json=data)
        logging.info(r.text)
    else:
        logging.info("没有获得token，发送企业微信消息失败")


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
    if (
        settings.input_corpid
        and settings.input_secret
        and settings.input_agentid
        and settings.input_touser
    ):
        send_wecom(r.text)


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
        f"{settings.input_base_url}/api/home/userInfo/getUserInfo?page=1",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()

    return r


def main():
    logging.info("开始签到")
    sign_in()
    # do_seal(SealType.SIGN)

    # logging.info("开始点赞")
    # counter = 0
    # for _ in range(10):
    #     time.sleep(3)
    #     r = like()
    #     if r.json()["data"] == 1:
    #         counter += 1
    #         logging.info(f"第{counter}次点赞结束")

    # time.sleep(3)
    # do_seal(SealType.LIKE)

    # logging.info("开始评论")
    # time.sleep(3)
    # comment()
    # do_seal(SealType.COMMENT)

    logging.info("任务完成")

    if settings.input_check_house_remain:
        logging.info("开始检查房屋拆除倒计时")
        user_info: dict[str, Any] = get_user_info()
        house_remain_day = (
            user_info.get("data", {}).get("characterDetail", {}).get("house_remain_day")
        )
        if house_remain_day:
            raise Exception(f"房屋拆除倒计时：{house_remain_day}")


if __name__ == "__main__":
    main()
